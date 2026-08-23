import React from 'react'
import Button from './Button'

interface ConfirmationDialogProps {
  isOpen: boolean
  title: string
  message: string
  confirmText?: string
  confirmLabel?: string
  cancelText?: string
  cancelLabel?: string
  isDangerous?: boolean
  onConfirm: () => void
  onCancel?: () => void
  onClose?: () => void
  isLoading?: boolean
}

const ConfirmationDialog: React.FC<ConfirmationDialogProps> = ({
  isOpen,
  title,
  message,
  confirmText,
  confirmLabel,
  cancelText,
  cancelLabel,
  isDangerous,
  onConfirm,
  onCancel,
  onClose,
  isLoading,
}) => {
  if (!isOpen) return null

  const handleDismiss = onClose || onCancel || (() => {})
  const displayConfirm = confirmLabel || confirmText || 'Confirm'
  const displayCancel = cancelLabel || cancelText || 'Cancel'

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-bg-surface rounded-lg shadow-lg max-w-sm w-full mx-4">
        <div className="px-6 py-4 border-b border-border">
          <h2 className="text-lg font-semibold text-text-primary">{title}</h2>
        </div>

        <div className="px-6 py-4">
          <p className="text-text-secondary text-sm">{message}</p>
        </div>

        <div className="flex items-center justify-end gap-3 border-t border-border px-6 py-4">
          <Button variant="secondary" onClick={handleDismiss} disabled={isLoading}>
            {displayCancel}
          </Button>
          <Button
            variant={isDangerous ? 'danger' : 'primary'}
            onClick={onConfirm}
            isLoading={isLoading}
          >
            {displayConfirm}
          </Button>
        </div>
      </div>
    </div>
  )
}

export default ConfirmationDialog
