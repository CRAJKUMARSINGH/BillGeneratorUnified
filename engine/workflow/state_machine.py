from typing import List, Optional
from datetime import datetime
from engine.models.document_model import UnifiedDocument, DocumentStatus


class WorkflowError(Exception):
    """Raised when a state transition is invalid."""
    pass


class DocumentWorkflowEngine:
    """Manages document state transitions and workflow logic."""

    # Define valid transitions
    VALID_TRANSITIONS = {
        DocumentStatus.UPLOADED: [DocumentStatus.PARSED],
        DocumentStatus.PARSED: [DocumentStatus.INPUT_EDITED, DocumentStatus.CALCULATED],
        DocumentStatus.INPUT_EDITED: [DocumentStatus.CALCULATED],
        DocumentStatus.CALCULATED: [DocumentStatus.FINAL_EDITED, DocumentStatus.PRINT_READY],
        DocumentStatus.FINAL_EDITED: [DocumentStatus.PRINT_READY],
        DocumentStatus.PRINT_READY: [DocumentStatus.EXPORTED],
        DocumentStatus.EXPORTED: []  # Terminal state
    }

    @classmethod
    def validate_next_state(cls, doc: UnifiedDocument, next_status: DocumentStatus) -> List[str]:
        """
        Validate if the document is ready for the next state.
        Returns a list of error messages. Empty list if valid.
        """
        errors = []
        
        # Check transition validity
        if not cls.can_transition(doc, next_status):
            allowed = cls.VALID_TRANSITIONS.get(doc.status, [])
            errors.append(f"Invalid transition from {doc.status.value} to {next_status.value}. Allowed: {[s.value for s in allowed]}")
            return errors

        # State-specific validation rules
        if next_status == DocumentStatus.CALCULATED:
            if not doc.items:
                errors.append("Document must have at least one item to be calculated.")
            if doc.total_amount <= 0:
                # Some documents might have 0 total but usually this is an error in Phase 2
                pass

        if next_status == DocumentStatus.PRINT_READY:
            meta = doc.metadata
            if not meta.work_name or meta.work_name == "Unknown Project":
                errors.append("Work Name is required for Print Ready status.")
            if not meta.bill_no:
                errors.append("Bill Number is required for Print Ready status.")
            if not doc.items:
                errors.append("Document must have items to be Print Ready.")

        return errors

    @classmethod
    def transition_to(cls, doc: UnifiedDocument, next_status: DocumentStatus) -> UnifiedDocument:
        """
        Transition a document to a new status if valid and requirements are met.
        """
        errors = cls.validate_next_state(doc, next_status)
        if errors:
            raise WorkflowError(f"Validation failed for transition to {next_status.value}: {', '.join(errors)}")
            
        current_status = doc.status
        
        # Perform transition
        doc.status = next_status
        doc.metadata.last_modified = datetime.now()
        
        # Record history
        doc.history.append({
            "action": f"Transitioned to {next_status.value}",
            "previous_status": current_status.value,
            "timestamp": datetime.now()
        })
        
        return doc

    @classmethod
    def can_transition(cls, doc: UnifiedDocument, next_status: DocumentStatus) -> bool:
        """Check if a transition is logically allowed in the state machine."""
        return next_status in cls.VALID_TRANSITIONS.get(doc.status, [])
