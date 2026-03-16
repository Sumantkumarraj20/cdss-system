import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = await req.json();

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.json();
    return NextResponse.json(
      { error: error.detail || "Registration failed" },
      { status: 400 },
    );
  }

  const data = await res.json();

  const response = NextResponse.json({ success: true });

  response.cookies.set("cdss_access", data.access_token, {
    httpOnly: true,
    secure: false,
    path: "/",
    maxAge: 60 * 60 * 24,
  });

  return response;
}
