/**
 * Metric component for displaying system status.
 */

export default function Metric({ label, value, delta, trend = 'up', className = '' }) {
  const deltaColor = trend === 'up' ? 'text-green-600' : 'text-red-600';
  
  return (
    <div className={`card ${className}`}>
      <p className="text-text-muted text-sm mb-2">{label}</p>
      <p className="text-3xl font-bold text-text-primary mb-2">{value}</p>
      {delta && <p className={`text-sm ${deltaColor}`}>{delta}</p>}
    </div>
  );
}
