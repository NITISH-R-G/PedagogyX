import { fetchHealth, fetchOverview } from "../lib/api";
import Header from "../components/Header";
import SchoolOverview from "../components/SchoolOverview";
import MetricsCards from "../components/MetricsCards";
import RecentSessionsTable from "../components/RecentSessionsTable";

const DEFAULT_SCHOOL = process.env.NEXT_PUBLIC_SCHOOL_ID ?? "pilot-school-dev";

export default async function HomePage() {
  const apiOk = await fetchHealth();
  const overview = await fetchOverview(DEFAULT_SCHOOL);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />

      <main className="p-8 max-w-7xl mx-auto w-full flex-grow">
        <SchoolOverview schoolId={DEFAULT_SCHOOL} apiOk={apiOk} />
        <MetricsCards overview={overview} />
        <RecentSessionsTable recentSessions={overview.recent_sessions} />
      </main>
    </div>
  );
}
