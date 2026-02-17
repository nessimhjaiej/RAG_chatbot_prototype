/**
 * Reusable Input component with label.
 */

export default function Input({ label, className = '', ...props }) {
  return (
    <div className={className}>
      {label && <label className="label">{label}</label>}
      <input className="input" {...props} />
    </div>
  );
}
