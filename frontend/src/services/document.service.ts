import type { DocumentItem, ExtractedField } from '../types';
import { apiClient } from '../api/client';

export interface DocumentIntelligenceResponse {
  document_type: string;
  fields: Record<string, unknown>;
  confidence: number;
  anomalies: Array<Record<string, unknown>>;
  evidence: string[];
  model_metadata: Record<string, any>;
  layout_regions: Array<{
    element_type: string;
    source_class?: string;
    semantic_class?: string;
    bbox: [number, number, number, number];
    confidence: number;
    page: number;
  }>;
  ocr_lines: Array<{
    text: string;
    confidence: number;
    bbox: [number, number, number, number];
    page: number;
  }>;
  requires_review: boolean;
}

export interface BackendDocumentResponse {
  id: number;
  document_id: string;
  owner_id: number;
  original_filename: string;
  mime_type: string;
  file_size: number;
  document_type: string;
  requirement: string;
  status: string;
  ocr_status: string;
  ai_analysis: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

export class DocumentService {
  static async getDocuments(): Promise<DocumentItem[]> {
    try {
      const response = await apiClient.get<BackendDocumentResponse[]>('/documents');
      if (Array.isArray(response.data)) {
        return response.data.map((doc) => {
          const confidence = doc.ai_analysis?.confidence;
          const ocrScore = confidence ? Math.round(confidence * 1000) / 10 : 99.0;
          return {
            id: doc.document_id,
            name: doc.original_filename,
            type: doc.document_type || 'Uploaded Document',
            requirement: (doc.requirement as any) || 'REQUIRED',
            dateUploaded: doc.created_at
              ? new Date(doc.created_at).toLocaleDateString('en-US', {
                  month: 'short',
                  day: '2-digit',
                  year: 'numeric',
                })
              : 'Recently',
            status: doc.status === 'VERIFIED' ? 'VERIFIED' : 'PROCESSING_OCR',
            ocrScore,
            tamperRisk:
              doc.ai_analysis?.anomalies && doc.ai_analysis.anomalies.length > 0
                ? 'LOW_FLAG'
                : 'NONE',
          };
        });
      }
    } catch (err) {
      console.warn('Real API getDocuments error:', err);
    }
    return [];
  }

  static async analyzeDocument(file: File): Promise<DocumentIntelligenceResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<DocumentIntelligenceResponse>('/ai/document', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  static async uploadDocument(file: File, docType = 'Uploaded Document'): Promise<DocumentItem> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', docType);

    const response = await apiClient.post<BackendDocumentResponse>('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    const doc = response.data;
    const confidence = doc.ai_analysis?.confidence;
    const ocrScore = confidence ? Math.round(confidence * 1000) / 10 : 99.0;

    return {
      id: doc.document_id,
      name: doc.original_filename,
      type: doc.document_type || docType,
      requirement: (doc.requirement as any) || 'REQUIRED',
      dateUploaded: doc.created_at
        ? new Date(doc.created_at).toLocaleDateString('en-US', {
            month: 'short',
            day: '2-digit',
            year: 'numeric',
          })
        : 'Recently',
      status: doc.status === 'VERIFIED' ? 'VERIFIED' : 'PROCESSING_OCR',
      ocrScore,
      tamperRisk:
        doc.ai_analysis?.anomalies && doc.ai_analysis.anomalies.length > 0 ? 'LOW_FLAG' : 'NONE',
    };
  }

  static validatePdfFile(file: File): { valid: boolean; error?: string } {
    if (!file.name.toLowerCase().endsWith('.pdf') && file.type !== 'application/pdf') {
      return { valid: false, error: 'File must be in PDF format (.pdf).' };
    }
    if (file.size > 25 * 1024 * 1024) {
      return { valid: false, error: 'File size exceeds 25MB vault limit.' };
    }
    return { valid: true };
  }

  static async getExtractedFields(): Promise<ExtractedField[]> {
    try {
      const docs = await this.getDocuments();
      if (docs.length > 0) {
        // Extract grounded fields from latest document
        const latestRes = await apiClient.get<BackendDocumentResponse>(`/documents/${docs[0].id}`);
        if (latestRes.data?.ai_analysis?.fields) {
          return Object.entries(latestRes.data.ai_analysis.fields).map(([k, v]) => ({
            fieldKey: k,
            label: k.replace(/_/g, ' ').toUpperCase(),
            extractedValue: String(v),
            confidenceScore: 0.99,
          }));
        }
      }
    } catch {
      // Return empty if no fields grounded
    }
    return [];
  }
}
