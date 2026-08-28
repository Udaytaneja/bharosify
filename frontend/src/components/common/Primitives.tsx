import React from 'react';

// Card Primitive - Stitch specifications: white bg, 1px #E2E8F0 border, 12px radius
export const Card: React.FC<{
  children: React.ReactNode;
  className?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
}> = ({ children, className = '', header, footer }) => {
  return (
    <div className={`bg-surface border border-border-subtle rounded-xl overflow-hidden shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] ${className}`}>
      {header && (
        <div className="px-6 py-4 border-b border-border-subtle bg-surface flex items-center justify-between">
          {header}
        </div>
      )}
      <div className="p-6">{children}</div>
      {footer && (
        <div className="px-6 py-3 border-t border-border-subtle bg-surface-muted/50 text-xs text-on-surface-variant flex items-center justify-between">
          {footer}
        </div>
      )}
    </div>
  );
};

// Button Primitive - Stitch specifications: 6px radius, Primary #2563EB / #0051D5, Secondary white + border
export const Button: React.FC<{
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  icon?: React.ReactNode;
}> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  className = '',
  type = 'button',
  disabled = false,
  icon
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed';
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-xs gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-5 py-2.5 text-base gap-2'
  }[size];

  const variantClasses = {
    primary: 'bg-[#2563EB] hover:bg-[#1d4ed8] text-white font-medium shadow-xs',
    secondary: 'bg-white hover:bg-surface-muted border border-border-subtle text-[#0F172A]',
    ghost: 'bg-transparent hover:bg-surface-muted/60 text-[#2563EB]',
    danger: 'bg-danger hover:bg-red-600 text-white'
  }[variant];

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${sizeClasses} ${variantClasses} ${className}`}
    >
      {icon && <span>{icon}</span>}
      {children}
    </button>
  );
};

// Badge Primitive
export const Badge: React.FC<{
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
  size?: 'sm' | 'md';
  className?: string;
}> = ({ children, variant = 'neutral', size = 'md', className = '' }) => {
  const variantClasses = {
    success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    danger: 'bg-rose-50 text-rose-700 border-rose-200',
    info: 'bg-blue-50 text-blue-700 border-blue-200',
    neutral: 'bg-slate-100 text-slate-700 border-slate-200'
  }[variant];

  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs';

  return (
    <span className={`inline-flex items-center gap-1 rounded-full font-medium border ${sizeClasses} ${variantClasses} ${className}`}>
      {children}
    </span>
  );
};

// AI Insight Container - Stitch specification: subtle #F1F5F9 box to distinguish AI outputs
export const AIInsight: React.FC<{
  title?: string;
  confidence?: number;
  modelName?: string;
  children: React.ReactNode;
  auditTrailId?: string;
  className?: string;
}> = ({
  title = "AI Governance Insight",
  confidence = 98.4,
  modelName = "AgentTrust V4-Enterprise",
  children,
  auditTrailId,
  className = ""
}) => {
  return (
    <div className={`bg-surface-muted/80 border border-border-subtle rounded-xl p-4 space-y-3 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-base text-secondary">auto_awesome</span>
          <span className="font-semibold text-xs uppercase tracking-wider text-on-surface-variant">{title}</span>
          <VerificationIndicator />
        </div>
        <div className="flex items-center gap-3 text-xs text-on-surface-variant">
          <span>{modelName}</span>
          <span className="bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded text-[11px] tnum">
            {confidence}% Confidence
          </span>
        </div>
      </div>
      <div className="text-sm text-on-surface leading-relaxed">
        {children}
      </div>
      {auditTrailId && (
        <div className="pt-2 border-t border-border-subtle flex items-center justify-between text-xs text-on-surface-variant">
          <span className="font-mono text-[11px]">Audit ID: {auditTrailId}</span>
          <a href="#audit" className="text-secondary font-medium hover:underline inline-flex items-center gap-1">
            View Immutable Proof <span className="material-symbols-outlined text-xs">arrow_forward</span>
          </a>
        </div>
      )}
    </div>
  );
};

// Verification Indicator - 16px green badge with check icon
export const VerificationIndicator: React.FC<{ label?: string }> = ({ label = "Verified" }) => {
  return (
    <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
      {label}
    </span>
  );
};

// Audit Trail Link
export const AuditTrailLink: React.FC<{ hash: string; label?: string }> = ({ hash, label = "Audit Hash" }) => {
  return (
    <span className="inline-flex items-center gap-1 text-xs font-mono text-on-surface-variant bg-surface border border-border-subtle px-2 py-1 rounded hover:border-secondary cursor-pointer transition-colors">
      <span className="material-symbols-outlined text-xs text-secondary">verified_user</span>
      <span>{label}: {hash}</span>
    </span>
  );
};
