/**
 * Reusable Card component.
 */

export default function Card({ title, children, className = '', ...props }) {
  return (
    <div className={`card ${className}`} {...props}>
      {title && <h3 className="text-lg font-semibold mb-4 text-text-primary">{title}</h3>}
      {children}
    </div>
  );
}
