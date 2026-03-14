import "./globals.css";
import type { Metadata } from "next";
import ClientShell from "../components/ClientShell";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "CDSS Ward",
  description: "Offline-ready clinical decision support pathway for chest pain.",
  manifest: "/manifest.json",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ClientShell>{children}</ClientShell>
      </body>
    </html>
  );
}
