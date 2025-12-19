import React from 'react';
import { IconProps, Fill, Style } from '../types';

export interface BaseIconProps extends IconProps {
  svgContent: string;
  metadata?: {
    name: string;
    componentConfig?: string;
  };
}

export function BaseIcon({ 
  className = '', 
  fill = 'Outline', 
  style = 'Sharp',
  size = 24,
  svgContent,
  metadata,
  'data-component-config': dataComponentConfig,
  ...props 
}: BaseIconProps) {
  const svgProps = {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'currentColor',
    className,
    'data-fill': fill,
    'data-style': style,
    'data-component-config': dataComponentConfig || metadata?.componentConfig || metadata?.name,
    ...props
  };

  return (
    <svg {...svgProps} dangerouslySetInnerHTML={{ __html: svgContent }} />
  );
}

