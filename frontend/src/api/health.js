/**
 * Health check API functions.
 */

import client from './client';

export const getSystemHealth = async () => {
  const response = await client.get('/api/health');
  return response.data;
};
