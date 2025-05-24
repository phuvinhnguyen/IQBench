# Markdown Site Generator

A beautiful, responsive website generator that converts markdown files into a modern website. Built with Jekyll, this project provides a clean and customizable way to showcase your markdown content.

## Features

- Convert markdown files to beautiful web pages
- Support for images, code blocks, tables, and more
- Responsive design that works on all devices
- Smooth animations and transitions
- Syntax highlighting for code blocks
- Customizable styling
- Easy navigation between posts
- SEO optimized

## Prerequisites

- Ruby (version 2.5.0 or higher)
- RubyGems
- Bundler

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd markdown-site
```

2. Install dependencies:
```bash
bundle install
```

## Usage

1. Add your markdown files to the `_posts` directory. Files should be named in the format: `YYYY-MM-DD-title.md`

2. Each markdown file should include front matter at the top:
```yaml
---
layout: post
title: Your Post Title
author: Your Name
date: YYYY-MM-DD
---
```

3. To run the site locally:
```bash
bundle exec jekyll serve
```

4. Visit `http://localhost:4000` in your browser to see your site.

## Customization

### Styling

- Edit `assets/css/main.css` to customize the site's appearance
- Modify `_layouts/default.html` to change the site structure
- Update `_config.yml` to change site-wide settings

### Adding New Posts

1. Create a new markdown file in the `_posts` directory
2. Use the front matter format shown above
3. Write your content using markdown syntax
4. Link to other posts using relative links: `[Link Text](post-filename.md)`

## Deployment

This site can be easily deployed to GitHub Pages:

1. Create a new repository on GitHub
2. Push your code to the repository
3. Enable GitHub Pages in the repository settings
4. Select the main branch as the source

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 