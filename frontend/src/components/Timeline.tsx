import React from 'react'

interface TimelineEvent {
  title: string
  date: string
  description?: string
}

interface TimelineProps {
  events: TimelineEvent[]
}

const Timeline: React.FC<TimelineProps> = ({ events }) => {
  return (
    <div className="space-y-6">
      {events.map((event, index) => (
        <div key={index} className="flex gap-4">
          <div className="flex flex-col items-center">
            <div className="w-3 h-3 rounded-full bg-brand-700" />
            {index < events.length - 1 && <div className="w-0.5 h-16 bg-border mt-2" />}
          </div>
          <div className="pb-6">
            <p className="font-medium text-text-primary">{event.title}</p>
            <p className="text-sm text-text-muted">{event.date}</p>
            {event.description && <p className="text-sm text-text-secondary mt-1">{event.description}</p>}
          </div>
        </div>
      ))}
    </div>
  )
}

export default Timeline
