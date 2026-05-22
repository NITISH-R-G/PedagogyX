const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

async function fetchHealth(): Promise<{ status?: string; error?: string }> {
  try {
    const res = await fetch(`${API_URL}/health`, { cache: "no-store" });
    if (!res.ok) {
      return { error: `API ${res.status}` };
    }
    return await res.json();
  } catch (e) {
    return { error: e instanceof Error ? e.message : "unreachable" };
  }
}

export default async function HomePage() {
  const health = await fetchHealth();
  const ok = health.status === "ok";

  return (
    <main>
      <h1>PedagogyX Admin</h1>
      <p>Boilerplate shell — wireframes 1–3 in Sprint 03 S03-06.</p>
      <section
        style={{
          marginTop: "1.5rem",
          padding: "1rem",
          border: "1px solid #ccc",
          borderRadius: 8,
          maxWidth: 480,
        }}
      >
        <h2 style={{ marginTop: 0 }}>API health</h2>
        <p>
          <strong>URL:</strong> {API_URL}/health
        </p>
        <p>
          <strong>Status:</strong>{" "}
          <span style={{ color: ok ? "green" : "crimson" }}>{ok ? "ok" : health.error ?? "error"}</span>
        </p>
        {!ok && (
          <p style={{ fontSize: "0.9rem", color: "#555" }}>
            Start stack: <code>docker compose -f infra/compose.dev.yaml up --build</code>
          </p>
        )}
      </section>
      <p style={{ marginTop: "2rem", fontSize: "0.85rem", color: "#666" }}>
        G2 required before real school data. Use synthetic sessions only.
      </p>
    </main>
  );
}
