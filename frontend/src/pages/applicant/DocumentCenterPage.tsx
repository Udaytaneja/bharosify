import React, { useState, useEffect } from 'react';
import { DocumentService } from '../../services/document.service';
import { ApplicationService } from '../../services/application.service';
import type {
  DocumentItem,
  LegalHeir,
  PreviousLoan,
  FullApplicationSubmission
} from '../../types';

export const DocumentCenterPage: React.FC = () => {
  const [activeViewTab, setActiveViewTab] = useState<'vault' | 'apply'>('vault');
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  // Form State for 10-section submission
  const [fullName, setFullName] = useState('Alex Mercer');
  const [fatherName, setFatherName] = useState('Robert Mercer');
  const [maritalStatus, setMaritalStatus] = useState<'Married' | 'Unmarried'>('Married');
  const [spouseName, setSpouseName] = useState('Elena Mercer');
  const [dob, setDob] = useState('1988-04-14');

  const [legalHeirs, setLegalHeirs] = useState<LegalHeir[]>([
    { id: '1', name: 'Julian Mercer', relation: 'Son', address: '100 Financial Plaza, NY', age: 14 }
  ]);

  const [assetsDesc, setAssetsDesc] = useState('Commercial Property (Real Estate), Money Market Fund');
  const [assetsVal, setAssetsVal] = useState('1850000');
  const [liabDesc, setLiabDesc] = useState('Mortgage Balance, Vehicle Financing');
  const [liabVal, setLiabVal] = useState('420000');
  const [financialNotes, setFinancialNotes] = useState('Liquid cash reserves cover 2.10x liabilities.');

  const [previousLoans, setPreviousLoans] = useState<PreviousLoan[]>([
    { id: '1', lenderName: 'Chase Commercial', originalAmount: 500000, outstandingAmount: 120000, status: 'Active', notes: 'Monthly payment $4,200 on time' }
  ]);

  const [guarantorName, setGuarantorName] = useState('Jonathan Mercer');
  const [guarantorRelation, setGuarantorRelation] = useState('Brother / Co-Director');
  const [guarantorNetWorth, setGuarantorNetWorth] = useState('3200000');
  const guaranteeAmount = '500000';
  const liabilityDetails = 'Personal guarantee unconditionally backed by liquid securities.';

  const [highestEducation, setHighestEducation] = useState<'Undergraduate' | 'Postgraduate' | 'Professional' | 'Doctorate' | 'Other'>('Postgraduate');
  const [institutionName, setInstitutionName] = useState('Columbia Business School');
  const [graduationYear, setGraduationYear] = useState('2012');

  const [panFile, setPanFile] = useState<File | null>(null);
  const [aadhaarFile, setAadhaarFile] = useState<File | null>(null);
  const [panError, setPanError] = useState<string | null>(null);
  const [aadhaarError, setAadhaarError] = useState<string | null>(null);

  const [loanAmount, setLoanAmount] = useState('450000');
  const [loanPurpose, setLoanPurpose] = useState<'Social' | 'Medical' | 'Commercial Real Estate' | 'Working Capital' | 'Equipment Financing' | 'Refinance' | 'Other'>('Commercial Real Estate');
  const [loanScheme, setLoanScheme] = useState('Priority Commercial Scheme');

  const [otherInfoToBank, setOtherInfoToBank] = useState('Looking to expand commercial operations in Q4 2026.');

  const [formErrors, setFormErrors] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionSuccess, setSubmissionSuccess] = useState<string | null>(null);

  useEffect(() => {
    DocumentService.getDocuments().then(setDocuments);
  }, []);

  // Handle Legal Heir Add/Remove
  const handleAddLegalHeir = () => {
    setLegalHeirs([
      ...legalHeirs,
      { id: Date.now().toString(), name: '', relation: '', address: '', age: '' }
    ]);
  };

  const handleRemoveLegalHeir = (id: string) => {
    setLegalHeirs(legalHeirs.filter(h => h.id !== id));
  };

  const handleUpdateLegalHeir = (id: string, field: keyof LegalHeir, value: string) => {
    setLegalHeirs(legalHeirs.map(h => (h.id === id ? { ...h, [field]: value } : h)));
  };

  // Handle Previous Loan Add/Remove
  const handleAddPreviousLoan = () => {
    setPreviousLoans([
      ...previousLoans,
      { id: Date.now().toString(), lenderName: '', originalAmount: '', outstandingAmount: '', status: 'Active', notes: '' }
    ]);
  };

  const handleRemovePreviousLoan = (id: string) => {
    setPreviousLoans(previousLoans.filter(l => l.id !== id));
  };

  const handleUpdatePreviousLoan = (id: string, field: keyof PreviousLoan, value: string) => {
    setPreviousLoans(previousLoans.map(l => (l.id === id ? { ...l, [field]: value } : l)));
  };

  // Upload Handlers
  const handlePanSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const validation = DocumentService.validatePdfFile(file);
      if (!validation.valid) {
        setPanError(validation.error || 'Invalid file');
        setPanFile(null);
      } else {
        setPanError(null);
        setPanFile(file);
        setUploading(true);
        setUploadMessage(`Persisting ${file.name} to vault...`);
        try {
          await DocumentService.uploadDocument(file, 'PAN Card PDF');
          const docs = await DocumentService.getDocuments();
          setDocuments(docs);
          setUploadMessage(`PAN Card uploaded & verified successfully!`);
        } catch (err: any) {
          setPanError(err.message || 'Upload failed');
        } finally {
          setUploading(false);
          setTimeout(() => setUploadMessage(null), 4000);
        }
      }
    }
  };

  const handleAadhaarSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const validation = DocumentService.validatePdfFile(file);
      if (!validation.valid) {
        setAadhaarError(validation.error || 'Invalid file');
        setAadhaarFile(null);
      } else {
        setAadhaarError(null);
        setAadhaarFile(file);
        setUploading(true);
        setUploadMessage(`Persisting ${file.name} to vault...`);
        try {
          await DocumentService.uploadDocument(file, 'Aadhaar Card PDF');
          const docs = await DocumentService.getDocuments();
          setDocuments(docs);
          setUploadMessage(`Aadhaar Card uploaded & verified successfully!`);
        } catch (err: any) {
          setAadhaarError(err.message || 'Upload failed');
        } finally {
          setUploading(false);
          setTimeout(() => setUploadMessage(null), 4000);
        }
      }
    }
  };

  const handleSimulatedVaultUpload = async (file: File) => {
    setUploading(true);
    setUploadMessage(`Uploading ${file.name}... Persisting to secure storage...`);

    try {
      await DocumentService.uploadDocument(file, 'Uploaded Document');
      const docs = await DocumentService.getDocuments();
      setDocuments(docs);
      setUploadMessage(`Document "${file.name}" uploaded and persisted successfully!`);
    } catch (err: any) {
      setUploadMessage(`Failed to upload "${file.name}": ${err.message || 'Error'}`);
    } finally {
      setUploading(false);
      setTimeout(() => setUploadMessage(null), 4000);
    }
  };

  const handleVaultFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleSimulatedVaultUpload(e.target.files[0]);
    }
  };

  const handleVaultDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleSimulatedVaultUpload(e.dataTransfer.files[0]);
    }
  };

  // Form Validation & Submission
  const handleSubmitApplication = (e: React.FormEvent) => {
    e.preventDefault();
    const errors: string[] = [];

    if (!fullName.trim()) errors.push('Full Name is required.');
    if (!fatherName.trim()) errors.push("Father's Name is required.");
    if (maritalStatus === 'Married' && !spouseName.trim()) errors.push('Spouse Name is required when married.');
    if (!dob) errors.push('Date of Birth is required.');
    if (!loanAmount || Number(loanAmount) <= 0) errors.push('Valid Loan Amount is required.');

    if (errors.length > 0) {
      setFormErrors(errors);
      return;
    }

    setFormErrors([]);
    setIsSubmitting(true);

    const payload: FullApplicationSubmission = {
      personalDetails: {
        fullName,
        fatherName,
        maritalStatus,
        spouseName: maritalStatus === 'Married' ? spouseName : undefined,
        dob
      },
      legalHeirs,
      financialReport: {
        assetsDescription: assetsDesc,
        totalAssetsValue: assetsVal,
        liabilitiesDescription: liabDesc,
        totalLiabilitiesValue: liabVal,
        otherNotes: financialNotes
      },
      previousLoans,
      guaranteeDetails: {
        guarantorName,
        relation: guarantorRelation,
        netWorth: guarantorNetWorth,
        guaranteeAmount,
        liabilityDetails
      },
      qualification: {
        highestEducation,
        institutionName,
        graduationYear
      },
      identityDocs: {},
      loanRequest: {
        loanAmount,
        purpose: loanPurpose,
        scheme: loanScheme
      },
      otherInfoToBank
    };

    ApplicationService.submitFullApplication(payload).then((newApp) => {
      setIsSubmitting(false);
      setSubmissionSuccess(`Application #${newApp.id} successfully submitted to underwriting queue!`);
      setActiveViewTab('vault');
    });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <h1 className="text-3xl font-bold font-display text-on-surface tracking-tight">
            Document Center & Loan Submission
          </h1>
          <p className="text-sm text-on-surface-variant mt-1">
            Upload financial evidence, manage identity records, and submit comprehensive credit applications.
          </p>
        </div>

        {/* View Switcher Tabs */}
        <div className="bg-surface-muted p-1 rounded-lg border border-border-subtle flex items-center gap-1 text-xs">
          <button
            onClick={() => setActiveViewTab('vault')}
            className={`px-3 py-1.5 rounded-md font-medium transition-all ${
              activeViewTab === 'vault' ? 'bg-surface text-primary shadow-xs font-semibold' : 'text-on-surface-variant hover:text-on-surface'
            }`}
          >
            Document Vault
          </button>
          <button
            onClick={() => setActiveViewTab('apply')}
            className={`px-3 py-1.5 rounded-md font-medium transition-all ${
              activeViewTab === 'apply' ? 'bg-[#2563EB] text-white shadow-xs font-semibold' : 'text-on-surface-variant hover:text-on-surface'
            }`}
          >
            + New Application Form
          </button>
        </div>
      </div>

      {submissionSuccess && (
        <div className="p-4 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-xl text-sm font-semibold flex items-center gap-2">
          <span className="material-symbols-outlined text-base">check_circle</span>
          <span>{submissionSuccess}</span>
        </div>
      )}

      {activeViewTab === 'vault' ? (
        /* Document Vault View */
        <div className="space-y-8">
          {/* Drag & Drop Upload Vault */}
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleVaultDrop}
            className="bg-surface border-2 border-dashed border-border-subtle hover:border-[#2563EB] rounded-xl p-8 text-center transition-colors flex flex-col items-center justify-center space-y-3 cursor-pointer group stroke-dash-6"
          >
            <div className="w-12 h-12 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center group-hover:scale-110 transition-transform">
              <span className="material-symbols-outlined text-2xl">cloud_upload</span>
            </div>
            <div>
              <h3 className="font-bold text-sm text-on-surface">Drag and drop your financial files here</h3>
              <p className="text-xs text-on-surface-variant mt-0.5">Supports PDF, PNG, JPG up to 25MB per file • FIPS 140-3 AES-256 Encrypted Vault</p>
            </div>

            <label className="bg-[#2563EB] text-white hover:bg-blue-700 font-medium text-xs px-4 py-2 rounded-md shadow-xs transition-colors flex items-center gap-2 cursor-pointer mt-2">
              <span className="material-symbols-outlined text-base">upload_file</span>
              <span>Browse File</span>
              <input type="file" onChange={handleVaultFileSelect} className="hidden" accept=".pdf,.png,.jpg,.jpeg" />
            </label>

            {uploading && (
              <div className="flex items-center gap-2 text-xs font-mono text-[#2563EB] bg-blue-50 px-3 py-1.5 rounded-full border border-blue-200">
                <span className="w-2 h-2 rounded-full bg-[#2563EB] animate-ping"></span>
                <span>{uploadMessage}</span>
              </div>
            )}

            {uploadMessage && !uploading && (
              <div className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-200">
                {uploadMessage}
              </div>
            )}
          </div>

          {/* Document List Table */}
          <div className="bg-surface border border-border-subtle rounded-xl overflow-hidden shadow-xs">
            <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/30 flex items-center justify-between">
              <h3 className="font-bold text-base text-on-surface">Required & Uploaded Documents</h3>
              <span className="text-xs font-mono text-on-surface-variant">OCR Engine Status: 99.8% Accuracy</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                    <th className="py-3 px-6">Document Name</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">Requirement</th>
                    <th className="py-3 px-4 font-mono">Date Uploaded</th>
                    <th className="py-3 px-4 text-center">Verification Status</th>
                    <th className="py-3 px-6 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle text-sm">
                  {documents.map((doc) => (
                    <tr key={doc.id} className="hover:bg-surface-muted/40 transition-colors h-14">
                      <td className="px-6 py-3 font-medium text-on-surface flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-blue-50 text-[#2563EB] flex items-center justify-center border border-blue-100">
                          <span className="material-symbols-outlined text-base">description</span>
                        </div>
                        <span>{doc.name}</span>
                      </td>
                      <td className="px-4 py-3 text-xs text-on-surface-variant">{doc.type}</td>
                      <td className="px-4 py-3 text-xs font-mono font-semibold">
                        <span className={doc.requirement === 'REQUIRED' ? 'text-rose-600' : 'text-on-surface-variant'}>
                          {doc.requirement}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-xs text-on-surface-variant">{doc.dateUploaded}</td>
                      <td className="px-4 py-3 text-center">
                        {doc.status === 'VERIFIED' && (
                          <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-bold uppercase tracking-wider">
                            VERIFIED
                          </span>
                        )}
                        {doc.status === 'PROCESSING_OCR' && (
                          <span className="px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-[11px] font-bold uppercase tracking-wider">
                            PROCESSING OCR
                          </span>
                        )}
                        {doc.status === 'NOT UPLOADED' && (
                          <span className="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-bold uppercase tracking-wider">
                            NOT UPLOADED
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-3 text-right">
                        <label className="text-xs text-[#2563EB] hover:underline font-semibold uppercase tracking-wider cursor-pointer">
                          {doc.status === 'NOT UPLOADED' ? 'Upload' : 'Replace'}
                          <input type="file" onChange={handleVaultFileSelect} className="hidden" accept=".pdf,.png,.jpg,.jpeg" />
                        </label>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        /* Structured Application Submission Form */
        <form onSubmit={handleSubmitApplication} className="space-y-8">
          {formErrors.length > 0 && (
            <div className="p-4 bg-rose-50 text-rose-800 border border-rose-200 rounded-xl space-y-1 text-xs font-semibold">
              <div className="font-bold">Please correct the following errors before submitting:</div>
              <ul className="list-disc pl-4 space-y-0.5 font-normal">
                {formErrors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Section 1: Personal Information */}
          <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
            <div className="border-b border-border-subtle pb-3">
              <h2 className="text-base font-bold font-headline-sm text-on-surface">1. Personal Information</h2>
              <p className="text-xs text-on-surface-variant">Core identity details as per official government records.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Full Name <span className="text-rose-600">*</span>
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Father's Name <span className="text-rose-600">*</span>
                </label>
                <input
                  type="text"
                  value={fatherName}
                  onChange={(e) => setFatherName(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Marital Status <span className="text-rose-600">*</span>
                </label>
                <select
                  value={maritalStatus}
                  onChange={(e) => setMaritalStatus(e.target.value as 'Married' | 'Unmarried')}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                >
                  <option value="Married">Married</option>
                  <option value="Unmarried">Unmarried</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Spouse Name {maritalStatus === 'Married' && <span className="text-rose-600">*</span>}
                </label>
                <input
                  type="text"
                  value={spouseName}
                  onChange={(e) => setSpouseName(e.target.value)}
                  disabled={maritalStatus === 'Unmarried'}
                  placeholder={maritalStatus === 'Unmarried' ? 'N/A (Unmarried)' : 'Enter spouse name'}
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none ${
                    maritalStatus === 'Unmarried' ? 'bg-surface-muted text-on-surface-variant/50 border-border-subtle cursor-not-allowed' : 'bg-surface border-border-subtle focus:border-[#2563EB]'
                  }`}
                />
              </div>

              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Date of Birth <span className="text-rose-600">*</span>
                </label>
                <input
                  type="date"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                  required
                />
              </div>
            </div>
          </div>

          {/* Section 2: Legal Heirs */}
          <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div>
                <h2 className="text-base font-bold font-headline-sm text-on-surface">2. Legal Heirs Information</h2>
                <p className="text-xs text-on-surface-variant">Designated legal beneficiaries for facility security.</p>
              </div>

              <button
                type="button"
                onClick={handleAddLegalHeir}
                className="px-3 py-1.5 bg-surface border border-border-subtle hover:border-[#2563EB] text-[#2563EB] rounded-md text-xs font-semibold transition-colors flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-sm">add</span> + Add Legal Heir
              </button>
            </div>

            <div className="space-y-4">
              {legalHeirs.map((heir, index) => (
                <div key={heir.id} className="p-4 bg-surface-bright rounded-lg border border-border-subtle relative space-y-3">
                  <div className="flex justify-between items-center text-xs font-semibold text-on-surface">
                    <span>Heir #{index + 1}</span>
                    {legalHeirs.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveLegalHeir(heir.id)}
                        className="text-rose-600 hover:underline text-[11px] font-semibold"
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Name</label>
                      <input
                        type="text"
                        value={heir.name}
                        onChange={(e) => handleUpdateLegalHeir(heir.id, 'name', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Relation</label>
                      <input
                        type="text"
                        value={heir.relation}
                        onChange={(e) => handleUpdateLegalHeir(heir.id, 'relation', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Address</label>
                      <input
                        type="text"
                        value={heir.address}
                        onChange={(e) => handleUpdateLegalHeir(heir.id, 'address', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Age</label>
                      <input
                        type="number"
                        value={heir.age}
                        onChange={(e) => handleUpdateLegalHeir(heir.id, 'age', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Section 3: Personal Financial Report */}
          <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
            <div className="border-b border-border-subtle pb-3">
              <h2 className="text-base font-bold font-headline-sm text-on-surface">3. Personal Financial Report</h2>
              <p className="text-xs text-on-surface-variant">Summary of personal asset holdings and debt obligations.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="space-y-2">
                <label className="block font-semibold text-on-surface uppercase tracking-wider text-[11px]">Assets Description</label>
                <textarea
                  rows={2}
                  value={assetsDesc}
                  onChange={(e) => setAssetsDesc(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                />
                <div className="flex items-center gap-2">
                  <span className="text-on-surface-variant">Estimated Total Assets ($):</span>
                  <input
                    type="number"
                    value={assetsVal}
                    onChange={(e) => setAssetsVal(e.target.value)}
                    className="w-40 px-2.5 py-1 font-mono font-bold border border-border-subtle rounded text-right focus:outline-none focus:border-[#2563EB] tnum"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="block font-semibold text-on-surface uppercase tracking-wider text-[11px]">Liabilities Description</label>
                <textarea
                  rows={2}
                  value={liabDesc}
                  onChange={(e) => setLiabDesc(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                />
                <div className="flex items-center gap-2">
                  <span className="text-on-surface-variant">Total Liabilities ($):</span>
                  <input
                    type="number"
                    value={liabVal}
                    onChange={(e) => setLiabVal(e.target.value)}
                    className="w-40 px-2.5 py-1 font-mono font-bold border border-border-subtle rounded text-right focus:outline-none focus:border-[#2563EB] tnum"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-on-surface uppercase tracking-wider mb-1">Additional Financial Notes</label>
              <input
                type="text"
                value={financialNotes}
                onChange={(e) => setFinancialNotes(e.target.value)}
                className="w-full px-3 py-1.5 text-xs bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
              />
            </div>
          </div>

          {/* Section 4: Previous Loans */}
          <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div>
                <h2 className="text-base font-bold font-headline-sm text-on-surface">4. Previous / Existing Credit Facilities</h2>
                <p className="text-xs text-on-surface-variant">Disclosure of current commercial and personal debt exposure.</p>
              </div>

              <button
                type="button"
                onClick={handleAddPreviousLoan}
                className="px-3 py-1.5 bg-surface border border-border-subtle hover:border-[#2563EB] text-[#2563EB] rounded-md text-xs font-semibold transition-colors flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-sm">add</span> + Add Previous Loan
              </button>
            </div>

            <div className="space-y-4">
              {previousLoans.map((loan, index) => (
                <div key={loan.id} className="p-4 bg-surface-bright rounded-lg border border-border-subtle space-y-3">
                  <div className="flex justify-between items-center text-xs font-semibold text-on-surface">
                    <span>Facility #{index + 1}</span>
                    {previousLoans.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemovePreviousLoan(loan.id)}
                        className="text-rose-600 hover:underline text-[11px] font-semibold"
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Lender / Institution</label>
                      <input
                        type="text"
                        value={loan.lenderName}
                        onChange={(e) => handleUpdatePreviousLoan(loan.id, 'lenderName', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Original Amount ($)</label>
                      <input
                        type="number"
                        value={loan.originalAmount}
                        onChange={(e) => handleUpdatePreviousLoan(loan.id, 'originalAmount', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB] font-mono tnum"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Outstanding ($)</label>
                      <input
                        type="number"
                        value={loan.outstandingAmount}
                        onChange={(e) => handleUpdatePreviousLoan(loan.id, 'outstandingAmount', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB] font-mono tnum"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Status</label>
                      <select
                        value={loan.status}
                        onChange={(e) => handleUpdatePreviousLoan(loan.id, 'status', e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                      >
                        <option value="Active">Active</option>
                        <option value="Closed">Closed</option>
                        <option value="Default">Default</option>
                      </select>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Section 5 & 6: Guarantee & Qualification */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Section 5: Guarantee */}
            <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
              <div className="border-b border-border-subtle pb-3">
                <h2 className="text-base font-bold font-headline-sm text-on-surface">5. Guarantee Information</h2>
                <p className="text-xs text-on-surface-variant">Guarantor details backing credit facility.</p>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Guarantor Full Name</label>
                  <input
                    type="text"
                    value={guarantorName}
                    onChange={(e) => setGuarantorName(e.target.value)}
                    className="w-full px-3 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                  />
                </div>
                <div>
                  <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Relation & Net Worth ($)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={guarantorRelation}
                      onChange={(e) => setGuarantorRelation(e.target.value)}
                      className="w-1/2 px-3 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                    />
                    <input
                      type="number"
                      value={guarantorNetWorth}
                      onChange={(e) => setGuarantorNetWorth(e.target.value)}
                      className="w-1/2 px-3 py-1.5 bg-surface border border-border-subtle rounded font-mono focus:outline-none focus:border-[#2563EB] tnum"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Section 6: Qualification */}
            <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
              <div className="border-b border-border-subtle pb-3">
                <h2 className="text-base font-bold font-headline-sm text-on-surface">6. Educational Qualification</h2>
                <p className="text-xs text-on-surface-variant">Academic and professional background.</p>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Highest Degree</label>
                  <select
                    value={highestEducation}
                    onChange={(e) => setHighestEducation(e.target.value as any)}
                    className="w-full px-3 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                  >
                    <option value="Undergraduate">Undergraduate</option>
                    <option value="Postgraduate">Postgraduate</option>
                    <option value="Professional">Professional Certification</option>
                    <option value="Doctorate">Doctorate</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[10px] uppercase text-on-surface-variant mb-1">Institution & Year</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={institutionName}
                      onChange={(e) => setInstitutionName(e.target.value)}
                      className="w-2/3 px-3 py-1.5 bg-surface border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                    />
                    <input
                      type="text"
                      value={graduationYear}
                      onChange={(e) => setGraduationYear(e.target.value)}
                      className="w-1/3 px-3 py-1.5 bg-surface border border-border-subtle rounded font-mono focus:outline-none focus:border-[#2563EB]"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Section 7: Identity Proof Documents (PAN + Aadhaar PDF Vault) */}
          <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
            <div className="border-b border-border-subtle pb-3">
              <h2 className="text-base font-bold font-headline-sm text-on-surface">7. Identity Documents (PAN & Aadhaar PDF Vault)</h2>
              <p className="text-xs text-on-surface-variant">Mandatory identity proof in PDF format for automated OCR verification.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              {/* PAN PDF Box */}
              <div className="p-4 bg-surface-bright rounded-lg border border-border-subtle space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#2563EB]">badge</span>
                    <span className="font-bold text-on-surface">PAN Card PDF</span>
                  </div>
                  {panFile && <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 uppercase">PDF Loaded</span>}
                </div>

                <label className="border border-dashed border-border-subtle hover:border-[#2563EB] p-4 rounded-md text-center block cursor-pointer bg-surface">
                  <span className="material-symbols-outlined text-xl text-on-surface-variant block mb-1">picture_as_pdf</span>
                  <span className="text-xs font-semibold text-[#2563EB]">{panFile ? panFile.name : 'Upload PAN Card PDF'}</span>
                  <span className="text-[10px] text-on-surface-variant block mt-0.5">PDF format only • Max 25MB</span>
                  <input type="file" accept=".pdf" onChange={handlePanSelect} className="hidden" />
                </label>

                {panError && <div className="text-[11px] text-rose-600 font-semibold">{panError}</div>}
              </div>

              {/* Aadhaar PDF Box */}
              <div className="p-4 bg-surface-bright rounded-lg border border-border-subtle space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#2563EB]">fingerprint</span>
                    <span className="font-bold text-on-surface">Aadhaar Card PDF</span>
                  </div>
                  {aadhaarFile && <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 uppercase">PDF Loaded</span>}
                </div>

                <label className="border border-dashed border-border-subtle hover:border-[#2563EB] p-4 rounded-md text-center block cursor-pointer bg-surface">
                  <span className="material-symbols-outlined text-xl text-on-surface-variant block mb-1">picture_as_pdf</span>
                  <span className="text-xs font-semibold text-[#2563EB]">{aadhaarFile ? aadhaarFile.name : 'Upload Aadhaar Card PDF'}</span>
                  <span className="text-[10px] text-on-surface-variant block mt-0.5">PDF format only • Max 25MB</span>
                  <input type="file" accept=".pdf" onChange={handleAadhaarSelect} className="hidden" />
                </label>

                {aadhaarError && <div className="text-[11px] text-rose-600 font-semibold">{aadhaarError}</div>}
              </div>
            </div>
          </div>

          {/* Section 8 & 9: Loan Information & Additional Notes */}
          <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
            <div className="border-b border-border-subtle pb-3">
              <h2 className="text-base font-bold font-headline-sm text-on-surface">8 & 9. Loan Request & Additional Notes</h2>
              <p className="text-xs text-on-surface-variant">Specify requested credit facility terms and notes for the underwriting committee.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Requested Amount ($) <span className="text-rose-600">*</span>
                </label>
                <input
                  type="number"
                  value={loanAmount}
                  onChange={(e) => setLoanAmount(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md font-mono font-bold text-on-surface focus:outline-none focus:border-[#2563EB] tnum"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Purpose of Loan <span className="text-rose-600">*</span>
                </label>
                <select
                  value={loanPurpose}
                  onChange={(e) => setLoanPurpose(e.target.value as any)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                >
                  <option value="Social">Social Purpose</option>
                  <option value="Medical">Medical Facility</option>
                  <option value="Commercial Real Estate">Commercial Real Estate</option>
                  <option value="Working Capital">Working Capital</option>
                  <option value="Equipment Financing">Equipment Financing</option>
                  <option value="Refinance">Refinance</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-on-surface mb-1 uppercase tracking-wider text-[11px]">
                  Bank Credit Scheme
                </label>
                <select
                  value={loanScheme}
                  onChange={(e) => setLoanScheme(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
                >
                  <option value="Priority Commercial Scheme">Priority Commercial Scheme</option>
                  <option value="Standard Retail Facility">Standard Retail Facility</option>
                  <option value="SME Growth Loan">SME Growth Loan</option>
                  <option value="Instant Approval Prime">Instant Approval Prime</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-on-surface uppercase tracking-wider mb-1">
                Any other information to the bank (Optional)
              </label>
              <textarea
                rows={3}
                value={otherInfoToBank}
                onChange={(e) => setOtherInfoToBank(e.target.value)}
                placeholder="Enter any additional context, collateral details, or notes..."
                className="w-full px-3 py-2 text-xs bg-surface border border-border-subtle rounded-md focus:outline-none focus:border-[#2563EB]"
              />
            </div>
          </div>

          {/* Section 10: Review & Final Submission Button */}
          <div className="p-6 bg-surface-bright rounded-xl border border-border-subtle flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-sm text-on-surface">10. Review & Submit Application</h3>
              <p className="text-xs text-on-surface-variant">By submitting, you authorize AgentTrust OS to process identity OCR and credit bureau checks.</p>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="px-6 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-medium text-xs rounded-md shadow-xs transition-colors flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {isSubmitting ? (
                <>
                  <span className="w-3.5 h-3.5 rounded-full border-2 border-white border-t-transparent animate-spin"></span>
                  <span>Submitting Application...</span>
                </>
              ) : (
                <>
                  <span>Submit Credit Application</span>
                  <span className="material-symbols-outlined text-base">send</span>
                </>
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
