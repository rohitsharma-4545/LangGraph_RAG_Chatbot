import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const token = req.headers.get("authorization");

  const formData = await req.formData();

  const backendRes = await fetch(`${process.env.BACKEND_URL}/admin/upload`, {
    method: "POST",
    headers: {
      Authorization: token || "",
    },
    body: formData,
  });

  const text = await backendRes.text();

  return new Response(text, {
    status: backendRes.status,
  });
}
