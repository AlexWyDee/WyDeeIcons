# WyDee Icons

Product Icons by Alex Young-Davies (www.alexyoungdavies.com)

A React icon component library with support for multiple fill and style variants.

## Overview

This library contains icon components extracted from Figma designs. Each icon (pictogram) supports up to 9 variants based on combinations of:

- **Fill**: `Outline`, `Solid`, or `Tonal`
- **Style**: `Sharp`, `Soft`, or `Round`

## Installation

```bash
npm install
```

## Usage

### Basic Usage

```tsx
import { Soup, Burger } from 'wydee-icons';

function App() {
  return (
    <div>
      <Soup fill="Solid" style="Round" size={32} />
      <Burger fill="Outline" style="Sharp" />
    </div>
  );
}
```

### Props

All icon components accept the following props:

- `fill?: 'Outline' | 'Solid' | 'Tonal'` - The fill variant (default: `'Outline'`)
- `style?: 'Sharp' | 'Soft' | 'Round'` - The style variant (default: `'Sharp'`)
- `size?: number | string` - Icon size in pixels (default: `24`)
- `className?: string` - Additional CSS classes
- `data-component-config?: string` - Metadata for component search/identification

### Available Icons

- `Burger`
- `Carrot`
- `CarrotAlt`
- `Carton`
- `Drumstick`
- `GlassBottle`
- `Grapes`
- `HotDrink`
- `MilkBottle`
- `Mug`
- `Soup`

### Example: All Variants

```tsx
import { Soup } from 'wydee-icons';

function IconShowcase() {
  const fills = ['Outline', 'Solid', 'Tonal'] as const;
  const styles = ['Sharp', 'Soft', 'Round'] as const;

  return (
    <div>
      {fills.map(fill => 
        styles.map(style => (
          <Soup 
            key={`${fill}-${style}`}
            fill={fill} 
            style={style}
            data-component-config="Soup"
          />
        ))
      )}
    </div>
  );
}
```

## Development

### Regenerating Components from Figma

To regenerate components from Figma:

1. Open your Figma file and select the frame containing the icons
2. Run the generation script:

```bash
python3 scripts/generate-components.py
```

This script will:
- Fetch SVG content from Figma's localhost server
- Extract the SVG vectors
- Generate React components with embedded SVG content
- Create/update the index file

**Note**: Make sure Figma is running and the localhost server is accessible when running the script.

### Project Structure

```
wydee-icons/
├── src/
│   ├── icons/          # Individual icon components
│   ├── types.ts        # TypeScript type definitions
│   ├── components/     # Base components and utilities
│   └── index.ts        # Main export file
├── scripts/
│   └── generate-components.py  # Component generation script
└── package.json
```

## Component Configuration Metadata

Each component includes a `data-component-config` attribute that can be used for searching and filtering icons. This attribute:

- Is set to the component name by default (e.g., `"Soup"`, `"Burger"`)
- Can be overridden via the `data-component-config` prop
- Should contain the "Component Configuration" string from Figma if available

```tsx
<Soup 
  data-component-config="food, meal, soup, hot"
  fill="Solid"
  style="Round"
/>
```

This metadata can be used to build search functionality or icon pickers. To extract Component Configuration from Figma components, you may need to manually add it to the generation script or extract it from Figma's component properties/descriptions.

## Building

```bash
npm run build
```

This will compile TypeScript and generate type definitions in the `dist/` directory.

## License

MIT
