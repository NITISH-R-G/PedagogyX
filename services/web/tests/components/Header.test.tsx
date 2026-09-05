import { render, screen } from "@testing-library/react";
import Header from "../../components/Header";

describe("Header component", () => {
  it("renders header title and navigation links correctly", () => {
    render(<Header />);

    // Header title
    expect(
      screen.getByRole("heading", { level: 1, name: "PedagogyX Admin" })
    ).toBeInTheDocument();

    // Navigation links
    const navLinks = ["Dashboard", "Teachers", "Recordings", "Analytics", "Settings"];
    navLinks.forEach((linkText) => {
      expect(screen.getByRole("link", { name: linkText })).toBeInTheDocument();
    });
  });
});
