/**
 * Typed wrapper around the N-ATLAS Civic Evidence backend API.
 * Never place secrets or privileged keys in this browser bundle.
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => response.statusText);
    throw new ApiError(detail || "Request failed", response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.includes("application/json")) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export interface CaseResponse {
  id: string;
  title: string;
  description?: string | null;
  status: string;
  consent_recorded?: boolean;
  created_at?: string;
}

export interface ClaimResponse {
  id: string;
  case_id: string;
  text: string;
  status: string;
  source_segment_id?: string | null;
  confidence?: number | null;
}

export interface GuidanceResponse {
  source_id: string;
  source_title: string;
  title: string;
  section: string;
  excerpt: string;
  url: string;
  jurisdiction: string;
}

export const api = {
  get: <T>(path: string) => apiFetch<T>(path),
  post: <T>(path: string, body: unknown) =>
    apiFetch<T>(path, { method: "POST", body: JSON.stringify(body) }),
  patch: <T>(path: string, body: unknown) =>
    apiFetch<T>(path, { method: "PATCH", body: JSON.stringify(body) }),
};

export const backendApi = {
  listCases: () => api.get<CaseResponse[]>("/api/v1/cases"),
  getCase: (id: string) => api.get<CaseResponse>(`/api/v1/cases/${id}`),
  listClaims: (caseId: string) => api.get<ClaimResponse[]>(`/api/v1/cases/${caseId}/claims`),
  extractClaims: (caseId: string, transcriptId: string) =>
    api.post<ClaimResponse[]>(`/api/v1/cases/${caseId}/claims/extract?transcript_id=${encodeURIComponent(transcriptId)}`, {}),
  searchGuidance: (query: string, jurisdiction?: string) => {
    const params = new URLSearchParams({ q: query });
    if (jurisdiction) params.set("jurisdiction", jurisdiction);
    return api.get<GuidanceResponse[]>(`/api/v1/civic-guidance/search?${params.toString()}`);
  },
};
