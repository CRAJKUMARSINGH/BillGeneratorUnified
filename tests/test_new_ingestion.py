import sys
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.ingestion.excel_ingestor import ExcelIngestor

def test_excel_ingestion():
    # Set encoding for safe printing
    import sys
    import io
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    ingestor = ExcelIngestor()
    test_file = Path("TEST_INPUT_FILES/FirstFINALnoExtra.xlsx")
    
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
        
    print(f"Testing ingestion of: {test_file}")
    
    # 1. Test Excel Ingestion
    doc = ingestor.ingest(str(test_file))
    
    print("\n--- Ingested Document (Excel) ---")
    print(f"ID: {doc.id}")
    print(f"Work: {doc.metadata.work_name}")
    print(f"Bill No: {doc.metadata.bill_no}")
    print(f"Contractor: {doc.metadata.contractor_name}")
    print(f"Item Count: {len(doc.items)}")
    print(f"Total Amount: {doc.summary['total_amount']}")
    
    if doc.items:
        for i, item in enumerate(doc.items[:5]):
            # Safe print to avoid encoding errors
            safe_desc = item.description[:50].encode('ascii', 'replace').decode('ascii')
            print(f"[{i}] {item.item_no}: {safe_desc} [Qty: {item.quantity}, Amt: {item.amount}]")
        
    # 2. Test OCR Ingestion (Mocked)
    from engine.ingestion.ocr_ingestor import OCRIngestor
    ocr_ingestor = OCRIngestor()
    ocr_doc = ocr_ingestor.ingest("mock_scanned_bill.png")
    print("\n--- Ingested Document (OCR Mock) ---")
    print(f"Item Count: {len(ocr_doc.items)}")
    print(f"First OCR Item: {ocr_doc.items[0].description[:50]}")

    # Save samples
    output_dir = Path("OUTPUT")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "new_ingestion_test.json", "w", encoding='utf-8') as f:
        f.write(doc.model_dump_json(indent=2))
    
    print(f"\nFinal report saved to: {output_dir / 'new_ingestion_test.json'}")

if __name__ == "__main__":
    test_excel_ingestion()
