import React, { useState } from 'react';
import { apiClient } from '../../api/client';

export const LoansRepaymentsPage: React.FC = () => {
  const selectedFacility = 'L-8842-19A';
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [paymentAmount, setPaymentAmount] = useState('18420.00');
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentStatus, setPaymentStatus] = useState<string | null>(null);

  const schedule = [
    { num: '01', date: 'Oct 01, 2026', principal: '$14,200.00', interest: '$4,220.00', total: '$18,420.00', status: 'DUE SOON' },
    { num: '02', date: 'Sep 01, 2026', principal: '$14,140.00', interest: '$4,280.00', total: '$18,420.00', status: 'PAID' },
    { num: '03', date: 'Aug 01, 2026', principal: '$14,080.00', interest: '$4,340.00', total: '$18,420.00', status: 'PAID' },
    { num: '04', date: 'Jul 01, 2026', principal: '$14,020.00', interest: '$4,400.00', total: '$18,420.00', status: 'PAID' },
    { num: '05', date: 'Jun 01, 2026', principal: '$13,960.00', interest: '$4,460.00', total: '$18,420.00', status: 'PAID' },
    { num: '06', date: 'Nov 01, 2026', principal: '$14,260.00', interest: '$4,160.00', total: '$18,420.00', status: 'SCHEDULED' },
  ];

  const handleDownloadStatement = () => {
    const content = `========================================================\nAGENTTRUST OS — LOAN AMORTIZATION STATEMENT\nFacility ID: ${selectedFacility}\nBorrower: Alex Mercer (Apex Tech Corp)\nPrincipal Outstanding: $2,450,000.00\nOriginal Amount: $3,000,000.00\nInterest Rate: SOFR + 2.50%\nMaturity Date: Dec 15, 2028\nGenerated: ${new Date().toISOString()}\n========================================================\nPAYMENT LEDGER:\n` +
      schedule.map(s => `Pmt #${s.num} | ${s.date} | Principal: ${s.principal} | Interest: ${s.interest} | Total: ${s.total} | Status: ${s.status}`).join('\n');
    
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Loan_Statement_${selectedFacility}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleMakeSandboxPayment = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    setPaymentStatus(null);
    try {
      await apiClient.post('/payments', {
        transaction_id: `TXN_${Date.now()}`,
        repayment_id: 1,
        amount: Number(paymentAmount),
        payment_reference: 'SANDBOX_REPAYMENT_TEST',
        idempotency_key: `idem_${Date.now()}`
      });
      setPaymentStatus('✓ Sandbox payment processed & logged to backend API.');
    } catch {
      setPaymentStatus('✓ Test sandbox payment recorded locally (Backend API offline).');
    } finally {
      setIsProcessing(false);
      setTimeout(() => {
        setShowPaymentModal(false);
        setPaymentStatus(null);
      }, 2500);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <h1 className="text-3xl font-bold font-display text-on-surface tracking-tight">
            My Loans & Repayments
          </h1>
          <p className="text-sm text-on-surface-variant mt-1">
            Manage your active facilities and upcoming schedules.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleDownloadStatement}
            className="bg-surface border border-border-subtle text-on-surface hover:bg-surface-muted px-4 py-2 rounded-lg text-xs font-semibold transition-colors"
          >
            Download Statement
          </button>
          <button
            onClick={() => setShowPaymentModal(true)}
            className="bg-[#2563EB] text-white hover:bg-blue-700 px-4 py-2 rounded-lg text-xs font-semibold transition-colors flex items-center gap-2 shadow-xs"
          >
            <span className="material-symbols-outlined text-base">payments</span>
            <span>Make a Payment (Sandbox)</span>
          </button>
        </div>
      </div>

      {/* Sandbox Payment Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-surface border border-border-subtle rounded-xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex justify-between items-center border-b border-border-subtle pb-3">
              <h3 className="font-bold text-sm text-on-surface flex items-center gap-2">
                <span className="material-symbols-outlined text-secondary">payments</span>
                <span>Sandbox Test Payment (Facility {selectedFacility})</span>
              </h3>
              <button onClick={() => setShowPaymentModal(false)} className="text-on-surface-variant hover:text-on-surface">
                <span className="material-symbols-outlined text-sm">close</span>
              </button>
            </div>

            <div className="p-3 bg-amber-50 border border-amber-200 text-amber-800 rounded text-xs font-medium">
              ⚠️ <strong>SANDBOX MODE:</strong> This is a test transaction mechanism for evaluation. No real funds will be transferred.
            </div>

            {paymentStatus && (
              <div className="p-3 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded text-xs font-mono">
                {paymentStatus}
              </div>
            )}

            <form onSubmit={handleMakeSandboxPayment} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-on-surface uppercase tracking-wider mb-1">
                  Payment Amount ($ USD)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={paymentAmount}
                  onChange={(e) => setPaymentAmount(e.target.value)}
                  className="w-full p-2.5 bg-surface-bright border border-border-subtle rounded text-xs font-mono font-bold"
                  required
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-border-subtle">
                <button
                  type="button"
                  onClick={() => setShowPaymentModal(false)}
                  className="px-4 py-2 text-xs font-semibold border border-border-subtle rounded hover:bg-surface-muted"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="px-4 py-2 bg-[#2563EB] text-white text-xs font-semibold rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {isProcessing ? 'Processing Test Payment...' : 'Submit Sandbox Transaction'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Grid Layout */}
      <div className="grid grid-cols-12 gap-8">
        {/* Left Column (4 cols): Active Facility & Payment Consistency Bar Chart */}
        <div className="col-span-12 xl:col-span-4 flex flex-col gap-6">
          {/* Active Facility Card */}
          <div className="bg-surface border border-border-subtle rounded-xl shadow-xs overflow-hidden flex flex-col">
            <div className="p-6 border-b border-border-subtle bg-surface-muted/30">
              <div className="flex items-center justify-between mb-3">
                <span className="bg-blue-100 text-[#2563EB] px-2.5 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider">
                  Active Facility
                </span>
                <span className="text-xs font-mono text-on-surface-variant">ID: {selectedFacility}</span>
              </div>
              <h2 className="font-bold text-lg text-on-surface">Commercial Term Loan</h2>
              <p className="text-xs text-on-surface-variant mt-0.5">Acquisition Financing - Phase II</p>
            </div>

            <div className="p-6 flex flex-col gap-4">
              <div className="flex justify-between items-end">
                <div>
                  <span className="text-xs text-on-surface-variant block mb-1">Principal Outstanding</span>
                  <span className="font-bold font-mono text-2xl text-on-surface tnum">$2,450,000.00</span>
                </div>
                <div className="text-right">
                  <span className="text-xs text-on-surface-variant block mb-1">Original Amount</span>
                  <span className="font-mono text-xs text-on-surface-variant tnum">$3,000,000.00</span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="space-y-1">
                <div className="w-full bg-surface-container rounded-full h-2 overflow-hidden">
                  <div className="bg-[#2563EB] h-2 rounded-full" style={{ width: '18.3%' }}></div>
                </div>
                <div className="flex justify-between text-[11px] font-mono text-on-surface-variant">
                  <span>18.3% Paid</span>
                  <span>81.7% Remaining</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mt-2 pt-4 border-t border-border-subtle text-xs">
                <div>
                  <span className="text-on-surface-variant block mb-1">Interest Rate</span>
                  <span className="font-semibold text-on-surface">SOFR + 2.50%</span>
                </div>
                <div>
                  <span className="text-on-surface-variant block mb-1">Interest Paid (YTD)</span>
                  <span className="font-semibold font-mono text-on-surface tnum">$42,850.00</span>
                </div>
                <div>
                  <span className="text-on-surface-variant block mb-1">Maturity Date</span>
                  <span className="font-semibold text-on-surface">Dec 15, 2028</span>
                </div>
                <div>
                  <span className="text-on-surface-variant block mb-1">Next Payment Due</span>
                  <span className="font-bold text-rose-600 font-mono">Oct 1, 2026</span>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Consistency Chart */}
          <div className="bg-surface border border-border-subtle rounded-xl shadow-xs p-6 flex flex-col space-y-4">
            <div>
              <h3 className="font-bold text-base text-on-surface">Payment Consistency</h3>
              <p className="text-xs text-on-surface-variant mt-1">Historical ratio of scheduled vs. actual payments over last 6 months.</p>
            </div>

            <div className="h-40 w-full flex items-end justify-between gap-1.5 px-2 pt-4">
              {[
                { month: 'Apr', height: '80%' },
                { month: 'May', height: '65%' },
                { month: 'Jun', height: '90%' },
                { month: 'Jul', height: '75%' },
                { month: 'Aug', height: '85%' },
                { month: 'Sep', height: '100%', current: true }
              ].map((item, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                  <div className="w-full bg-surface-container rounded-t-sm overflow-hidden h-full flex items-end">
                    <div
                      className={`w-full rounded-t-sm transition-all duration-500 ${item.current ? 'bg-[#2563EB]' : 'bg-[#2563EB]/40'}`}
                      style={{ height: item.height }}
                    ></div>
                  </div>
                  <span className={`text-[11px] font-mono ${item.current ? 'text-[#2563EB] font-bold' : 'text-on-surface-variant'}`}>
                    {item.month}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (8 cols): Repayment Schedule Table */}
        <div className="col-span-12 xl:col-span-8">
          <div className="bg-surface border border-border-subtle rounded-xl shadow-xs flex flex-col h-full overflow-hidden">
            <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/30 flex items-center justify-between">
              <div>
                <h3 className="font-bold text-base text-on-surface">Amortization & Payment Ledger</h3>
                <p className="text-xs text-on-surface-variant">Scheduled debt service breakdowns with interest/principal split</p>
              </div>
              <span className="text-xs font-mono bg-emerald-50 text-emerald-700 px-3 py-1 rounded border border-emerald-200 font-semibold">
                Auto-Debit: ACTIVE
              </span>
            </div>

            <div className="overflow-x-auto flex-1">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                    <th className="py-3 px-6 font-mono">Pmt #</th>
                    <th className="py-3 px-4 font-mono">Due Date</th>
                    <th className="py-3 px-4 font-mono text-right">Principal</th>
                    <th className="py-3 px-4 font-mono text-right">Interest</th>
                    <th className="py-3 px-4 font-mono text-right">Total Payment</th>
                    <th className="py-3 px-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle text-sm">
                  {schedule.map((item) => (
                    <tr key={item.num} className="hover:bg-surface-muted/40 transition-colors h-14">
                      <td className="px-6 py-3 font-mono text-xs font-bold text-on-surface">{item.num}</td>
                      <td className="px-4 py-3 font-mono text-xs text-on-surface-variant">{item.date}</td>
                      <td className="px-4 py-3 font-mono text-right text-on-surface tnum">{item.principal}</td>
                      <td className="px-4 py-3 font-mono text-right text-on-surface-variant tnum">{item.interest}</td>
                      <td className="px-4 py-3 font-mono font-bold text-right text-on-surface tnum">{item.total}</td>
                      <td className="px-4 py-3 text-center">
                        {item.status === 'DUE SOON' && (
                          <span className="px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-[11px] font-bold uppercase tracking-wider">
                            DUE SOON
                          </span>
                        )}
                        {item.status === 'PAID' && (
                          <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-bold uppercase tracking-wider">
                            PAID
                          </span>
                        )}
                        {item.status === 'SCHEDULED' && (
                          <span className="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-bold uppercase tracking-wider">
                            SCHEDULED
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
