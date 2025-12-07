from core.ui.download_ui import DownloadManager, create_download_manager

# Create download manager
manager = create_download_manager()

# Add files
manager.add_item("document.html", html_content, "html", 
                 "Bill document", "Bills/HTML")
manager.add_item("document.pdf", pdf_content, "pdf", 
                 "PDF version", "Bills/PDF")

# Add multiple files from dictionary
items_dict = {"file1.html": html1, "file2.pdf": pdf2}
manager.add_items_from_dict(items_dict, category="Generated")