import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import RecentSessionsTable from "./RecentSessionsTable";

describe("RecentSessionsTable", () => {
  it("renders table headers correctly", () => {
    render(<RecentSessionsTable recentSessions={[]} />);

    expect(
      screen.getByRole("heading", { level: 2, name: /Recent sessions/i }),
    ).toBeInTheDocument();
    expect(screen.getByText("Room")).toBeInTheDocument();
    expect(screen.getByText("Teacher")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Talk ratio (T)")).toBeInTheDocument();
    expect(screen.getByText("Insight (s)")).toBeInTheDocument();
  });

  it("renders empty state when there are no recent sessions", () => {
    const { rerender } = render(<RecentSessionsTable recentSessions={[]} />);
    expect(screen.getByText("No recent sessions found.")).toBeInTheDocument();

    rerender(<RecentSessionsTable recentSessions={undefined} />);
    expect(screen.getByText("No recent sessions found.")).toBeInTheDocument();
  });

  it("renders a list of sessions correctly", () => {
    const mockSessions = [
      {
        id: "1",
        room_id: "Room 101",
        teacher_id: "Teacher A",
        status: "completed",
        teacher_talk_ratio: 0.45,
        insight_latency_sec: 1.2,
      },
      {
        id: "2",
        room_id: "Room 102",
        teacher_id: "Teacher B",
        status: "processing",
        teacher_talk_ratio: 0.6,
        insight_latency_sec: 5.8,
      },
      {
        id: "3",
        room_id: undefined,
        teacher_id: undefined,
        status: "failed",
        teacher_talk_ratio: undefined,
        insight_latency_sec: undefined,
      },
    ];

    render(<RecentSessionsTable recentSessions={mockSessions} />);

    // Table rows shouldn't show the empty state message
    expect(
      screen.queryByText("No recent sessions found."),
    ).not.toBeInTheDocument();

    // Row 1
    expect(screen.getByText("Room 101")).toBeInTheDocument();
    expect(screen.getByText("Teacher A")).toBeInTheDocument();
    expect(screen.getByText("completed")).toBeInTheDocument();
    expect(screen.getByText("45%")).toBeInTheDocument(); // 0.45 * 100
    expect(screen.getByText("1")).toBeInTheDocument(); // Math.round(1.2)

    // Row 2
    expect(screen.getByText("Room 102")).toBeInTheDocument();
    expect(screen.getByText("Teacher B")).toBeInTheDocument();
    expect(screen.getByText("processing")).toBeInTheDocument();
    expect(screen.getByText("60%")).toBeInTheDocument(); // 0.60 * 100
    expect(screen.getByText("6")).toBeInTheDocument(); // Math.round(5.8)

    // Row 3
    expect(screen.getByText("failed")).toBeInTheDocument();

    // Test the "—" empty states. Since there are multiple "—", we can check if they exist
    const emptyPlaceholders = screen.getAllByText("—");
    expect(emptyPlaceholders.length).toBeGreaterThan(0);
  });
});
