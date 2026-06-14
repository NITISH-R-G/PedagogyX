import { Overview } from "../lib/api";

type RecentSessionsTableProps = {
  recentSessions: Overview["recent_sessions"];
};

function pct(n: number | undefined) {
  if (n == null) return "—";
  return `${Math.round(n * 100)}%`;
}

export default function RecentSessionsTable({
  recentSessions,
}: RecentSessionsTableProps) {
  return (
    <section className="mt-10 p-6 bg-white border border-gray-200 rounded-xl shadow-sm">
      <h2 className="text-lg font-semibold text-gray-900 mb-6">
        Recent sessions
      </h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50/50">
              <th className="px-4 py-3 font-medium text-gray-600 rounded-tl-lg">
                Room
              </th>
              <th className="px-4 py-3 font-medium text-gray-600">Teacher</th>
              <th className="px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="px-4 py-3 font-medium text-gray-600">
                Talk ratio (T)
              </th>
              <th className="px-4 py-3 font-medium text-gray-600 rounded-tr-lg">
                Insight (s)
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {(recentSessions ?? []).map((s) => (
              <tr
                key={String(s.id)}
                className="hover:bg-gray-50/80 transition-colors"
              >
                <td className="px-4 py-4 text-gray-900 font-medium">
                  {s.room_id ?? "—"}
                </td>
                <td className="px-4 py-4 text-gray-600">
                  {s.teacher_id ?? "—"}
                </td>
                <td className="px-4 py-4">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize
                    ${
                      s.status === "completed"
                        ? "bg-emerald-100 text-emerald-800"
                        : s.status === "processing"
                          ? "bg-amber-100 text-amber-800"
                          : s.status === "failed"
                            ? "bg-rose-100 text-rose-800"
                            : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {s.status}
                  </span>
                </td>
                <td className="px-4 py-4 text-gray-900 font-medium">
                  {pct(s.teacher_talk_ratio)}
                </td>
                <td className="px-4 py-4 text-gray-600">
                  {s.insight_latency_sec != null
                    ? Math.round(s.insight_latency_sec)
                    : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {!recentSessions?.length && (
        <div className="mt-8 text-center p-8 bg-gray-50 rounded-lg border border-dashed border-gray-200">
          <p className="text-gray-500 mb-2">No recent sessions found.</p>
          <p className="text-sm text-gray-400">
            Run{" "}
            <code className="px-1.5 py-0.5 bg-gray-100 rounded text-gray-600 font-mono text-xs">
              make mock-capture
            </code>{" "}
            after{" "}
            <code className="px-1.5 py-0.5 bg-gray-100 rounded text-gray-600 font-mono text-xs">
              make dev-up
            </code>{" "}
            to seed data.
          </p>
        </div>
      )}
    </section>
  );
}
