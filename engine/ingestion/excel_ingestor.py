import uuid
from typing import Optional, List
import pandas as pd
from engine.models.document_model import UnifiedDocument, BillItem, DocumentMetadata, DocumentStatus
from engine.workflow.state_machine import DocumentWorkflowEngine
from core.processors.excel_processor import ExcelProcessor
from core.utils.safe_conversions import safe_float

class ExcelIngestor:
    """Adapts legacy ExcelProcessor output to UnifiedDocument model."""
    
    def __init__(self):
        self.processor = ExcelProcessor()
        
    def ingest(self, file_path: str) -> UnifiedDocument:
        """
        Process an Excel file and convert it to a UnifiedDocument.
        """
        # Note: legacy ExcelProcessor.process_excel takes a file object or path
        result_data = self.processor.process_excel(file_path)
        
        # Extract metadata from title_data
        title_data = result_data.get('title_data', {})
        
        # Combine work order, bill quantity, and extra items
        all_items = []
        
        # Helper to process DataFrames from different sheets
        def process_df(df, source_mode):
            if df is None or df.empty:
                return []
            

            items = []
            for _, row in df.iterrows():
                # Item No. is already standardized to string in legacy processor
                item_no = str(row.get('Item No.', ''))
                description = str(row.get('Description', ''))
                
                if not description or description.lower() == 'nan':
                    continue
                
                item = BillItem(
                    item_no=item_no,
                    description=description,
                    unit=str(row.get('Unit', 'Nos')),
                    quantity=safe_float(row.get('Quantity', 0.0)),
                    rate=safe_float(row.get('Rate', 0.0)),
                    amount=safe_float(row.get('Amount', 0.0)),
                )
                items.append(item)
            return items

        # Process sheets prioritizing Work Order or Bill Quantity
        # In this legacy system, they are often used interchangeably or together
        work_order_items = process_df(result_data.get('work_order_data'), "Mode 1")
        bill_qty_items = process_df(result_data.get('bill_quantity_data'), "Mode 1")
        extra_items = process_df(result_data.get('extra_items_data'), "Mode 1")
        
        # Use simple heuristic: if work_order has items, use it. Else use bill_qty.
        # Plus always append extra items.
        if work_order_items:
            all_items = work_order_items
        else:
            all_items = bill_qty_items
            
        all_items.extend(extra_items)
            
        # Create metadata
        metadata = DocumentMetadata(
            bill_no=str(title_data.get('Running Bill No. :', title_data.get('Bill No.', f"BILL-{uuid.uuid4().hex[:6].upper()}"))),
            work_name=str(title_data.get('Name of Work :-', title_data.get('Work Name', "Unknown Project"))),
            contractor_name=str(title_data.get('Name of Agency / supplier :', title_data.get('Contractor', "Detected Contractor"))),
            agreement_no=str(title_data.get('Agreement No. :', '')),
            source_mode="Mode 1",
            source_filename=str(file_path)
        )
        
        # Assemble UnifiedDocument (Start at UPLOADED)
        doc = UnifiedDocument(
            id=str(uuid.uuid4()),
            status=DocumentStatus.UPLOADED,
            metadata=metadata,
            items=all_items
        )
        doc.update_totals()
        
        # Transition to PARSED via Workflow Engine
        doc = DocumentWorkflowEngine.transition_to(doc, DocumentStatus.PARSED)
        
        return doc
