import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from "@testing-library/react";
import MetricsCards from "../../components/MetricsCards";
import { Overview } from "../../lib/api";

describe("MetricsCards", () => {
  it("renders correctly with complete overview data", () => {
    const mockOverview: Overview = {
      school_id: "test-school",
      m_a_coverage: {
        rooms_observed: 10,
        rooms_target: 20,
        coverage_pct: 50,
      },
      m_b_median_insight_sec: 120.5,
      sessions_week: 42,
    };

    render(<MetricsCards overview={mockOverview} />);

    // M-A section
    expect(screen.getByText("M-A · Observation coverage")).toBeInTheDocument();
    expect(screen.getByText("10 / 20")).toBeInTheDocument();
    expect(screen.getByText("50% this week (target)")).toBeInTheDocument();

    // M-B section
    expect(screen.getByText("M-B · Time to insight")).toBeInTheDocument();
    expect(screen.getByText("121 sec")).toBeInTheDocument(); // 120.5 rounds to 121

    // Sessions section
    expect(screen.getByText("Sessions (7d)")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
  });

  it("renders correctly with missing optional data (falling back to defaults)", () => {
    const mockOverview: Overview = {
      school_id: "test-school",
    };

    render(<MetricsCards overview={mockOverview} />);

    // M-A fallback
    expect(screen.getByText("No data")).toBeInTheDocument();

    // M-B fallback
    expect(screen.getByText("—")).toBeInTheDocument();

    // Sessions fallback
    expect(screen.getByText("0")).toBeInTheDocument();
  });

  it("renders error message in M-A section when error is provided and m_a_coverage is missing", () => {
    const mockOverview: Overview = {
      school_id: "test-school",
      error: "Failed to load observation data",
    };

    render(<MetricsCards overview={mockOverview} />);

    expect(screen.getByText("Failed to load observation data")).toBeInTheDocument();
    expect(screen.queryByText("No data")).not.toBeInTheDocument();
  });
});
