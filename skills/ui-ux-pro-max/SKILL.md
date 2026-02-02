# UI UX Pro Max

AI-powered design intelligence toolkit for building professional UI/UX across multiple platforms and frameworks.

## 🎯 What This Skill Does

Provides searchable databases of:
- **100+ Product Types** - Industry-specific design recommendations
- **67 UI Styles** - From glassmorphism to brutalism with AI prompts and CSS keywords
- **96 Color Palettes** - Organized by product type and mood
- **Font Pairings** - Curated typography with Google Fonts imports
- **24 Landing Page Patterns** - Conversion-optimized structures
- **Chart Types** - Data visualization recommendations
- **UX Best Practices** - Guidelines and anti-patterns

## 🔍 Search Command

### Domain Search
```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

**Available Domains:**
- `product` - Product type recommendations (SaaS, e-commerce, portfolio, etc.)
- `style` - UI styles with AI prompts and CSS keywords
- `typography` - Font pairings with Google Fonts imports
- `color` - Color palettes by product type
- `landing` - Page structure and CTA strategies
- `chart` - Chart types and library recommendations
- `ux` - Best practices and anti-patterns

**Examples:**
```bash
# Find styles for a wellness app
python3 src/ui-ux-pro-max/scripts/search.py "spa wellness" --domain style

# Get color palettes for e-commerce
python3 src/ui-ux-pro-max/scripts/search.py "e-commerce" --domain color

# Find font pairings for luxury brand
python3 src/ui-ux-pro-max/scripts/search.py "luxury elegant" --domain typography
```

### Stack-Specific Search
```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>
```

**Available Stacks:**
- `html-tailwind` (default)
- `react`, `nextjs`, `astro`
- `vue`, `nuxtjs`, `nuxt-ui`
- `svelte`, `sveltekit`
- `shadcn`
- `swiftui`, `react-native`, `flutter`, `jetpack-compose`

**Example:**
```bash
# Get React-specific guidelines
python3 src/ui-ux-pro-max/scripts/search.py "button component" --stack react
```

### Auto-Detection
Omit `--domain` to let the system auto-detect the domain:
```bash
python3 src/ui-ux-pro-max/scripts/search.py "minimalist design"
```

## 🎨 Design System Generator

The flagship feature - generates complete, tailored design systems based on project requirements.

**What It Generates:**
- Landing page pattern (Hero-Centric, Feature-First, etc.)
- UI style recommendation (Soft UI, Glassmorphism, etc.)
- Color palette (Primary, Secondary, CTA, Background, Text)
- Typography pairing with Google Fonts links
- Key effects and animations
- Anti-patterns to avoid
- Pre-delivery checklist

**Example Output:**
```
TARGET: Serenity Spa - RECOMMENDED DESIGN SYSTEM

PATTERN: Hero-Centric + Social Proof
  Conversion: Emotion-driven with trust elements
  Sections: Hero → Services → Testimonials → Booking → Contact

STYLE: Soft UI Evolution
  Keywords: Soft shadows, subtle depth, calming, premium feel
  Best For: Wellness, beauty, lifestyle brands

COLORS:
  Primary:    #E8B4B8 (Soft Pink)
  Secondary:  #A8D5BA (Sage Green)
  CTA:        #D4AF37 (Gold)
  Background: #FFF5F5 (Warm White)
  Text:       #2D3436 (Charcoal)

TYPOGRAPHY: Cormorant Garamond / Montserrat
  Mood: Elegant, calming, sophisticated
  Google Fonts: https://fonts.google.com/share?selection.family=...

PRE-DELIVERY CHECKLIST:
  [ ] No emojis as icons (use SVG: Heroicons/Lucide)
  [ ] cursor-pointer on all clickable elements
  [ ] Hover states with smooth transitions (150-300ms)
  [ ] Text contrast 4.5:1 minimum
  [ ] Responsive: 375px, 768px, 1024px, 1440px
