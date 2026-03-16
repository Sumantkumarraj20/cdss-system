import "./globals.css";
import type { Metadata } from "next";
import ClientShell from "../components/ClientShell";
import { isAuthenticated } from "@/lib/auth";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "CDSS Ward",
  description:
    "Offline-ready clinical decision support pathway for chest pain.",
  manifest: "/manifest.json",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const authenticated = await isAuthenticated();

  return (
    <html lang="en">
      <body>
        <ClientShell authenticated={authenticated}>{children}</ClientShell>
      </body>
    </html>
  );
}
