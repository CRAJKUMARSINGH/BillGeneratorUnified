"""
PDF Generator - Generate PDF documents from HTML content
"""
import asyncio
import io
from typing import Dict, Any
from core.generators.base_generator import BaseGenerator

class PDFGenerator(BaseGenerator):
    """Generates PDF documents from HTML content"""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
    
    async def _convert_html_to_pdf_async(self, html_content: str, doc_name: str) -> bytes:
        """
        Convert HTML to PDF using Playwright for pixel-perfect rendering
        PERMANENT FIX: Tables will NOT shrink
        Deviation Statement uses LANDSCAPE orientation
        """
        try:
            from playwright.async_api import async_playwright
            
            # Determine page orientation based on document name
            is_landscape = 'Deviation' in doc_name
            page_size = 'A4 landscape' if is_landscape else 'A4'
            
            # Add CSS to prevent table shrinking + CSS zoom for pixel-perfect rendering
            no_shrink_css = f"""
            <style>
                /* CRITICAL: CSS Zoom for pixel-perfect scaling */
                body {{
                    zoom: 1.0;
                    -moz-transform: scale(1.0);
                    -moz-transform-origin: 0 0;
                }}
                
                /* CRITICAL: Prevent table shrinking */
                table {{
                    table-layout: fixed !important;
                    width: 100% !important;
                    min-width: 100% !important;
                    max-width: 100% !important;
                    border-collapse: collapse !important;
                }}
                th, td {{
                    white-space: normal !important;
                    word-wrap: break-word !important;
                    overflow-wrap: break-word !important;
                    box-sizing: border-box !important;
                }}
                
                /* Disable text rendering optimizations */
                * {{
                    -webkit-font-smoothing: antialiased !important;
                    -moz-osx-font-smoothing: grayscale !important;
                    text-rendering: optimizeLegibility !important;
                }}
            </style>
            """
            
            # Inject CSS into HTML
            if '<head>' in html_content:
                html_content = html_content.replace('<head>', f'<head>\n{no_shrink_css}', 1)
            else:
                html_content = html_content.replace('<html>', f'<html>\n<head>\n{no_shrink_css}\n</head>', 1)
            
            # Launch Playwright and convert to PDF
            async with async_playwright() as p:
                # Use Chromium browser
                browser = await p.chromium.launch(
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--no-first-run',
                        '--no-zygote',
                        '--single-process'  # Critical for Streamlit Cloud compatibility
                    ]
                )
                page = await browser.new_page()
                
                # Set viewport to A4 size at 96 DPI
                await page.set_viewport_size({'width': 794, 'height': 1123})
                
                # Set the HTML content
                await page.set_content(html_content, wait_until='networkidle')
                
                # Wait for rendering
                await page.wait_for_timeout(500)
                
                # Generate PDF with NO SHRINKING settings
                # Use landscape for Deviation Statement
                pdf_bytes = await page.pdf(
                    format='A4',
                    landscape=is_landscape,  # Landscape for Deviation Statement
                    print_background=True,
                    margin={'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
                    prefer_css_page_size=True,
                    display_header_footer=False,
                    scale=1.0  # CRITICAL: No scaling = no shrinking
                )
                
                await browser.close()
                return pdf_bytes
        except Exception as e:
            print(f"Playwright PDF conversion failed: {e}")
            # Fallback to xhtml2pdf if Playwright fails
            try:
                return self._convert_html_to_pdf_fallback(html_content, doc_name)
            except Exception as fallback_error:
                print(f"Fallback PDF conversion also failed: {fallback_error}")
                raise Exception("No PDF engine available. Please check requirements installation.")
    
    def _convert_html_to_pdf_fallback(self, html_content: str, doc_name: str) -> bytes:
        """
        Fallback PDF conversion using xhtml2pdf (works on Streamlit Cloud)
        """
        try:
            print("[INFO] Using xhtml2pdf (Streamlit Cloud compatible)...")
            from xhtml2pdf import pisa
            import io
            
            # Add CSS zoom to HTML for better rendering
            zoom = 1.0
            html_with_zoom = self.add_css_zoom_to_html(html_content, zoom)
            
            output = io.BytesIO()
            pisa.CreatePDF(html_with_zoom, dest=output, encoding="utf-8")
            return output.getvalue()
        except Exception as e:
            print(f"[WARNING] xhtml2pdf failed: {e}")
            raise Exception("No PDF engine available. Please check requirements installation.")
    
    def add_css_zoom_to_html(self, html_content: str, zoom: float = 1.0) -> str:
        """
        Add CSS zoom to HTML content for better rendering
        """
        zoom_style = f"""
        <style>
            body {{
                zoom: {zoom};
                -moz-transform: scale({zoom});
                -moz-transform-origin: 0 0;
            }}
        </style>
        """
        
        if '<head>' in html_content:
            return html_content.replace('<head>', f'<head>\n{zoom_style}', 1)
        else:
            return html_content.replace('<html>', f'<html>\n<head>\n{zoom_style}\n</head>', 1)
    
    def create_pdf_documents(self, documents: Dict[str, str]) -> Dict[str, bytes]:
        """
        Convert HTML documents to PDF format using Playwright for exact HTML rendering
        
        Args:
            documents: Dictionary of HTML documents
            
        Returns:
            Dictionary of PDF documents as bytes
        """
        pdf_documents = {}
        
        # Convert each document to PDF asynchronously
        async def convert_all():
            tasks = []
            for doc_name, html_content in documents.items():
                task = self._convert_html_to_pdf_async(html_content, doc_name)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, (doc_name, result) in enumerate(zip(documents.keys(), results)):
                if isinstance(result, Exception):
                    print(f"Failed to convert {doc_name} to PDF: {result}")
                    # Fallback to xhtml2pdf if Playwright fails
                    try:
                        pdf_documents[doc_name] = self._convert_html_to_pdf_fallback(documents[doc_name], doc_name)
                    except Exception as fallback_error:
                        print(f"Fallback PDF conversion also failed for {doc_name}: {fallback_error}")
                else:
                    pdf_documents[doc_name] = result
        
        # Run the async conversion
        asyncio.run(convert_all())
        
        return pdf_documents
    
    def batch_convert(self, html_documents: Dict[str, str], 
                     output_dir: str = "output_pdfs",
                     enable_fallback: bool = True) -> Dict[str, str]:
        """
        Batch convert HTML documents to PDFs
        
        Args:
            html_documents: Dictionary mapping document names to HTML content
            output_dir: Directory to save PDFs
            enable_fallback: Enable fallback to xhtml2pdf if Playwright fails
            
        Returns:
            Dictionary mapping document names to PDF file paths
        """
        import os
        import re
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert documents to PDFs
        pdf_paths = {}
        pdf_documents = self.create_pdf_documents(html_documents)
        
        # Save PDFs to files
        for doc_name, pdf_content in pdf_documents.items():
            # Generate safe filename
            safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', doc_name)
            if not safe_name.endswith('.pdf'):
                safe_name += '.pdf'
            
            pdf_path = os.path.join(output_dir, safe_name)
            
            try:
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_content)
                pdf_paths[doc_name] = pdf_path
                print(f"Saved {doc_name} to {pdf_path}")
            except Exception as e:
                print(f"Failed to save {doc_name}: {e}")
        
        return pdf_paths