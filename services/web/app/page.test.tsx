import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import Page from "./page";

// Mock the fetch call globally so the async server component can render in testing
global.fetch = vi.fn().mockResolvedValue({
  json: () =>
    Promise.resolve({
      school_id: "pilot-school-dev",
      m_a_coverage: { rooms_observed: 0, rooms_target: 10, coverage_pct: 0 },
      sessions_week: 0,
      recent_sessions: [],
    }),
});

describe("Page", () => {
  it("renders a heading", async () => {
    const Component = await Page();
    render(Component);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("PedagogyX Admin");
  });
});
