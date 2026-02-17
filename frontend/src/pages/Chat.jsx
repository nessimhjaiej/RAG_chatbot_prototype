/**
 * Main Chat page for RAG queries.
 */

import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { askQuestion } from '../api/query';
import Button from '../components/Button';
import Alert from '../components/Alert';
import LoadingSpinner from '../components/LoadingSpinner';
import SourcePassage from '../components/SourcePassage';

export default function Chat() {
  const { user } = useAuth();
  const [question, setQuestion] = useState('');
  const [topK, setTopK] = useState(5);
  const [answer, setAnswer] = useState('');
  const [contexts, setContexts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mode, setMode] = useState('AI Chat');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setError('');
    setLoading(true);
    setAnswer('');
    setContexts([]);

    try {
      const response = await askQuestion(question, topK);
      setAnswer(response.answer);
      setContexts(response.contexts);
      
      // Show AI Agent placeholder for admin in agent mode
      if (mode === 'AI Agent' && user?.role === 'admin') {
        // Placeholder for future AI Agent functionality
        console.log('AI Agent mode active');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="mb-2">ICC Knowledge Assistant</h1>
      <p className="text-text-secondary mb-6">
        Ask a question about ICC policy documents. Answers are grounded in retrieved passages from the Chroma vector store.
      </p>

      {/* Admin mode selector */}
      {user?.role === 'admin' && (
        <div className="mb-6">
          <label className="label">Select Mode</label>
          <select
            className="input"
            value={mode}
            onChange={(e) => setMode(e.target.value)}
          >
            <option value="AI Chat">AI Chat</option>
            <option value="AI Agent">AI Agent</option>
          </select>
        </div>
      )}

      {error && (
        <Alert type="error" className="mb-4">
          {error}
        </Alert>
      )}

      {mode === 'AI Agent' && user?.role === 'admin' && answer && (
        <Alert type="info" className="mb-4">
          🤖 AI Agent Mode: Enhanced processing with autonomous capabilities (placeholder).
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="mb-8">
        <label className="label">Your question</label>
        <textarea
          className="input mb-4"
          rows="4"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What are the ICC membership criteria?"
        />

        <div className="mb-4">
          <label className="label">
            Passages to retrieve: {topK}
          </label>
          <input
            type="range"
            min="1"
            max="10"
            value={topK}
            onChange={(e) => setTopK(parseInt(e.target.value))}
            className="w-full"
          />
        </div>

        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? 'Getting answer...' : 'Get answer'}
        </Button>
      </form>

      {loading && (
        <div className="my-8">
          <LoadingSpinner size="lg" />
          <p className="text-center text-text-muted mt-4">
            Retrieving passages and generating answer...
          </p>
        </div>
      )}

      {answer && !loading && (
        <>
          <div className="mb-8">
            <h2 className="mt-0 mb-4">Answer</h2>
            <div className="card">
              <p className="text-text-primary mb-0 whitespace-pre-wrap">{answer}</p>
            </div>
          </div>

          <div className="border-t border-border pt-8">
            <h2 className="mt-0 mb-4">Sources</h2>
            {contexts.length > 0 ? (
              <div className="space-y-3">
                {contexts.map((context, index) => (
                  <SourcePassage
                    key={index}
                    passage={context}
                    index={index + 1}
                  />
                ))}
              </div>
            ) : (
              <Alert type="info">
                No supporting passages were found for this question.
              </Alert>
            )}
          </div>
        </>
      )}
    </div>
  );
}
