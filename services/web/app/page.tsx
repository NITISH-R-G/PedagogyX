const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";
const DEFAULT_SCHOOL = process.env.NEXT_PUBLIC_SCHOOL_ID ?? "pilot-school-dev";

type Overview = {
  school_id: string;
  m_a_coverage?: { rooms_observed: number; rooms_target: number; coverage_pct: number };
  m_b_median_insight_sec?: number | null;
  sessions_week?: number;
  recent_sessions?: Array<{
    id: string;
    room_id?: string;
    teacher_id?: string;
    status: string;
    teacher_talk_ratio?: number;
    insight_latency_sec?: number;
  }>;
  error?: string;
};

async function fetchOverview(schoolId: string): Promise<Overview> {
  try {
    const res = await fetch(`${API_URL}/v1/schools/${schoolId}/overview`, {
      cache: "no-store",
    });
    if (!res.ok) return { school_id: schoolId, error: `API ${res.status}` };
    return await res.json();
  } catch (e) {
    return { school_id: schoolId, error: e instanceof Error ? e.message : "unreachable" };
  }
}

async function fetchHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/health`, { cache: "no-store" });
    const data = await res.json();
    return data.status === "ok";
  } catch {
    return false;
  }
}

function pct(n: number | undefined) {
  if (n == null) return "—";
  return `${Math.round(n * 100)}%`;
}

export default async function HomePage() {
  const apiOk = await fetchHealth();
  const overview = await fetchOverview(DEFAULT_SCHOOL);
  const mA = overview.m_a_coverage;
  const mB = overview.m_b_median_insight_sec;

  return (
    <main>
      <h1>PedagogyX Admin</h1>
      <p style={{ color: "#555" }}>
        School: <strong>{DEFAULT_SCHOOL}</strong> · API{" "}
        <span style={{ color: apiOk ? "green" : "crimson" }}>{apiOk ? "connected" : "offline"}</span>
      </p>

      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginTop: "1.5rem" }}>
        <section style={cardStyle}>
          <h2 style={h2}>M-A · Observation coverage</h2>
          {mA ? (
            <>
              <p style={big}>
                {mA.rooms_observed} / {mA.rooms_target} rooms
              </p>
              <p>{mA.coverage_pct}% this week (target)</p>
              <div style={barTrack}>
                <div style={{ ...barFill, width: `${Math.min(100, mA.coverage_pct)}%` }} />
              </div>
            </>
          ) : (
            <p>{overview.error ?? "No data"}</p>
          )}
        </section>

        <section style={cardStyle}>
          <h2 style={h2}>M-B · Time to insight</h2>
          <p style={big}>{mB != null ? `${Math.round(mB)} sec` : "—"}</p>
          <p style={{ fontSize: "0.85rem", color: "#666" }}>Median preview latency (target &lt; 30 min)</p>
        </section>

        <section style={cardStyle}>
          <h2 style={h2}>Sessions (7d)</h2>
          <p style={big}>{overview.sessions_week ?? 0}</p>
        </section>
      </div>

      <section style={{ ...cardStyle, marginTop: "1.5rem", maxWidth: 900 }}>
        <h2 style={h2}>Recent sessions</h2>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
          <thead>
            <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
              <th style={th}>Room</th>
              <th style={th}>Teacher</th>
              <th style={th}>Status</th>
              <th style={th}>Talk ratio (T)</th>
              <th style={th}>Insight (s)</th>
            </tr>
          </thead>
          <tbody>
            {(overview.recent_sessions ?? []).map((s) => (
              <tr key={String(s.id)} style={{ borderBottom: "1px solid #eee" }}>
                <td style={td}>{s.room_id ?? "—"}</td>
                <td style={td}>{s.teacher_id ?? "—"}</td>
                <td style={td}>{s.status}</td>
                <td style={td}>{pct(s.teacher_talk_ratio)}</td>
                <td style={td}>
                  {s.insight_latency_sec != null ? Math.round(s.insight_latency_sec) : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!overview.recent_sessions?.length && (
          <p style={{ marginTop: "1rem", color: "#666" }}>
            Run <code>make mock-capture</code> after <code>make dev-up</code> to seed data.
          </p>
        )}
      </section>
    </main>
  );
}

const cardStyle: React.CSSProperties = {
  flex: "1 1 220px",
  padding: "1rem",
  border: "1px solid #ccc",
  borderRadius: 8,
  minWidth: 220,
};
const h2: React.CSSProperties = { marginTop: 0, fontSize: "1rem" };
const big: React.CSSProperties = { fontSize: "1.75rem", margin: "0.25rem 0", fontWeight: 600 };
const barTrack: React.CSSProperties = {
  height: 8,
  background: "#eee",
  borderRadius: 4,
  marginTop: 8,
  overflow: "hidden",
};
const barFill: React.CSSProperties = { height: "100%", background: "#2563eb" };
const th: React.CSSProperties = { padding: "0.5rem 0.25rem" };
const td: React.CSSProperties = { padding: "0.5rem 0.25rem" };
