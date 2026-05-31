const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export type Overview = {
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

export async function fetchOverview(schoolId: string): Promise<Overview> {
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

export async function fetchHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/health`, { cache: "no-store" });
    const data = await res.json();
    return data.status === "ok";
  } catch {
    return false;
  }
}
