import type {
  HealthResponse,
  MatchRequest,
  MatchResult,
  CompareRequest,
  CompareResult,
  ParseResult,
  DocType,
} from "./types";

async function handleResponse<T>(resp: Response): Promise<T> {
  if (!resp.ok) {
    const text = await resp.text().catch(() => "Request failed");
    throw new Error(text || `HTTP ${resp.status}`);
  }
  return resp.json();
}

export async function getHealth(): Promise<HealthResponse> {
  const resp = await fetch("/api/health");
  return handleResponse(resp);
}

export async function matchResume(req: MatchRequest): Promise<MatchResult> {
  const resp = await fetch("/api/match", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  return handleResponse(resp);
}

export async function compareAlgorithms(
  req: CompareRequest
): Promise<CompareResult> {
  const resp = await fetch("/api/match/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  return handleResponse(resp);
}

export async function parseDocument(
  text: string,
  docType: DocType
): Promise<ParseResult> {
  const formData = new FormData();
  formData.append("text", text);
  formData.append("doc_type", docType);
  const resp = await fetch("/api/parse", {
    method: "POST",
    body: formData,
  });
  return handleResponse(resp);
}

export async function parseFile(
  file: File,
  docType: DocType
): Promise<ParseResult> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("doc_type", docType);
  const resp = await fetch("/api/parse", {
    method: "POST",
    body: formData,
  });
  return handleResponse(resp);
}
