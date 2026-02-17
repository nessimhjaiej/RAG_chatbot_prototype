# Modern Light Theme Conversion Prompt for AI Agents

You are a UI/UX specialist tasked with converting an existing web application to a modern light theme. Follow these guidelines precisely.

## Core Objectives

1. Transform all colors to a cohesive modern light palette
2. Maintain all existing functionality and layout structure
3. Improve visual hierarchy and spacing
4. Apply contemporary design patterns
5. Ensure accessibility and readability

## Modern Light Theme Specification

### Color Palette (Use these exact hex values)

**Base Colors:**
- Page Background: `#f5f5f7`
- Surface/Card Background: `#ffffff`
- Primary Brand: `#4f46e5` (Indigo)
- Primary Soft Background: `#eef2ff`
- Secondary: `#6366f1`

**Text Colors:**
- Primary Text: `#111827` (Near-black)
- Secondary Text: `#6b7280` (Medium gray)
- Muted Text: `#9ca3af` (Light gray)
- Text on Primary: `#ffffff` (White)

**Utility Colors:**
- Success: `#22c55e` (Green)
- Warning: `#f59e0b` (Amber)
- Danger/Error: `#ef4444` (Red)
- Info: `#06b6d4` (Cyan)

**Borders & Dividers:**
- Subtle Border: `#e5e7eb` (Light gray)
- Strong Border: `#d1d5db` (Medium gray)
- Hover Border: `#bfdbfe` (Light blue)

### Typography

**Font Family:** Use system fonts in this order:
```
system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif
```

**Font Sizes & Weight:**
- H1: 28-32px, weight 600, letter-spacing -0.02em
- H2: 22-24px, weight 600
- H3: 18-20px, weight 600
- Body: 14-16px, weight 400
- Small: 12-13px, weight 400
- Button/Label: 14px, weight 500

**Line Height:**
- Headings: 1.2
- Body text: 1.6
- Compact: 1.4

### Spacing & Layout

**Spacing Scale (in pixels):**
- xs: 4px
- sm: 8px
- md: 12px
- lg: 16px
- xl: 20px
- 2xl: 24px
- 3xl: 32px

**Border Radius:**
- Small elements (buttons, badges): 6-8px
- Cards, modals: 12-16px
- Rounded buttons: 999px (full round)

**Shadows (for elevation):**
- Subtle (hover): `0 4px 6px rgba(0, 0, 0, 0.07)`
- Medium (cards): `0 10px 15px rgba(0, 0, 0, 0.1)`
- Large (modals): `0 20px 25px rgba(0, 0, 0, 0.15)`

### Component Patterns

**Buttons:**
- Primary: Solid background `#4f46e5`, white text, rounded corners
- Secondary: Light background `#eef2ff`, text `#4f46e5`, rounded corners
- Ghost/Outline: Transparent with 1px border `#e5e7eb`, text `#111827`
- Hover: Slightly darker shade + subtle shadow
- Disabled: 50% opacity, no pointer events

**Cards:**
- Background: `#ffffff`
- Border: 1px `#e5e7eb`
- Border-radius: 12-16px
- Padding: 16-24px
- Shadow on hover (optional): subtle shadow

**Navigation/Header:**
- Background: `#ffffffcc` with `backdrop-filter: blur(12px)` for modern glassmorphism
- Border-bottom: 1px `#e5e7eb`
- Position: sticky, z-index: 20

**Input Fields:**
- Background: `#ffffff`
- Border: 1px `#e5e7eb`
- Border-radius: 8px
- Padding: 8-10px 12px
- Focus: border `#4f46e5`, box-shadow with primary color (10% opacity)
- Placeholder: `#9ca3af`

**Status Indicators:**
- Success: background `rgba(34, 197, 94, 0.1)`, border `#22c55e`, text `#166534`
- Warning: background `rgba(245, 158, 11, 0.1)`, border `#f59e0b`, text `#92400e`
- Error: background `rgba(239, 68, 68, 0.1)`, border `#ef4444`, text `#991b1b`
- Info: background `rgba(6, 182, 212, 0.1)`, border `#06b6d4`, text `#164e63`

