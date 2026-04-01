export type DocumentStatus = 'UPLOADED' | 'PARSED' | 'INPUT_EDITED' | 'CALCULATED' | 'FINAL_EDITED' | 'PRINT_READY' | 'EXPORTED';

export interface BillItem {
  item_no: string;
  description: string;
  unit: string;
  quantity: number;
  rate: number;
  amount: number;
  is_part_rate?: boolean;
}

export interface DocumentMetadata {
  bill_no: string;
  work_name: string;
  contractor_name: string;
  agreement_no?: string;
  date_created: string;
  last_modified: string;
  source_mode: string;
  source_filename?: string;
}

export interface UnifiedDocument {
  id: string;
  status: DocumentStatus;
  metadata: DocumentMetadata;
  items: BillItem[];
  summary: {
    total_amount: number;
    tax_amount: number;
    net_amount: number;
  };
}
