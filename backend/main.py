from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid

from engine.models.document_model import UnifiedDocument, DocumentStatus
from engine.workflow.state_machine import DocumentWorkflowEngine, WorkflowError

app = FastAPI(title="BillGenerator Unified API", version="0.1.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock database/store for demonstration
# In Phase 7, this will be replaced by a real DB (PostgreSQL/Redis)
documents = {
    "1": UnifiedDocument(
        id="1",
        status=DocumentStatus.PRINT_READY,
        metadata={
            "bill_no": "BILL-2026-001",
            "work_name": "Stadium Structural Reinforcement",
            "contractor_name": "Global Infra Corp",
            "source_mode": "Mode 1",
            "source_filename": "stadium_reinforcement.xlsx"
        },
        items=[]
    ),
    "2": UnifiedDocument(
        id="2",
        status=DocumentStatus.CALCULATED,
        metadata={
            "bill_no": "BILL-2026-012",
            "work_name": "Main Canal Lining Phase 4",
            "contractor_name": "PWD Primary Agency",
            "source_mode": "Mode 1",
            "source_filename": "canal_lining_p4.xlsx"
        },
        items=[]
    )
}

@app.get("/")
async def root():
    return {"message": "BillGenerator Unified API is running", "version": "0.1.0"}

@app.get("/documents/", response_model=List[UnifiedDocument])
async def list_documents():
    return list(documents.values())

@app.post("/documents/", response_model=UnifiedDocument)
async def create_document(doc: UnifiedDocument):
    if not doc.id:
        doc.id = str(uuid.uuid4())
    documents[doc.id] = doc
    return doc

@app.get("/documents/{doc_id}", response_model=UnifiedDocument)
async def get_document(doc_id: str):
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    return documents[doc_id]

@app.post("/documents/{doc_id}/transition")
async def transition_document(doc_id: str, target_status: DocumentStatus):
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc = documents[doc_id]
    try:
        updated_doc = DocumentWorkflowEngine.transition_to(doc, target_status)
        documents[doc_id] = updated_doc
        return updated_doc
    except WorkflowError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
