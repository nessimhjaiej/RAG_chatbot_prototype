/**
 * Sidebar component with system health status.
 */

import { useEffect, useState } from 'react';
import { getSystemHealth } from '../api/health';
import Alert from './Alert';

export default function Sidebar() {
  const [healthStatus, setHealthStatus] = useState({ checks: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHealthStatus();
  }, []);

  const loadHealthStatus = async () => {
    try {
      const data = await getSystemHealth();
      setHealthStatus(data);
    } catch (error) {
      console.error('Error fetching health status:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAlertType = (check) => {
    if (check.includes('MISSING') || check.toLowerCase().includes('error') || 
        check.includes('disconnected') || check.includes('missing')) {
      return 'error';
    }
    return 'success';
  };

  return (
    <aside className="w-64 bg-bg-surface border-r border-border p-6 hidden md:block overflow-y-auto">
      <h2 className="text-lg font-semibold mb-4 text-text-primary mt-0">System Status</h2>
      
      {loading ? (
        <p className="text-text-muted">Loading...</p>
      ) : (
        <div className="space-y-3">
          {healthStatus.checks.map((check, index) => (
            <Alert key={index} type={getAlertType(check)} className="text-xs p-2">
              {check}
            </Alert>
          ))}
        </div>
      )}
      
      <button
        onClick={loadHealthStatus}
        className="mt-4 w-full text-sm text-accent hover:text-indigo-700 transition-colors"
      >
        Refresh Status
      </button>
    </aside>
  );
}
