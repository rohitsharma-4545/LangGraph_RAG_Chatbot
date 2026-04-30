import { NextRequest } from "next/server";

export async function DELETE(req: NextRequest) {
  const token = req.headers.get("authorization");

  const backendRes = await fetch(`${process.env.BACKEND_URL}/admin/delete`, {
    method: "DELETE",
    headers: {
      Authorization: token || "",
    },
  });

  const text = await backendRes.text();

  return new Response(text, {
    status: backendRes.status,
  });
}
