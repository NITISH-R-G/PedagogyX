import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchHealth } from './api';

describe('fetchHealth', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('returns true when status is "ok"', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ status: 'ok' }),
    } as Response);

    const result = await fetchHealth();
    expect(result).toBe(true);
    expect(fetch).toHaveBeenCalledWith('http://localhost:8080/health', { cache: 'no-store' });
  });

  it('returns false when status is not "ok"', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      json: async () => ({ status: 'error' }),
    } as Response);

    const result = await fetchHealth();
    expect(result).toBe(false);
  });

  it('returns false when fetch rejects', async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'));

    const result = await fetchHealth();
    expect(result).toBe(false);
  });
});
