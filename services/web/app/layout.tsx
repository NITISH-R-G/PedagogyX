import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "PedagogyX Admin",
  description: "Teacher pedagogy monitoring (boilerplate)",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: "2rem", lineHeight: 1.5 }}>
        {children}
      </body>
    </html>
  );
}
