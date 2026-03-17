# Design Advisor

## Overview

A design advisor skill that provides industry-specific UI/UX recommendations before building. Searches design data files to give actionable recommendations with hex codes, font pairings, layout patterns, component examples, and anti-pattern warnings.

Supports 260+ industry palettes, 57 font pairings, 750+ design rules, real 21st.dev component examples, and CT kit recommendations.

## Workflow

1. Identify the industry/product type from the user's request
2. Search relevant CSV data files in this skill's `data/` directory
3. Cross-reference with design vocabulary for proper terminology
4. Search 21st.dev for real component examples (if MCP `magic` server is available)
5. Check CT catalog for matching dashboard/UI kits
6. Present structured recommendations with implementation details

## Data Files

Search these CSV files in `data/` based on what the user needs:

- **colors.csv** — 260 industry color palettes (primary, secondary, CTA, bg, text, border)
- **typography.csv** — 57 font pairings with mood, use cases, Google Fonts links
- **ui-reasoning.csv** — 80+ industry design patterns, anti-patterns, severity levels
- **styles.csv** — 22 visual design styles with implementation details
- **landing.csv** — 30 landing page layout patterns and CTA strategies
- **ux-guidelines.csv** — 166 UX do/don't rules with code examples
- **charts.csv** — 31 data visualization recommendations by data type
- **creative-tim.csv** — 45 CT component/kit mappings by industry and use case

## How to Search

1. Read the relevant CSV files from `data/`
2. Filter rows matching the user's industry or product type (case-insensitive, partial match)
3. If no exact match, find the closest industry category
4. Combine results across files into a cohesive recommendation

## Output Format

Structure your response as:

### 1. Style Direction
Recommended visual style and why it fits this industry.

### 2. Color Palette
| Role | Hex | Usage |
|------|-----|-------|
| Primary | #hex | Headers, key UI elements |
| Secondary | #hex | Hover states, secondary buttons |
| CTA | #hex | Buttons, links needing attention |
| Background | #hex | Page background |
| Text | #hex | Body text |
| Border | #hex | Cards, dividers |

Include contrast ratio notes for accessibility (WCAG AA minimum).

### 3. Typography
- Heading font + Body font pairing
- Mood and why it fits
- Ready-to-use Google Fonts link
- Tailwind/CSS config snippet

### 4. Page Structure
Section order with CTA placement strategy. Reference `landing.csv` patterns.

### 5. Key Effects
Recommended animations and interactions (with CSS/Tailwind snippets).

### 6. Anti-Patterns
| Severity | What to Avoid | Why |
|----------|--------------|-----|
| HIGH | ... | ... |
| MEDIUM | ... | ... |

### 7. Component Examples
- **21st.dev**: Search for matching components using the `magic` MCP tool (if available). Show component names and links.
- **CT**: Recommend specific kits, templates, or components from `creative-tim.csv`.

### 8. Next Step
Suggest a concrete next action — e.g., "Use the design skill again with more specifics" or "Start building with these specs."

## Brand Override

If the user specifies brand colors, fonts, or constraints, respect those and adapt the recommendations around them. Example: "Design a SaaS dashboard but use our brand color #FF6B00" — use #FF6B00 as primary and build the palette around it.

## No Match Behavior

If the industry isn't in the data files, use the closest match and clearly state the substitution. Recommend the user add their industry to the CSV files for future accuracy.
