export type Fill = 'Outline' | 'Solid' | 'Tonal';
export type Style = 'Sharp' | 'Soft' | 'Round';

export interface IconProps {
  className?: string;
  fill?: Fill;
  style?: Style;
  size?: number | string;
  'data-component-config'?: string;
}

export interface IconMetadata {
  name: string;
  componentConfig?: string;
}

