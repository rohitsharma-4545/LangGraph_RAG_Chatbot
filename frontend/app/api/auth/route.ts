import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();

  const res = await fetch(`${process.env.BACKEND_URL}/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "test",
      role: body.role,
      password: body.password || null,
    }),
  });

  const data = await res.json();
  return NextResponse.json(data);
}
