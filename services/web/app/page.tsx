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
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between shadow-sm">
        <h1 className="text-xl font-bold text-gray-900">PedagogyX Admin</h1>
        <nav className="flex space-x-6 text-sm font-medium text-gray-600">
          <a href="#" className="text-blue-600 font-semibold border-b-2 border-blue-600 pb-1">Dashboard</a>
          <a href="#" className="hover:text-gray-900 transition-colors">Teachers</a>
          <a href="#" className="hover:text-gray-900 transition-colors">Recordings</a>
          <a href="#" className="hover:text-gray-900 transition-colors">Analytics</a>
          <a href="#" className="hover:text-gray-900 transition-colors">Settings</a>
        </nav>
      </header>

      <main className="p-8 max-w-7xl mx-auto w-full flex-grow">
        <div className="mb-8">
          <p className="text-gray-600 text-sm">
            School: <strong className="text-gray-900">{DEFAULT_SCHOOL}</strong> <span className="mx-2 text-gray-300">|</span> API{" "}
            <span className={`font-medium ${apiOk ? "text-emerald-600" : "text-rose-600"}`}>
              {apiOk ? "connected" : "offline"}
            </span>
          </p>
        </div>

        <div className="flex flex-wrap gap-6 mt-6">
          <section className="flex-1 min-w-[220px] p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">M-A · Observation coverage</h2>
            {mA ? (
              <>
                <p className="text-3xl font-bold text-gray-900 my-2">
                  {mA.rooms_observed} / {mA.rooms_target} <span className="text-lg text-gray-500 font-medium">rooms</span>
                </p>
                <p className="text-sm text-gray-600">{mA.coverage_pct}% this week (target)</p>
                <div className="h-2 bg-gray-100 rounded-full mt-4 overflow-hidden">
                  <div className="h-full bg-blue-600 transition-all duration-500 ease-out" style={{ width: `${Math.min(100, mA.coverage_pct)}%` }} />
                </div>
              </>
            ) : (
              <p className="text-gray-500 mt-4">{overview.error ?? "No data"}</p>
            )}
          </section>

          <section className="flex-1 min-w-[220px] p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">M-B · Time to insight</h2>
            <p className="text-3xl font-bold text-gray-900 my-2">{mB != null ? `${Math.round(mB)} sec` : "—"}</p>
            <p className="text-sm text-gray-500 mt-4">Median preview latency (target &lt; 30 min)</p>
          </section>

          <section className="flex-1 min-w-[220px] p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Sessions (7d)</h2>
            <p className="text-3xl font-bold text-gray-900 my-2">{overview.sessions_week ?? 0}</p>
          </section>
        </div>

        <section className="mt-10 p-6 bg-white border border-gray-200 rounded-xl shadow-sm">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Recent sessions</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50/50">
                  <th className="px-4 py-3 font-medium text-gray-600 rounded-tl-lg">Room</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Teacher</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Status</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Talk ratio (T)</th>
                  <th className="px-4 py-3 font-medium text-gray-600 rounded-tr-lg">Insight (s)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {(overview.recent_sessions ?? []).map((s) => (
                  <tr key={String(s.id)} className="hover:bg-gray-50/80 transition-colors">
                    <td className="px-4 py-4 text-gray-900 font-medium">{s.room_id ?? "—"}</td>
                    <td className="px-4 py-4 text-gray-600">{s.teacher_id ?? "—"}</td>
                    <td className="px-4 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize
                        ${s.status === 'completed' ? 'bg-emerald-100 text-emerald-800' :
                          s.status === 'processing' ? 'bg-amber-100 text-amber-800' :
                          s.status === 'failed' ? 'bg-rose-100 text-rose-800' :
                          'bg-gray-100 text-gray-800'}`}>
                        {s.status}
                      </span>
                    </td>
                    <td className="px-4 py-4 text-gray-900 font-medium">{pct(s.teacher_talk_ratio)}</td>
                    <td className="px-4 py-4 text-gray-600">
                      {s.insight_latency_sec != null ? Math.round(s.insight_latency_sec) : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {!overview.recent_sessions?.length && (
            <div className="mt-8 text-center p-8 bg-gray-50 rounded-lg border border-dashed border-gray-200">
              <p className="text-gray-500 mb-2">No recent sessions found.</p>
              <p className="text-sm text-gray-400">
                Run <code className="px-1.5 py-0.5 bg-gray-100 rounded text-gray-600 font-mono text-xs">make mock-capture</code> after <code className="px-1.5 py-0.5 bg-gray-100 rounded text-gray-600 font-mono text-xs">make dev-up</code> to seed data.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
