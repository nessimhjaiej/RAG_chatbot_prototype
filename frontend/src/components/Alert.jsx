/**
 * Alert component for status messages.
 */

export default function Alert({ type = 'info', children, className = '' }) {
  const types = {
    success: 'bg-green-50 border-success text-green-800',
    error: 'bg-red-50 border-error text-red-800',
    warning: 'bg-amber-50 border-warning text-amber-800',
    info: 'bg-cyan-50 border-info text-cyan-800',
  };
  
  return (
    <div className={`border rounded-md p-4 ${types[type]} ${className}`}>
      {children}
    </div>
  );
}
