/**
 * Reusable Button component.
 */

export default function Button({ variant = 'primary', children, className = '', ...props }) {
  const variants = {
    primary: 'btn btn-primary',
    secondary: 'btn btn-secondary',
    outline: 'btn btn-outline',
  };
  
  return (
    <button className={`${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
