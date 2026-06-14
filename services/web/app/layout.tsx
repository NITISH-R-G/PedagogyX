import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "PedagogyX Admin",
  description: "Teacher pedagogy monitoring (boilerplate)",
};

import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-gray-50 text-gray-900">
        {children}
      </body>
    </html>
  );
}
