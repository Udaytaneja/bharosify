import React from 'react'

interface SkeletonProps {
  width?: string
  height?: string
  count?: number
  circle?: boolean
  className?: string
}

const Skeleton: React.FC<SkeletonProps> = ({ width = '100%', height = '20px', count = 1, circle, className }) => {
  const skeletons = Array.from({ length: count })

  return (
    <>
      {skeletons.map((_, i) => (
        <div
          key={i}
          className={`bg-gray-200 animate-pulse ${circle ? 'rounded-full' : 'rounded'} ${className || ''}`}
          style={{ width, height: circle && !height ? width : height }}
        />
      ))}
    </>
  )
}

export default Skeleton
