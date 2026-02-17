/**
 * Login page component.
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { login as apiLogin } from '../api/auth';
import Input from '../components/Input';
import Button from '../components/Button';
import Alert from '../components/Alert';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await apiLogin(username, password);
      if (response.success && response.user) {
        login(response.user);
        navigate('/chat');
      } else {
        setError(response.message || 'Invalid credentials');
        setLoading(false);
      }
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Request timeout. Please check if the backend server is running.');
      } else if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
        setError('Cannot connect to server. Please ensure the backend is running on http://localhost:8000');
      } else {
        setError(err.response?.data?.detail || 'Authentication failed. Please try again.');
      }
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg-page flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="card">
          <h1 className="text-3xl font-bold text-center mb-2">ICC Knowledge Assistant</h1>
          <p className="text-text-secondary text-center mb-6">
            Sign in to access the knowledge base
          </p>

          {error && (
            <Alert type="error" className="mb-4">
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
            />
            
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />

            <Button
              type="submit"
              variant="primary"
              className="w-full"
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
