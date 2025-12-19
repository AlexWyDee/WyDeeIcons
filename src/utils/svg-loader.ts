// Utility to load SVG content
// This will be used to load SVG files or fetch from URLs

export async function loadSVG(url: string): Promise<string> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to load SVG: ${response.statusText}`);
    }
    return await response.text();
  } catch (error) {
    console.error(`Error loading SVG from ${url}:`, error);
    throw error;
  }
}

export function extractSVGContent(svgString: string): string {
  // Extract the inner content of the SVG (remove outer <svg> tags)
  const match = svgString.match(/<svg[^>]*>(.*?)<\/svg>/s);
  if (match) {
    return match[1];
  }
  return svgString;
}

