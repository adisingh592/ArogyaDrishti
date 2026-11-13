/**
 * MagnificationDock Component
 * 
 * A rock-solid, stable macOS-inspired dock component with fluid magnification effects, 
 * spring physics, and tooltips. Built with Framer Motion.
 * Supports both vertical (right/left aligned) and horizontal orientations.
 */

import {
  motion,
  MotionValue,
  useMotionValue,
  useSpring,
  useTransform,
  type SpringOptions,
  AnimatePresence,
} from 'framer-motion';
import React, { Children, cloneElement, useEffect, useRef, useState } from 'react';
import { cn } from '@/lib/utils';

export type DockItemData = {
  icon: React.ReactNode;
  label: React.ReactNode;
  onClick: () => void;
  className?: string;
  active?: boolean;
};

export type DockProps = {
  items: DockItemData[];
  className?: string;
  distance?: number;
  panelHeight?: number;
  panelWidth?: number;
  baseItemSize?: number;
  magnification?: number;
  spring?: SpringOptions;
  orientation?: 'vertical' | 'horizontal';
};

type DockItemProps = {
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
  mousePos: MotionValue<number>;
  spring: SpringOptions;
  distance: number;
  baseItemSize: number;
  magnification: number;
  active?: boolean;
  orientation?: 'vertical' | 'horizontal';
};

function DockItem({
  children,
  className = '',
  onClick,
  mousePos,
  spring,
  distance,
  magnification,
  baseItemSize,
  active = false,
  orientation = 'vertical',
}: DockItemProps) {
  const ref = useRef<HTMLDivElement>(null);
  const isHovered = useMotionValue(0);

  // Measure distance along Y for vertical dock, or along X for horizontal dock
  const mouseDistance = useTransform(mousePos, (val: number) => {
    if (val === Infinity || !ref.current) return Infinity;
    const rect = ref.current.getBoundingClientRect();
    if (orientation === 'vertical') {
      const centerY = rect.top + rect.height / 2;
      return val - centerY;
    }
    const centerX = rect.left + rect.width / 2;
    return val - centerX;
  });

  const targetSize = useTransform(
    mouseDistance,
    [-distance, 0, distance],
    [baseItemSize, magnification, baseItemSize]
  );

  const size = useSpring(targetSize, spring);

  return (
    <motion.div
      ref={ref}
      style={{
        width: size,
        height: size,
      }}
      onHoverStart={() => isHovered.set(1)}
      onHoverEnd={() => isHovered.set(0)}
      onFocus={() => isHovered.set(1)}
      onBlur={() => isHovered.set(0)}
      onClick={onClick}
      className={cn(
        'relative inline-flex items-center justify-center rounded-full bg-[#272727] border border-white/10 shadow-md cursor-pointer flex-shrink-0 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#ffe17c] select-none',
        active && 'ring-2 ring-[#ffe17c] bg-[#ffe17c] text-[#171e19]',
        className
      )}
      tabIndex={0}
      role="button"
      aria-haspopup="true"
    >
      {Children.map(children, child =>
        React.isValidElement(child)
          ? cloneElement(
              child as React.ReactElement<{
                isHovered?: MotionValue<number>;
                orientation?: 'vertical' | 'horizontal';
              }>,
              { isHovered, orientation }
            )
          : child
      )}
      {active && (
        <span
          className={cn(
            'absolute w-1.5 h-1.5 rounded-full bg-[#ffe17c] pointer-events-none',
            orientation === 'vertical'
              ? '-left-2 top-1/2 -translate-y-1/2 shadow-[0_0_8px_#ffe17c]'
              : '-bottom-1.5 left-1/2 -translate-x-1/2'
          )}
        />
      )}
    </motion.div>
  );
}

type DockLabelProps = {
  className?: string;
  children: React.ReactNode;
  isHovered?: MotionValue<number>;
  orientation?: 'vertical' | 'horizontal';
};

function DockLabel({
  children,
  className = '',
  isHovered,
  orientation = 'vertical',
}: DockLabelProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (!isHovered) return;
    const unsubscribe = isHovered.on('change', (latest: number) => {
      setIsVisible(latest === 1);
    });
    return () => unsubscribe();
  }, [isHovered]);

  const isVertical = orientation === 'vertical';

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{
            opacity: 0,
            x: isVertical ? 6 : '-50%',
            y: isVertical ? '-50%' : 0,
            scale: 0.95,
          }}
          animate={{
            opacity: 1,
            x: isVertical ? 0 : '-50%',
            y: isVertical ? '-50%' : -10,
            scale: 1,
          }}
          exit={{
            opacity: 0,
            x: isVertical ? 6 : '-50%',
            y: isVertical ? '-50%' : 0,
            scale: 0.95,
          }}
          transition={{ duration: 0.15, ease: 'easeOut' }}
          className={cn(
            'absolute w-fit whitespace-nowrap rounded-md border border-white/15 bg-[#171e19] px-2.5 py-1 text-[11px] font-medium font-mono text-[#ffe17c] shadow-2xl pointer-events-none z-50',
            isVertical
              ? 'right-full mr-3.5 top-1/2'
              : '-top-9 left-1/2',
            className
          )}
          role="tooltip"
        >
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

type DockIconProps = {
  className?: string;
  children: React.ReactNode;
  isHovered?: MotionValue<number>;
};

function DockIcon({ children, className = '' }: DockIconProps) {
  return (
    <div className={cn('flex items-center justify-center text-current pointer-events-none', className)}>
      {children}
    </div>
  );
}

export function MagnificationDock({
  items,
  className = '',
  spring = { mass: 0.1, stiffness: 180, damping: 14 },
  magnification = 68,
  distance = 140,
  panelHeight,
  panelWidth,
  baseItemSize = 46,
  orientation = 'vertical',
}: DockProps) {
  const mousePos = useMotionValue(Infinity);

  return (
    <div
      onMouseMove={(e) => {
        // Use client coordinates so fixed positioning is stable across scrolling
        mousePos.set(orientation === 'vertical' ? e.clientY : e.clientX);
      }}
      onMouseLeave={() => {
        mousePos.set(Infinity);
      }}
      className={cn(
        'relative flex items-center justify-center pointer-events-auto rounded-full border border-white/10 bg-[#171e19]/90 backdrop-blur-xl shadow-[0_16px_40px_rgba(0,0,0,0.45)] select-none transition-all',
        orientation === 'vertical'
          ? 'flex-col gap-2.5 px-2 py-3 w-fit'
          : 'flex-row gap-2.5 py-2 px-3 h-fit',
        className
      )}
      style={{
        width: panelWidth,
        height: panelHeight,
      }}
      role="toolbar"
      aria-label="Application dock"
    >
      {items.map((item, index) => (
        <DockItem
          key={index}
          onClick={item.onClick}
          className={item.className}
          mousePos={mousePos}
          spring={spring}
          distance={distance}
          magnification={magnification}
          baseItemSize={baseItemSize}
          active={item.active}
          orientation={orientation}
        >
          <DockIcon>{item.icon}</DockIcon>
          <DockLabel orientation={orientation}>{item.label}</DockLabel>
        </DockItem>
      ))}
    </div>
  );
}

export default MagnificationDock;
