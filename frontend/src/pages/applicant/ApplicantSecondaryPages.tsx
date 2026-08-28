import React from 'react';

export const ApplicantNotificationsPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Notifications & Credit Alerts
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs space-y-3">
      <div className="p-3 bg-blue-50 border border-blue-200 rounded text-xs text-blue-800">
        • Underwriter assigned to your Commercial Line Expansion (APP-8942-NY).
      </div>
      <div className="p-3 bg-emerald-50 border border-emerald-200 rounded text-xs text-emerald-800">
        • 2023 IRS Tax Return document verified by Forensic OCR Engine.
      </div>
    </div>
  </div>
);

export const ApplicantSettingsPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Account & Portal Settings
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs">
      <p className="text-sm text-on-surface-variant">Manage corporate profile, two-factor authentication, and contact preferences.</p>
    </div>
  </div>
);
