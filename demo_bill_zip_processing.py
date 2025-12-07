#!/usr/bin/env python3
"""
Demo script showing enhanced ZIP processing with actual bill data
"""

from core.utils.enhanced_zip_processor import EnhancedZipProcessor, ZipConfig, create_zip_from_dict
from core.utils.download_manager import EnhancedDownloadManager, DownloadCategory, FileType
from core.ui.enhanced_download_ui import EnhancedDownloadUI


def demo_bill_document_processing():
    """Demonstrate enhanced ZIP processing with realistic bill documents"""
    
    print("=== Enhanced ZIP Processing Demo ===")
    print("Simulating bill document generation and ZIP packaging...\n")
    
    # Simulate generated bill documents
    bill_documents = {
        # HTML Documents
        "Bill_Scrutiny_Sheet_0511-N.html": """
<!DOCTYPE html>
<html>
<head>
    <title>Bill Scrutiny Sheet - 0511-N</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .bill-details { margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BILL SCRUTINY SHEET</h1>
        <h2>Public Works Department</h2>
    </div>
    
    <div class="bill-details">
        <p><strong>Bill Number:</strong> 0511-N</p>
        <p><strong>Contractor:</strong> Shree Construction Company</p>
        <p><strong>Work Order:</strong> WO-2024-48</p>
        <p><strong>Date:</strong> December 7, 2025</p>
    </div>
    
    <table>
        <tr>
            <th>Sl. No.</th>
            <th>Description</th>
            <th>Quantity</th>
            <th>Rate</th>
            <th>Amount</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Excavation Work</td>
            <td>150.00 Cu.M</td>
            <td>₹250.00</td>
            <td>₹37,500.00</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Concrete Work</td>
            <td>85.50 Cu.M</td>
            <td>₹1,200.00</td>
            <td>₹102,600.00</td>
        </tr>
        <tr>
            <td colspan="4" style="text-align: right;"><strong>Total Amount:</strong></td>
            <td><strong>₹140,100.00</strong></td>
        </tr>
    </table>
</body>
</html>
        """,
        
        "Deviation_Report_0511-N.html": """
<!DOCTYPE html>
<html>
<head>
    <title>Deviation Report - 0511-N</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .deviation-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .highlight { background-color: #fff3cd; }
    </style>
</head>
<body>
    <div class="header">
        <h1>DEVIATION REPORT</h1>
        <h2>Bill Number: 0511-N</h2>
    </div>
    
    <table class="deviation-table">
        <tr>
            <th>Item</th>
            <th>Schedule Rate</th>
            <th>Actual Rate</th>
            <th>Variance</th>
            <th>Remarks</th>
        </tr>
        <tr class="highlight">
            <td>Concrete M25</td>
            <td>₹1,100.00</td>
            <td>₹1,200.00</td>
            <td>+₹100.00 (9.09%)</td>
            <td>Market rate increase</td>
        </tr>
        <tr>
            <td>Steel Fe-500</td>
            <td>₹55.00/kg</td>
            <td>₹58.00/kg</td>
            <td>+₹3.00 (5.45%)</td>
            <td>Quarterly revision</td>
        </tr>
    </table>
    
    <div style="margin-top: 30px;">
        <p><strong>Prepared by:</strong> _____________________</p>
        <p><strong>Checked by:</strong> _____________________</p>
        <p><strong>Approved by:</strong> _____________________</p>
    </div>
</body>
</html>
        """,
        
        # PDF-like binary content (simulated)
        "Bill_Scrutiny_Sheet_0511-N.pdf": b"%PDF-1.4\n%Simulated PDF content for Bill Scrutiny Sheet\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000108 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n158\n%%EOF",
        
        "Deviation_Report_0511-N.pdf": b"%PDF-1.4\n%Simulated PDF content for Deviation Report\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000108 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n158\n%%EOF",
        
        # Excel file (simulated)
        "Enhanced_Bill_0511-N.xlsx": b"PK\x03\x04\x14\x00\x00\x00\x08\x00Simulated Excel file with enhanced summary sheet\n[Content_Types].xml\x00\x00PK\x03\x04\x14\x00\x00\x00\x08\x00xl/workbook.xmlPK\x03\x04\x14\x00\x00\x00\x08\x00xl/worksheets/sheet1.xmlPK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00",
        
        # JSON data export
        "Bill_Data_0511-N.json": """
{
  "bill_number": "0511-N",
  "contractor": "Shree Construction Company",
  "work_order": "WO-2024-48",
  "total_amount": 140100.00,
  "items": [
    {
      "sl_no": 1,
      "description": "Excavation Work",
      "quantity": "150.00 Cu.M",
      "rate": 250.00,
      "amount": 37500.00
    },
    {
      "sl_no": 2,
      "description": "Concrete Work",
      "quantity": "85.50 Cu.M",
      "rate": 1200.00,
      "amount": 102600.00
    }
  ],
  "deviations": [
    {
      "item": "Concrete M25",
      "schedule_rate": 1100.00,
      "actual_rate": 1200.00,
      "variance": 100.00,
      "percentage": 9.09,
      "remarks": "Market rate increase"
    }
  ]
}
        """.strip(),
        
        # Summary report
        "Processing_Summary.txt": """
BILL PROCESSING SUMMARY
=====================

Bill Number: 0511-N
Contractor: Shree Construction Company
Work Order: WO-2024-48
Processing Date: December 7, 2025

Documents Generated:
- Bill Scrutiny Sheet (HTML & PDF)
- Deviation Report (HTML & PDF)
- Enhanced Excel File with Summary Sheet
- JSON Data Export

Statistics:
- Total Items Processed: 2
- Deviations Identified: 1
- Total Amount: ₹140,100.00
- Processing Time: 2.3 seconds

File Sizes:
- HTML Documents: 2.1 KB
- PDF Documents: 0.3 KB
- Excel File: 0.2 KB
- JSON Data: 0.8 KB

Generated by BillGenerator Unified v2.0.0
        """.strip()
    }
    
    # Create download manager and add items
    print("1. Creating download manager and organizing documents...")
    dm = EnhancedDownloadManager()
    
    # Add HTML documents
    dm.add_html_document(
        "Bill_Scrutiny_Sheet_0511-N.html", 
        bill_documents["Bill_Scrutiny_Sheet_0511-N.html"],
        "Main bill scrutiny sheet in HTML format"
    )
    
    dm.add_html_document(
        "Deviation_Report_0511-N.html", 
        bill_documents["Deviation_Report_0511-N.html"],
        "Deviation analysis report in HTML format"
    )
    
    # Add PDF documents
    dm.add_pdf_document(
        "Bill_Scrutiny_Sheet_0511-N.pdf", 
        bill_documents["Bill_Scrutiny_Sheet_0511-N.pdf"],
        "Main bill scrutiny sheet in PDF format"
    )
    
    dm.add_pdf_document(
        "Deviation_Report_0511-N.pdf", 
        bill_documents["Deviation_Report_0511-N.pdf"],
        "Deviation analysis report in PDF format"
    )
    
    # Add Excel file
    dm.add_excel_file(
        "Enhanced_Bill_0511-N.xlsx", 
        bill_documents["Enhanced_Bill_0511-N.xlsx"],
        "Excel file with enhanced summary sheet"
    )
    
    # Add JSON data
    dm.add_item(
        "Bill_Data_0511-N.json",
        bill_documents["Bill_Data_0511-N.json"].encode('utf-8'),
        FileType.JSON,
        "Structured bill data in JSON format",
        DownloadCategory.GENERAL
    )
    
    # Add summary report
    dm.add_item(
        "Processing_Summary.txt",
        bill_documents["Processing_Summary.txt"].encode('utf-8'),
        FileType.TXT,
        "Processing summary and statistics",
        DownloadCategory.GENERAL
    )
    
    print(f"   ✅ Added {len(dm.get_all_items())} documents to download manager")
    
    # Show organization
    categorized = dm.get_items_by_category()
    print("   📁 Documents organized by category:")
    for category, items in categorized.items():
        print(f"      - {category.value}: {len(items)} files")
    
    # Create enhanced ZIP with configuration
    print("\n2. Creating enhanced ZIP archive with configuration...")
    config = ZipConfig(
        compression_level=6,           # Standard compression
        max_file_size_mb=50,          # 50MB limit per file
        max_total_size_mb=100,        # 100MB total limit
        enable_integrity_check=True,   # Verify ZIP integrity
        memory_limit_mb=256,          # 256MB memory limit
        enable_progress_tracking=True, # Enable progress tracking
        preserve_directory_structure=True # Maintain folder structure
    )
    
    # Prepare data for ZIP creation
    data_dict = {}
    for item in dm.get_all_items():
        data_dict[item.name] = item.content
    
    # Create ZIP with progress tracking
    print("   📦 Creating ZIP archive...")
    
    def progress_callback(progress, message):
        print(f"      Progress: {progress:.1f}% - {message}")
    
    with EnhancedZipProcessor(config) as processor:
        processor.set_progress_callback(progress_callback)
        
        # Add files to processor
        for filename, content in data_dict.items():
            processor.add_file_from_memory(content, filename)
        
        # Create ZIP
        zip_buffer, metrics = processor.create_zip()
    
    print(f"   ✅ ZIP archive created successfully!")
    print(f"      Total files: {metrics['total_files']}")
    print(f"      Total size: {metrics['total_size_bytes']} bytes")
    print(f"      Compression level: {metrics['compression_level']}")
    print(f"      Memory usage: {metrics['memory_usage_mb']:.2f} MB")
    
    # Show statistics
    print("\n3. Download Statistics:")
    stats = dm.get_statistics()
    print(f"   📊 Total Items: {stats['total_items']}")
    print(f"   💾 Total Size: {stats['total_size_mb']} MB")
    print("   📁 Categories:")
    for category, count in stats['categories'].items():
        print(f"      - {category}: {count} files")
    print("   📄 File Types:")
    for file_type, count in stats['file_types'].items():
        print(f"      - {file_type}: {count} files")
    
    # Demonstrate filtering
    print("\n4. Filtered Downloads:")
    html_docs = dm.get_items_by_filter(file_type=FileType.HTML)
    pdf_docs = dm.get_items_by_filter(file_type=FileType.PDF)
    print(f"   📄 HTML Documents: {len(html_docs)} files")
    print(f"   📕 PDF Documents: {len(pdf_docs)} files")
    
    # Show ZIP creation metrics
    print("\n5. ZIP Creation Metrics:")
    print(f"   ⚡ Processing Time: {metrics['processing_time']}")
    print(f"   🗃️  Compression Level: {metrics['compression_level']}")
    print(f"   💾 Files Processed: {metrics['total_files']}")
    
    print("\n🎉 Enhanced ZIP Processing Demo Completed Successfully!")
    print("\nThis demonstrates how the enhanced ZIP system:")
    print("✅ Organizes documents by category")
    print("✅ Provides progress tracking")
    print("✅ Enforces security limits")
    print("✅ Maintains file integrity")
    print("✅ Offers flexible configuration")
    print("✅ Generates detailed metrics")


if __name__ == "__main__":
    demo_bill_document_processing()