import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchOverview } from './api';

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

  it('should return "unreachable" error when fetch throws a non-Error object', async () => {
    (global.fetch as any).mockRejectedValue('String error');

    const result = await fetchOverview('test-school');

    expect(result).toEqual({
      school_id: 'test-school',
      error: 'unreachable'
    });
  });
});
