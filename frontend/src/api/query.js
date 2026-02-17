/**
 * RAG query API functions.
 */

import client from './client';

export const askQuestion = async (question, topK = 5) => {
  const response = await client.post('/api/query', {
    question,
    top_k: topK,
  });
  return response.data;
};
