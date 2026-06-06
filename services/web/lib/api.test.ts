import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchOverview, fetchHealth } from './api';

describe('fetchOverview', () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.clearAllMocks();
  });

  it('should return error object when fetch throws an error', async () => {
    const mockError = new Error('Network failure');
    (global.fetch as any).mockRejectedValue(mockError);

    const result = await fetchOverview('test-school');

    expect(result).toEqual({
      school_id: 'test-school',
      error: 'Network failure'
    });
  });

  it('should return fallback error when fetch throws a non-Error', async () => {
    (global.fetch as any).mockRejectedValue('String error');

    const result = await fetchOverview('test-school');

    expect(result).toEqual({
      school_id: 'test-school',
      error: 'unreachable'
    });
  });

  it('should return error object when fetch returns non-ok status', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 500
    });

    const result = await fetchOverview('test-school');

    expect(result).toEqual({
      school_id: 'test-school',
      error: 'API 500'
    });
  });

  it('should return parsed data when fetch is successful', async () => {
    const mockData = {
      school_id: 'test-school',
      sessions_week: 10
    };
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    });

    const result = await fetchOverview('test-school');

    expect(result).toEqual(mockData);
  });
});


describe('fetchHealth', () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.clearAllMocks();
  });

  it('should return true when API returns status "ok"', async () => {
    (global.fetch as any).mockResolvedValue({
      json: () => Promise.resolve({ status: 'ok' })
    });

    const result = await fetchHealth();

    expect(result).toBe(true);
  });

  it('should return false when API returns a status other than "ok"', async () => {
    (global.fetch as any).mockResolvedValue({
      json: () => Promise.resolve({ status: 'error' })
    });

    const result = await fetchHealth();

    expect(result).toBe(false);
  });

  it('should return false when fetch throws an error', async () => {
    const mockError = new Error('Network failure');
    (global.fetch as any).mockRejectedValue(mockError);

    const result = await fetchHealth();

    expect(result).toBe(false);
  });
});
