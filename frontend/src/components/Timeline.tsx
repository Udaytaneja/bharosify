import React from 'react'

interface TimelineEvent {
  title: string
  date: string
  description?: string
  completed?: boolean
}

interface TimelineProps {
  events?: TimelineEvent[]
  items?: TimelineEvent[]
}

const Timeline: React.FC<TimelineProps> = ({ events, items }) => {
  const displayEvents = events || items || []
  return (
    <div className="space-y-6">
      {displayEvents.map((event, index) => (
        <div key={index} className="flex gap-4">
          <div className="flex flex-col items-center">
            <div
              className={`w-3.5 h-3.5 rounded-full flex items-center justify-center text-[10px] text-white ${
                event.completed !== false ? 'bg-status-success' : 'bg-border'
              }`}
            >
              {event.completed !== false ? '✓' : ''}
            </div>
            {index < displayEvents.length - 1 && (
              <div
                className={`w-0.5 h-12 mt-1 ${
                  event.completed !== false ? 'bg-status-success/40' : 'bg-border'
                }`}
              />
            )}
          </div>
          <div className="pb-2">
            <p className="font-semibold text-text-primary text-sm">{event.title}</p>
            <p className="text-xs text-text-muted mt-0.5">{event.date}</p>
            {event.description && <p className="text-xs text-text-secondary mt-1">{event.description}</p>}
          </div>
        </div>
      ))}
    </div>
  )
}

export default Timeline
