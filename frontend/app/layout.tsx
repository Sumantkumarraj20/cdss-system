import "./globals.css";
import ReactQueryProvider from "@/lib/react-query-provider";
import type { Metadata } from "next";

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
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </body>
    </html>
  );
}
