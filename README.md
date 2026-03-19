# WyDee Icons

A React icon library with ~950 pictogram icons and ~6,900 total variants across three styles and three fills.

## Installation

```bash
npm install wydee-icons
# or
yarn add wydee-icons
# or
pnpm add wydee-icons
```

React 17+ is required as a peer dependency.

## Usage

```tsx
import { Arrow, Sparkle, Search } from 'wydee-icons';

// Standard icon — style + fill props
<Arrow style="Round" fill="Solid" />

// Outline-only icon — style prop only
<Sparkle style="Soft" />

// With extra SVG props
<Search style="Sharp" fill="Tonal" className="w-5 h-5" aria-label="Search" />
```

All extra props (`className`, `onClick`, `aria-label`, etc.) are forwarded to the underlying `<svg>` element.

## Props

### Standard icons

| Prop | Type | Default | Options |
|------|------|---------|---------|
| `style` | `Style` | `'Sharp'` | `'Sharp'` \| `'Soft'` \| `'Round'` |
| `fill` | `Fill` | `'Outline'` | `'Outline'` \| `'Solid'` \| `'Tonal'` |

### Outline-only icons

| Prop | Type | Default | Options |
|------|------|---------|---------|
| `style` | `Style` | `'Sharp'` | `'Sharp'` \| `'Soft'` \| `'Round'` |

These icons only exist in the Outline fill and do not accept a `fill` prop.

## License

MIT
