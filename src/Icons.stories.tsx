import type { Meta, StoryObj } from '@storybook/react';
import * as Icons from './index';
import { Fill, Style } from './types';
import React from 'react';

// Get all icon components (filter out Props types)
const iconEntries = Object.entries(Icons).filter(
  ([name]) => !name.endsWith('Props') && typeof Icons[name as keyof typeof Icons] === 'function'
) as Array<[string, React.ComponentType<any>]>;

// Icons that only have style prop (no fill)
const iconsWithoutFill = new Set([
  'Alt', 'Command', 'Control', 'Option', 'OptionKey', 'OptionKey1',
  'Shift', 'ShiftKey', 'Tab'
]);

const meta: Meta = {
  title: 'Icons',
  parameters: {
    layout: 'padded',
  },
};

export default meta;
type Story = StoryObj;

// Story for all icons grid
export const AllIcons: Story = {
  render: () => {
    const IconComponents = iconEntries.map(([name, Component]) => ({
      name,
      Component: Component as React.ComponentType<any>,
    }));

    return (
      <div style={{ padding: '2rem' }}>
        <h1 style={{ marginBottom: '1rem', fontSize: '2rem', fontWeight: 'bold' }}>
          WyDee Icons Library
        </h1>
        <p style={{ marginBottom: '2rem', color: '#666', fontSize: '1rem' }}>
          Total Icons: {IconComponents.length}
        </p>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {IconComponents.map(({ name, Component }) => (
            <div
              key={name}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                padding: '1.5rem',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                backgroundColor: '#fff',
                transition: 'box-shadow 0.2s',
                cursor: 'pointer',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <Component size={48} />
              <span
                style={{
                  marginTop: '0.75rem',
                  fontSize: '0.875rem',
                  textAlign: 'center',
                  fontWeight: '500',
                }}
              >
                {name}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  },
};

// Story showing all variants for icons with fill
export const IconVariants: Story = {
  render: () => {
    const fills: Fill[] = ['Outline', 'Solid', 'Tonal'];
    const styles: Style[] = ['Sharp', 'Soft', 'Round'];
    
    const iconsWithFill = iconEntries.filter(
      ([name]) => !iconsWithoutFill.has(name)
    );

    return (
      <div style={{ padding: '2rem' }}>
        <h1 style={{ marginBottom: '2rem', fontSize: '2rem', fontWeight: 'bold' }}>
          Icon Variants Preview
        </h1>
        {iconsWithFill.slice(0, 5).map(([name, Component]) => {
          const IconComponent = Component as React.ComponentType<any>;
          return (
            <div key={name} style={{ marginBottom: '3rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: 'bold' }}>
                {name}
              </h2>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(3, 1fr)',
                  gap: '1rem',
                }}
              >
                {fills.map((fill) =>
                  styles.map((style) => (
                    <div
                      key={`${fill}-${style}`}
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        padding: '1rem',
                        border: '1px solid #e0e0e0',
                        borderRadius: '8px',
                        backgroundColor: '#fff',
                      }}
                    >
                      <IconComponent fill={fill} style={style} size={48} />
                      <span
                        style={{
                          marginTop: '0.5rem',
                          fontSize: '0.75rem',
                          fontWeight: '500',
                        }}
                      >
                        {fill} - {style}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    );
  },
};

// Individual icon story template
function createIconStory(name: string, Component: React.ComponentType<any>) {
  const usesFill = !iconsWithoutFill.has(name);
  
  return {
    render: (args: any) => {
      if (usesFill) {
        const fills: Fill[] = ['Outline', 'Solid', 'Tonal'];
        const styles: Style[] = ['Sharp', 'Soft', 'Round'];

        return (
          <div style={{ padding: '2rem' }}>
            <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: 'bold' }}>
              {name}
            </h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1.5rem',
              }}
            >
              {fills.map((fill) =>
                styles.map((style) => (
                  <div
                    key={`${fill}-${style}`}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      padding: '1.5rem',
                      border: '1px solid #e0e0e0',
                      borderRadius: '8px',
                      backgroundColor: '#fff',
                    }}
                  >
                    <Component fill={fill} style={style} size={64} {...args} />
                    <span
                      style={{
                        marginTop: '0.75rem',
                        fontSize: '0.875rem',
                        fontWeight: '500',
                      }}
                    >
                      {fill} - {style}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        );
      } else {
        const styles: Style[] = ['Sharp', 'Soft', 'Round'];

        return (
          <div style={{ padding: '2rem' }}>
            <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: 'bold' }}>
              {name}
            </h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1.5rem',
              }}
            >
              {styles.map((style) => (
                <div
                  key={style}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    padding: '1.5rem',
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                    backgroundColor: '#fff',
                  }}
                >
                  <Component style={style} size={64} {...args} />
                  <span
                    style={{
                      marginTop: '0.75rem',
                      fontSize: '0.875rem',
                      fontWeight: '500',
                    }}
                  >
                    {style}
                  </span>
                </div>
              ))}
            </div>
          </div>
        );
      }
    },
    args: {
      size: 24,
    },
  } as Story;
}

// Create stories for first few icons as examples
export const SoupExample = createIconStory('Soup', Icons.Soup);
export const DocumentExample = createIconStory('Document', Icons.Document);
export const AltExample = createIconStory('Alt', Icons.Alt);
