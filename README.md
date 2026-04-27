# Vita Spire Product Showcase Website

A Hugo-based website showcasing Vita Spire's products across three specialized domains and marketing materials.

## Overview

This website features:
- **3 Product Categories**: Biomedical & Health Materials, Human Nutrition Solutions, Advanced Industrial Materials
- **Marketing Materials**: PDF flyers and brochures for download
- **Search**: Full-text product search powered by Fuse.js
- **Responsive Design**: Mobile-friendly with adaptive navigation

## Structure

### Content Organization
```
content/
├── _index.md                          # Homepage content
├── about/
│   └── index.md                       # About Us page
├── contact/
│   └── index.md                       # Contact Us page
├── marketing-materials/
│   ├── _index.md                      # Marketing Materials listing page
│   └── *.md                           # PDF flyer entries (links to static/pdf/)
└── products/
    ├── _index.md                      # Main products page
    ├── biomedical-health-materials/
    │   ├── _index.md                  # Category overview
    │   ├── bioactive-coating-materials/
    │   │   ├── _index.md              # Sub-category with table_columns config
    │   │   └── HAP3D-01.md            # Individual product
    │   ├── bioink-materials/
    │   ├── bone-repair-dental-filling-materials/
    │   ├── medical-aesthetic-subdermal-injection-materials/
    │   └── personal-care-materials/
    ├── human-nutrition-solutions/
    │   ├── _index.md
    │   ├── biopolysaccharides/
    │   ├── lipid-extracts/
    │   └── polypeptide-extracts/
    └── advanced-industrial-materials/
        ├── _index.md
        ├── carbon-nanotube/
        ├── graphene/
        ├── industrial-carbon-nanotube/
        └── others-carbon-materials/
```

### Layouts
```
layouts/
├── baseof.html                        # Base HTML template with shared styles
├── index.html                         # Homepage with carousel & category cards
├── index.json                         # Search index output for Fuse.js
├── about/
│   └── single.html                    # About Us page layout
├── contact/
│   └── single.html                    # Contact Us page layout
├── marketing-materials/
│   └── list.html                      # PDF card grid layout
├── products/
│   ├── list.html                      # Category/product table layout
│   └── single.html                    # Individual product detail layout
└── _partials/
    ├── site-navigation.html           # Navigation bar + search modal + mobile menu
    ├── site-footer.html               # Footer component
    ├── site-header-carousel.html      # Homepage image carousel
    └── site-favicon.html              # Favicon links
```

### Static Assets
```
static/
├── css/                               # Tailwind CSS, FontAwesome, custom fonts
├── images/
│   ├── categories/                    # Sub-category cover images
│   ├── products/                      # Product images (named by Cat. No.)
│   └── logo.png                       # Site logo
├── pdf/                               # Marketing material PDFs
└── js/
    └── fuse.min.js                    # Search library
```

## Adding New Products

To add a new product:

1. Create a new markdown file in the appropriate sub-category folder (e.g., `content/products/biomedical-health-materials/bioactive-coating-materials/NEW-PRODUCT.md`)
2. Add front matter with product details:
```yaml
---
title: "Product Full Name"
cat: "CAT-NO"                         # Catalog number (used for image lookup)
product_description: |
  Multi-line product description.
morphology_appearance: "White powder"
purity: "≥99.0%"
particle_size: "D50:~12µm"
features: |
  Key features summary
---
```
3. Add product images to `static/images/products/` named by catalog number (e.g., `CAT-NO.jpg` or `CAT-NO.png`)

## Adding New Marketing Materials

To add a new PDF flyer:

1. Place the PDF file in `static/pdf/your-flyer.pdf`
2. Create a markdown file in `content/marketing-materials/your-flyer.md`:
```yaml
---
title: "Flyer Title"
description: "Optional description"
pdf: "/pdf/your-flyer.pdf"
cover_image: "/images/marketing/your-flyer.png"  # Optional cover image
---
```
3. Optionally add a cover image to `static/images/marketing/`

## Adding New Product Categories

To add a new product sub-category:

1. Create a new folder under the appropriate category (e.g., `content/products/biomedical-health-materials/new-sub-category/`)
2. Create an `_index.md` file with category details:
```yaml
---
title: "New Sub-Category"
description: "Category description"
table_columns:                        # Optional: customize product table columns
  - key: "image"
    label: "Image"
  - key: "cat"
    label: "Cat. No."
  - key: "title"
    label: "Product Name"
  - key: "features"
    label: "Features"
---
```

## Running the Website

### Development Server
```bash
cd quickstart
hugo server -D
```

### Production Build
```bash
cd quickstart
hugo
```

The built site will be in the `public/` folder.

## Configuration

### Site Settings
Edit `hugo.toml` to change:
- Site title, description, base URL
- Navigation menu items and order
- Contact information (address, email, phone)
- Output formats

### Styling
The site uses a custom design with:
- **Tailwind CSS** for utility classes
- **Inter** and **Playfair Display** fonts
- **FontAwesome** icons
- Custom CSS embedded in `baseof.html`

Key style variables:
- Max content width: `1440px`
- Category colors: indigo, emerald, red, amber

## Features

- ✅ Homepage with product category cards and image carousel
- ✅ 3-level product hierarchy: Category → Sub-category → Product
- ✅ Product listing with customizable table columns
- ✅ Individual product detail pages with technical specifications
- ✅ Marketing Materials page with PDF download cards
- ✅ Full-text product search (Fuse.js)
- ✅ Responsive design with mobile hamburger menu
- ✅ About Us and Contact Us pages
- ✅ SEO optimized (OpenGraph, Schema, Sitemap, Canonical URLs)
- ✅ Auto-generated search index (`/index.json`)

## Deployment

The static site in the `public/` folder can be deployed to:
- GitHub Pages (configured via `.github/workflows/hugo.yaml`)
- Netlify
- Vercel
- Any static hosting service