## Conversion Instructions

### Step 1: Global Styles
- Define CSS variables (`:root`) with all colors from the palette above
- Set body background to page background color
- Set default text color to primary text
- Apply system font family globally
- Set default line-height to 1.6

### Step 2: Replace Colors
- Search and replace all existing color values with the modern palette
- Dark backgrounds → `#f5f5f7` or `#ffffff`
- Dark text → `#111827` or `#6b7280` depending on context
- Bright/neon colors → Replace with the modern accent colors
- Remove any dark mode variables (keep light mode only)

### Step 3: Update Components
- **All buttons:** Apply button pattern styles (rounded, proper spacing, hover states)
- **All cards/containers:** Add 1px border, subtle shadow on hover
- **Navigation:** Make sticky with glassmorphism effect
- **Forms:** Style inputs with light theme borders and focus states
- **Status messages/alerts:** Use status indicator pattern colors

### Step 4: Spacing & Sizing
- Add consistent padding/margins using the spacing scale
- Ensure minimum 16px padding in containers
- Set max-width to 1120-1200px for content areas with auto margin
- Use proper spacing between sections (24-32px)

### Step 5: Visual Hierarchy
- Use size and weight for hierarchy, not multiple colors
- Limit primary accent color usage to CTAs and highlights only
- Use secondary text color for descriptions and metadata
- Apply muted color only for very subtle information

### Step 6: Accessibility Checks
- Ensure text contrast ratio is at least 4.5:1 for normal text
- Check that all interactive elements have clear focus states
- Verify hover states are obvious (no opacity-only changes)
- Test that color is not the only way to convey information

## CSS Framework Template

```css
:root {
  /* Colors */
  --bg-page: #f5f5f7;
  --bg-surface: #ffffff;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --accent: #4f46e5;
  --accent-soft: #eef2ff;
  --border: #e5e7eb;
  --success: #22c55e;
  --error: #ef4444;
  --warning: #f59e0b;

  /* Typography */
  --font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --fs-h1: 28px;
  --fs-h2: 22px;
  --fs-body: 14px;
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;

  /* Spacing */
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 999px;

  /* Shadows */
  --shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-md: 0 10px 15px rgba(0, 0, 0, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  font-size: var(--fs-body);
  font-weight: var(--fw-regular);
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--bg-page);
}

/* Example: Buttons */
.btn {
  padding: 8px 16px;
  border-radius: var(--radius-full);
  border: none;
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all 0.18s ease;
}

.btn-primary {
  background: var(--accent);
  color: #ffffff;
}

.btn-primary:hover {
  background: #4338ca;
  box-shadow: var(--shadow-md);
}

/* Example: Cards */
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
}

.card:hover {
  box-shadow: var(--shadow-sm);
}
```

## Quality Checklist

- [ ] All dark backgrounds converted to light theme
- [ ] All text colors updated to modern palette
- [ ] Buttons have proper hover and active states
- [ ] Cards have subtle borders and shadows
- [ ] Spacing is consistent using the scale
- [ ] Navigation is sticky with proper styling
- [ ] Input fields have focus states
- [ ] Status colors applied correctly
- [ ] Typography hierarchy is clear
- [ ] No dark mode code remains
- [ ] Accessibility contrast ratios met
- [ ] All interactive elements have clear focus states

## Additional Modern Design Tips

1. **Whitespace:** Don't crowd elements; use plenty of breathing room
2. **Glassmorphism:** Use `backdrop-filter: blur()` for headers/overlays
3. **Micro-interactions:** Smooth transitions (0.15-0.3s) on hover/focus
4. **Consistency:** Use the same spacing and radius throughout
5. **Subtlety:** Avoid harsh shadows and bright colors; keep it refined
6. **Performance:** Use CSS variables for theme flexibility

---

## How to Use This Prompt

1. Copy this entire prompt
2. Provide it to your AI agent along with your project code
3. Ask the agent to: "Apply this modern light theme specification to my project"
4. The agent should output updated CSS/component files
5. Review the changes and test in your browser
6. Make any minor adjustments as needed

Good luck with your theme transformation! 🎨