import React from 'react';
import { cn } from '@/lib/utils';

export interface MenuToggleIconProps extends React.ComponentProps<'svg'> {
  open?: boolean;
  duration?: number;
}

export function MenuToggleIcon({
  open = false,
  duration = 300,
  className,
  ...props
}: MenuToggleIconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={cn('transition-all duration-300', className)}
      style={{ transitionDuration: `${duration}ms` }}
      {...props}
    >
      <line
        x1="4"
        y1={open ? '4' : '6'}
        x2="20"
        y2={open ? '20' : '6'}
        className="origin-center transition-all"
        style={{ transitionDuration: `${duration}ms` }}
      />
      <line
        x1="4"
        y1="12"
        x2="20"
        y2="12"
        className={cn('transition-opacity', { 'opacity-0': open })}
        style={{ transitionDuration: `${duration}ms` }}
      />
      <line
        x1="4"
        y1={open ? '20' : '18'}
        x2="20"
        y2={open ? '4' : '18'}
        className="origin-center transition-all"
        style={{ transitionDuration: `${duration}ms` }}
      />
    </svg>
  );
}
