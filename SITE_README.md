# Temporal Design Patterns Website

This site is built with [Just the Docs](https://just-the-docs.github.io/just-the-docs/), a documentation theme for Jekyll.

## Local Development

### Prerequisites

- Ruby 2.7 or higher
- Bundler

### Setup

1. Install dependencies:
```bash
bundle install
```

2. Run the site locally:
```bash
bundle exec jekyll serve
```

3. Open http://localhost:4000/temporal-design-patterns in your browser

## Deployment

### GitHub Pages

1. Push to GitHub
2. Go to repository Settings > Pages
3. Set Source to "Deploy from a branch"
4. Select branch (usually `main`) and `/` (root)
5. Update `url` and `baseurl` in `_config.yml` to match your GitHub Pages URL

### Manual Build

```bash
bundle exec jekyll build
```

The site will be generated in the `_site/` directory.

## Structure

- `_config.yml` - Site configuration
- `index.md` - Homepage
- `*-patterns.md` - Category pages
- Individual pattern files with front matter for navigation
