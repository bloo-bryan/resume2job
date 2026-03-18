const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";
const TIMEOUT_MS = 30_000;

function buildUrl(request: Request, path: string[]): string {
  const { search } = new URL(request.url);
  return `${API_BASE}/api/${path.join("/")}${search}`;
}

function proxyHeaders(resp: Response): HeadersInit {
  return { "content-type": resp.headers.get("content-type") || "application/json" };
}

export async function GET(
  request: Request,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  try {
    const resp = await fetch(buildUrl(request, path), {
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    return new Response(resp.body, { status: resp.status, headers: proxyHeaders(resp) });
  } catch {
    return Response.json({ error: "Backend API is unreachable" }, { status: 502 });
  }
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const contentType = request.headers.get("content-type") || "";
  const body = await request.arrayBuffer();

  try {
    const resp = await fetch(buildUrl(request, path), {
      method: "POST",
      headers: { "content-type": contentType },
      body,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    return new Response(resp.body, { status: resp.status, headers: proxyHeaders(resp) });
  } catch {
    return Response.json({ error: "Backend API is unreachable" }, { status: 502 });
  }
}
