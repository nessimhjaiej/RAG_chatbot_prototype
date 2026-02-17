/**
 * Header component with user info and logout.
 */

import { useAuth } from '../context/AuthContext';
import { logout as apiLogout } from '../api/auth';

export default function Header() {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await apiLogout();
      logout();
    } catch (error) {
      console.error('Logout error:', error);
      logout(); // Logout locally even if API call fails
    }
  };

  return (
    <header className="sticky top-0 z-20 bg-bg-surface border-b border-border backdrop-blur-md bg-opacity-90">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-text-primary mb-0">ICC Knowledge Assistant</h1>
        <div className="flex items-center gap-4">
          {user && (
            <>
              <span className="text-text-secondary text-sm">
                {user.username} ({user.role})
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-text-secondary hover:text-text-primary transition-colors"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
