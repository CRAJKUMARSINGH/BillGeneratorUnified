import type { UnifiedDocument } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export async function fetchDocuments(): Promise<UnifiedDocument[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/`);
    if (!response.ok) throw new Error('Failed to fetch documents');
    return await response.ok ? response.json() : [];
  } catch (error) {
    console.error('Error fetching documents:', error);
    return [];
  }
}

export async function transitionDocument(docId: string, targetStatus: string): Promise<UnifiedDocument | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/${docId}/transition?target_status=${targetStatus}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Transition failed');
    return await response.json();
  } catch (error) {
    console.error('Error transitioning document:', error);
    return null;
  }
}
