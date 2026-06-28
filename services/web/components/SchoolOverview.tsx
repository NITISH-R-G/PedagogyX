type SchoolOverviewProps = {
  schoolId: string;
  apiOk: boolean;
};

export default function SchoolOverview({
  schoolId,
  apiOk,
}: SchoolOverviewProps) {
  return (
    <div className="mb-8">
      <p className="text-gray-600 text-sm">
        School: <strong className="text-gray-900">{schoolId}</strong>{" "}
        <span className="mx-2 text-gray-300">|</span> API{" "}
        <span
          className={`font-medium ${apiOk ? "text-emerald-600" : "text-rose-600"}`}
        >
          {apiOk ? "connected" : "offline"}
        </span>
      </p>
    </div>
  );
}
