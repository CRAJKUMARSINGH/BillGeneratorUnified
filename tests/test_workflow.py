import pytest
import uuid
from engine.models.document_model import UnifiedDocument, DocumentStatus, BillItem, DocumentMetadata
from engine.workflow.state_machine import DocumentWorkflowEngine, WorkflowError

@pytest.fixture
def sample_doc():
    return UnifiedDocument(
        id=str(uuid.uuid4()),
        status=DocumentStatus.UPLOADED,
        metadata=DocumentMetadata(
            bill_no="TEST-001",
            work_name="Test Project",
            contractor_name="Test Contractor",
            source_mode="Test",
            source_filename="test.xlsx"
        ),
        items=[
            BillItem(item_no="1", description="Item 1", unit="Nos", quantity=10.0, rate=100.0, amount=1000.0)
        ]
    )

def test_valid_transition(sample_doc):
    # UPLOADED -> PARSED is valid
    doc = DocumentWorkflowEngine.transition_to(sample_doc, DocumentStatus.PARSED)
    assert doc.status == DocumentStatus.PARSED
    assert len(doc.history) == 1
    assert "Transitioned to PARSED" in doc.history[0]["action"]

def test_invalid_transition(sample_doc):
    # UPLOADED -> CALCULATED is invalid (must go to PARSED first)
    with pytest.raises(WorkflowError) as excinfo:
        DocumentWorkflowEngine.transition_to(sample_doc, DocumentStatus.CALCULATED)
    assert "Invalid transition" in str(excinfo.value)

def test_validation_print_ready(sample_doc):
    # UPLOADED -> PARSED -> CALCULATED
    doc = DocumentWorkflowEngine.transition_to(sample_doc, DocumentStatus.PARSED)
    doc = DocumentWorkflowEngine.transition_to(doc, DocumentStatus.CALCULATED)
    
    # Try PRINT_READY without work_name
    doc.metadata.work_name = ""
    with pytest.raises(WorkflowError) as excinfo:
        DocumentWorkflowEngine.transition_to(doc, DocumentStatus.PRINT_READY)
    assert "Work Name is required" in str(excinfo.value)
    
    # Fix and try again
    doc.metadata.work_name = "Real Project"
    doc = DocumentWorkflowEngine.transition_to(doc, DocumentStatus.PRINT_READY)
    assert doc.status == DocumentStatus.PRINT_READY

def test_can_transition(sample_doc):
    assert DocumentWorkflowEngine.can_transition(sample_doc, DocumentStatus.PARSED) is True
    assert DocumentWorkflowEngine.can_transition(sample_doc, DocumentStatus.CALCULATED) is False
