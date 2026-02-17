/**
 * 404 Not Found page.
 */

import { Link } from 'react-router-dom';
import Button from '../components/Button';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-bg-page flex items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-text-primary mb-4">404</h1>
        <p className="text-xl text-text-secondary mb-6">Page not found</p>
        <Link to="/chat">
          <Button variant="primary">Return to Chat</Button>
        </Link>
      </div>
    </div>
  );
}
