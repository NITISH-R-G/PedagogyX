import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { fetchOverview, fetchHealth } from './api'

describe('api.ts', () => {
  const originalFetch = global.fetch

  beforeEach(() => {
    global.fetch = vi.fn()
  })

  afterEach(() => {
    global.fetch = originalFetch
  })

  describe('fetchOverview', () => {
    it('returns data on successful fetch', async () => {
      const mockData = { school_id: 'test-school', sessions_week: 10 }
      vi.mocked(global.fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockData
      } as Response)

      const result = await fetchOverview('test-school')
      expect(result).toEqual(mockData)
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/v1/schools/test-school/overview'), expect.any(Object))
    })

    it('returns an error object when fetch returns a non-ok status', async () => {
      vi.mocked(global.fetch).mockResolvedValueOnce({
        ok: false,
        status: 404
      } as Response)

      const result = await fetchOverview('test-school')
      expect(result).toEqual({ school_id: 'test-school', error: 'API 404' })
    })

    it('returns an error object when fetch throws an error', async () => {
      vi.mocked(global.fetch).mockRejectedValueOnce(new Error('Network failure'))

      const result = await fetchOverview('test-school')
      expect(result).toEqual({ school_id: 'test-school', error: 'Network failure' })
    })

    it('returns "unreachable" error object when fetch throws a non-Error', async () => {
      vi.mocked(global.fetch).mockRejectedValueOnce('Some string error')

      const result = await fetchOverview('test-school')
      expect(result).toEqual({ school_id: 'test-school', error: 'unreachable' })
    })
  })

  describe('fetchHealth', () => {
    it('returns true when health check is ok', async () => {
      vi.mocked(global.fetch).mockResolvedValueOnce({
        json: async () => ({ status: 'ok' })
      } as Response)

      const result = await fetchHealth()
      expect(result).toBe(true)
    })

    it('returns false when health check status is not ok', async () => {
      vi.mocked(global.fetch).mockResolvedValueOnce({
        json: async () => ({ status: 'error' })
      } as Response)

      const result = await fetchHealth()
      expect(result).toBe(false)
    })

    it('returns false when health check throws', async () => {
      vi.mocked(global.fetch).mockRejectedValueOnce(new Error('Failed'))

      const result = await fetchHealth()
      expect(result).toBe(false)
    })
  })
})
