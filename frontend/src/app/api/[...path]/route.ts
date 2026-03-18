const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const url = `${API_BASE}/api/${path.join("/")}`;
  const resp = await fetch(url);
  return new Response(resp.body, {
    status: resp.status,
    headers: {
      "content-type": resp.headers.get("content-type") || "application/json",
    },
  });
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const url = `${API_BASE}/api/${path.join("/")}`;
  const contentType = request.headers.get("content-type") || "";

  const body = await request.arrayBuffer();

  const resp = await fetch(url, {
    method: "POST",
    headers: { "content-type": contentType },
    body: body,
  });
  return new Response(resp.body, {
    status: resp.status,
    headers: {
      "content-type": resp.headers.get("content-type") || "application/json",
    },
  });
}
