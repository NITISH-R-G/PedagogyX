import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import SchoolOverview from './SchoolOverview'

describe('SchoolOverview', () => {
  it('renders school ID and connected status when apiOk is true', () => {
    render(<SchoolOverview schoolId="DPS-DELHI-01" apiOk={true} />)

    expect(screen.getByText(/School:/i)).toBeInTheDocument()
    expect(screen.getByText('DPS-DELHI-01')).toBeInTheDocument()

    const statusElement = screen.getByText('connected')
    expect(statusElement).toBeInTheDocument()
    expect(statusElement).toHaveClass('text-emerald-600')
    expect(statusElement).not.toHaveClass('text-rose-600')
  })

  it('renders school ID and offline status when apiOk is false', () => {
    render(<SchoolOverview schoolId="KV-MUMBAI-02" apiOk={false} />)

    expect(screen.getByText(/School:/i)).toBeInTheDocument()
    expect(screen.getByText('KV-MUMBAI-02')).toBeInTheDocument()

    const statusElement = screen.getByText('offline')
    expect(statusElement).toBeInTheDocument()
    expect(statusElement).toHaveClass('text-rose-600')
    expect(statusElement).not.toHaveClass('text-emerald-600')
  })
})