```

## 📁 Architecture

```
.windsurf/skills/ui-ux-pro-max/
├── SKILL.md                      # This file
├── CLAUDE.md                     # Claude Code compatibility
├── README.md                     # Full documentation
├── src/ui-ux-pro-max/            # Source of Truth
│   ├── data/                     # CSV databases
│   │   ├── products.csv          # 100+ product types
│   │   ├── styles.csv            # 67 UI styles
│   │   ├── colors.csv            # 96 color palettes
│   │   ├── typography.csv        # Font pairings
│   │   ├── landing.csv           # Landing page patterns
│   │   ├── charts.csv            # Chart types
│   │   ├── ux.csv                # UX guidelines
│   │   └── stacks/               # Stack-specific guidelines
│   ├── scripts/
│   │   ├── search.py             # CLI entry point
│   │   ├── core.py               # BM25 + regex search engine
│   │   └── design_system.py      # Design system generator
│   └── templates/
│       ├── base/                 # Base templates
│       └── platforms/            # Platform configs
└── cli/                          # NPM CLI installer (uipro-cli)
```

## 🚀 Usage Workflow

### 1. Search for Design Elements
```bash
# Find UI style
python3 src/ui-ux-pro-max/scripts/search.py "modern minimalist" --domain style

# Find color palette
python3 src/ui-ux-pro-max/scripts/search.py "fintech" --domain color

# Find typography
python3 src/ui-ux-pro-max/scripts/search.py "professional corporate" --domain typography
```

### 2. Generate Design System
Use the search results to inform your design decisions, or let the system generate a complete design system based on the project type.

### 3. Apply to Your Stack
Use stack-specific search to get implementation guidelines:
```bash
python3 src/ui-ux-pro-max/scripts/search.py "button styles" --stack react
```

## 🔧 Prerequisites

- Python 3.x (no external dependencies required)
- The search engine uses BM25 ranking + regex matching

## 📝 Key Features

### Intelligent Search
- **BM25 Ranking** - Industry-standard text search algorithm
- **Regex Matching** - Pattern-based keyword detection
- **Auto-Detection** - Automatically determines search domain
- **Multi-Domain** - Search across all databases simultaneously

### Design Intelligence
- **Product-Aware** - Recommendations based on industry and product type
- **Style Matching** - AI prompts and CSS keywords for each style
- **Color Psychology** - Palettes organized by mood and product type
- **Typography Pairing** - Pre-tested font combinations with Google Fonts
- **Conversion-Optimized** - Landing page patterns proven to convert

### Stack Support
- **Multi-Framework** - Support for 13+ frameworks and platforms
- **Best Practices** - Stack-specific guidelines and patterns
- **Component Libraries** - Integration with shadcn, Nuxt UI, etc.

## ⚠️ Important Notes

1. **Source of Truth**: Always edit files in `src/ui-ux-pro-max/`, not in CLI assets
2. **No External Dependencies**: Pure Python 3.x, no pip install needed
3. **Search Results**: Use `-n` flag to limit results (default varies by domain)
4. **Design System**: Generated systems are starting points - customize for your needs

## 🔗 Related Resources

- **Full Documentation**: See `README.md` for complete feature list
- **CLI Tool**: `npm install -g uipro-cli` for easy installation
- **GitHub**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

## 📊 Database Stats

- **100** Product type recommendations
- **67** UI styles with AI prompts
- **96** Color palettes
- **24** Landing page patterns
- **13+** Supported frameworks/platforms
- **100+** UX best practices and anti-patterns

## 🎯 When to Use This Skill

Use this skill when you need to:
- Choose a UI style for a new project
- Find color palettes that match your product type
- Get font pairing recommendations
- Design a landing page structure
- Select appropriate chart types for data visualization
- Follow UX best practices
- Get stack-specific implementation guidelines
- Generate a complete design system quickly

## 💡 Pro Tips

1. **Start with Product Type**: Search by product type first to get industry-specific recommendations
2. **Combine Searches**: Use multiple domain searches to build a complete design system
3. **Check Anti-Patterns**: Always review the "avoid" section to prevent common mistakes
4. **Use Stack Search**: Get implementation details specific to your framework
5. **Customize Results**: Treat search results as starting points, not final solutions
