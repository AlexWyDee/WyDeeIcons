import React from 'react';
import { Style } from '../types';

export interface OptionKey1Props {
  className?: string;
  style?: Style;
  size?: number | string;
  'data-component-config'?: string;
}

const SVG_VARIANTS: Record<string, string> = {
  'N/A-Round': "<g id=\"Vector\">\n<path d=\"M6.12423 1.64594C5.79143 1.04689 5.62503 0.747371 5.38835 0.529266C5.17897 0.336315 4.93081 0.190295 4.66046 0.10097C4.35486 0 4.01222 0 3.32693 0H0.75C0.335786 0 0 0.335786 0 0.75C0 1.16421 0.335787 1.5 0.75 1.5H3.81946C3.99078 1.5 4.07644 1.5 4.15284 1.52524C4.22043 1.54757 4.28247 1.58408 4.33481 1.63232C4.39398 1.68684 4.43558 1.76172 4.51878 1.91149L8.37577 8.85406C8.70857 9.4531 8.87497 9.75263 9.11165 9.97073C9.32103 10.1637 9.56919 10.3097 9.83954 10.399C10.1451 10.5 10.4878 10.5 11.1731 10.5H15.5C15.9142 10.5 16.25 10.1642 16.25 9.75C16.25 9.33579 15.9142 9 15.5 9H10.6805C10.5092 9 10.4236 9 10.3472 8.97476C10.2796 8.95243 10.2175 8.91592 10.1652 8.86768C10.106 8.81316 10.0644 8.73828 9.98122 8.58851L6.12423 1.64594Z\" fill=\"var(--fill-0, #363738)\"/>\n<path d=\"M16.25 0.75C16.25 0.335786 15.9142 0 15.5 0H10.75C10.3358 0 10 0.335786 10 0.75C10 1.16421 10.3358 1.5 10.75 1.5H15.5C15.9142 1.5 16.25 1.16421 16.25 0.75Z\" fill=\"var(--fill-0, #363738)\"/>\n</g>",
  'N/A-Sharp': "<path id=\"Vector\" d=\"M16.0821 6.24176L8.04107 0L0 6.24176L0.860727 7.47137L8.04107 1.84289L15.2214 7.47137L16.0821 6.24176Z\" fill=\"var(--fill-0, #363738)\"/>",
  'N/A-Soft': "<g id=\"Vector\">\n<path d=\"M5.78133 1.02871C5.42859 0.393784 4.75935 0 4.03302 0H0.75C0.335786 0 0 0.335786 0 0.75C0 1.16421 0.335787 1.5 0.75 1.5H3.99598C4.17756 1.5 4.34487 1.59845 4.43306 1.75718L8.71867 9.47129C9.07141 10.1062 9.74065 10.5 10.467 10.5H15.5C15.9142 10.5 16.25 10.1642 16.25 9.75C16.25 9.33579 15.9142 9 15.5 9H10.504C10.3224 9 10.1551 8.90155 10.0669 8.74282L5.78133 1.02871Z\" fill=\"var(--fill-0, #363738)\"/>\n<path d=\"M16.25 0.75C16.25 0.335786 15.9142 0 15.5 0H10.75C10.3358 0 10 0.335786 10 0.75C10 1.16421 10.3358 1.5 10.75 1.5H15.5C15.9142 1.5 16.25 1.16421 16.25 0.75Z\" fill=\"var(--fill-0, #363738)\"/>\n</g>",
};

export function OptionKey1({ 
  className = '', 
  style = 'Sharp' as Style,
  size = 24,
  'data-component-config': dataComponentConfig,
  ...props 
}: OptionKey1Props) {
  const variantKey = `N/A-${style}`;
  const svgContent = SVG_VARIANTS[variantKey] || SVG_VARIANTS['N/A-Sharp'] || '';

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      className={className}
      data-style={style}
      data-component-config={dataComponentConfig || 'Option Key 1'}
      {...props}
      dangerouslySetInnerHTML={{ __html: svgContent }}
    />
  );
}
