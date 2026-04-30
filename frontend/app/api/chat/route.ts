import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const token = req.headers.get("authorization");

  const backendRes = await fetch(`${process.env.BACKEND_URL}/chat/ask-stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: token || "",
    },
    body: JSON.stringify(body),
  });

  if (!backendRes.ok) {
    const text = await backendRes.text();

    return new Response(`data: ERROR: ${text || backendRes.statusText}\n\n`, {
      status: 200,
      headers: { "Content-Type": "text/event-stream" },
    });
  }

  return new Response(backendRes.body, {
    headers: {
      "Content-Type": "text/event-stream",
    },
  });
}
