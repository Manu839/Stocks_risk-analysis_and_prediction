import { AlertCircle, RefreshCw, X } from 'lucide-react'

const ErrorMessage = ({ 
  error, 
  onRetry = null, 
  onDismiss = null, 
  className = '',
  variant = 'error' 
}) => {
  const variants = {
    error: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-700',
      icon: 'text-red-500'
    },
    warning: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-200',
      text: 'text-yellow-700',
      icon: 'text-yellow-500'
    },
    info: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-700',
      icon: 'text-blue-500'
    }
  }

  const style = variants[variant]

  return (
    <div className={`${style.bg} ${style.border} border rounded-md p-4 ${className}`}>
      <div className="flex items-start">
        <AlertCircle className={`h-5 w-5 ${style.icon} mr-3 mt-0.5 flex-shrink-0`} />
        <div className="flex-1">
          <p className={`text-sm ${style.text}`}>
            {typeof error === 'string' ? error : error?.message || 'An unexpected error occurred'}
          </p>
          {(onRetry || onDismiss) && (
            <div className="mt-3 flex space-x-2">
              {onRetry && (
                <button
                  onClick={onRetry}
                  className={`inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md ${style.text} bg-white border ${style.border} hover:bg-gray-50 transition-colors`}
                >
                  <RefreshCw className="h-3 w-3 mr-1" />
                  Try Again
                </button>
              )}
              {onDismiss && (
                <button
                  onClick={onDismiss}
                  className={`inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md ${style.text} bg-white border ${style.border} hover:bg-gray-50 transition-colors`}
                >
                  <X className="h-3 w-3 mr-1" />
                  Dismiss
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ErrorMessage
