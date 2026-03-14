import { NextRequest, NextResponse } from "next/server";

export default function proxy(req: NextRequest) {
  const path = req.nextUrl.pathname;
  if (path.startsWith("/admin") && path !== "/admin") {
    const token = req.cookies.get("cdss_access");
    if (!token) {
      const url = req.nextUrl.clone();
      url.pathname = "/admin";
      url.searchParams.set("redirect", path);
      return NextResponse.redirect(url);
    }
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};
