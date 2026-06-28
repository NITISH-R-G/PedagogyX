import { Overview } from "../lib/api";

type MetricsCardsProps = {
  overview: Overview;
};

export default function MetricsCards({ overview }: MetricsCardsProps) {
  const mA = overview.m_a_coverage;
  const mB = overview.m_b_median_insight_sec;

  return (
    <div className="flex flex-wrap gap-6 mt-6">
      <section className="flex-1 min-w-[220px] p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
          M-A · Observation coverage
        </h2>
        {mA ? (
          <>
            <p className="text-3xl font-bold text-gray-900 my-2">
              {mA.rooms_observed} / {mA.rooms_target}{" "}
              <span className="text-lg text-gray-500 font-medium">rooms</span>
            </p>
            <p className="text-sm text-gray-600">
              {mA.coverage_pct}% this week (target)
            </p>
            <div className="h-2 bg-gray-100 rounded-full mt-4 overflow-hidden">
              <div
                className="h-full bg-blue-600 transition-all duration-500 ease-out"
                style={{ width: `${Math.min(100, mA.coverage_pct)}%` }}
              />
            </div>
          </>
        ) : (
          <p className="text-gray-500 mt-4">{overview.error ?? "No data"}</p>
        )}
      </section>

      <section className="flex-1 min-w-[220px] p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
          M-B · Time to insight
        </h2>
        <p className="text-3xl font-bold text-gray-900 my-2">
          {mB != null ? `${Math.round(mB)} sec` : "—"}
        </p>
        <p className="text-sm text-gray-500 mt-4">
          Median preview latency (target &lt; 30 min)
        </p>
      </section>

      <section className="flex-1 min-w-[220px] p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
          Sessions (7d)
        </h2>
        <p className="text-3xl font-bold text-gray-900 my-2">
          {overview.sessions_week ?? 0}
        </p>
      </section>
    </div>
  );
}
