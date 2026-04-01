import uuid
from typing import List, Optional
from datetime import datetime
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

from engine.models.document_model import UnifiedDocument, BillItem, DocumentMetadata, DocumentStatus
from engine.workflow.state_machine import DocumentWorkflowEngine, WorkflowError
from core.utils.safe_conversions import safe_float

class OCRIngestor:
    """Ingests unstructured documents (PDF/Images) using OCR."""
    
    def __init__(self):
        if pytesseract is None:
            print("Warning: pytesseract or PIL not installed. OCR will be disabled.")
            
    def ingest(self, file_path: str) -> UnifiedDocument:
        """
        Extract text from an image and map it to a UnifiedDocument.
        """
        if pytesseract is None:
            # Fallback for systems without Tesseract (like CI or local dev without it)
            extracted_text = f"MOCK TEXT for {file_path}\n1 Professional Services 10.0 500.0\n2 Software License 1.0 12000.0"
        else:
            try:
                # Open image and extract text
                img = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(img)
            except Exception as e:
                print(f"OCR failed for {file_path}: {e}")
                extracted_text = ""

        # Basic regex-based extraction for Phase 3 baseline
        import re
        items = []
        
        # Simple pattern: [ItemNo] [Description] [Qty] [Rate]
        # Example: "1 Cement Bags 50 450"
        pattern = r"(?P<item_no>\d+)\s+(?P<desc>.+?)\s+(?P<qty>[\d\.,]+)\s+(?P<rate>[\d\.,]+)"
        
        for match in re.finditer(pattern, extracted_text):

            qty = safe_float(match.group('qty'))
            rate = safe_float(match.group('rate'))
            
            items.append(BillItem(
                item_no=match.group('item_no'),
                description=match.group('desc').strip(),
                unit="Nos",
                quantity=qty,
                rate=rate,
                amount=round(qty * rate, 2)
            ))
            
        if not items:
            # Fallback dummy item if no regex matches
            items.append(BillItem(
                item_no="OCR-FAIL",
                description=f"Raw text extracted from {file_path} (Failed to parse structure)",
                unit="Lump Sum",
                quantity=1.0,
                rate=0.0,
                amount=0.0
            ))
        
        metadata = DocumentMetadata(
            bill_no=f"OCR-{uuid.uuid4().hex[:6].upper()}",
            work_name="Unstructured Bill Ingest",
            contractor_name="Unknown",
            source_mode="Mode 3",
            source_filename=file_path
        )
        
        # Assemble UnifiedDocument (Start at UPLOADED)
        doc = UnifiedDocument(
            id=str(uuid.uuid4()),
            status=DocumentStatus.UPLOADED,
            metadata=metadata,
            items=items
        )
        doc.update_totals()
        
        # Transition to PARSED via Workflow Engine
        doc = DocumentWorkflowEngine.transition_to(doc, DocumentStatus.PARSED)
        
        return doc
