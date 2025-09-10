# BooNooNooNouS

This repository contains Karla Nunez's resume in raw_resume.md, and tools to convert it to GitHub markdown as well as PDF.


## Scripts

### `convert_to_github_md.py`
Converts a markdown resume (raw_resume.md) to a GitHub-compatible format by replacing markdown tables and html tables with SVG images.
Example:
```bash
python convert_to_github_md.py --input_file raw_resume.md --output_file README.md
```


### `convert_to_pdf.py`
Converts a markdown file to PDF using the template.html and styles.css files.
Example:
```bash
python convert_to_pdf.py resume_github.md resume.pdf
```


## Development

This project includes a devcontainer configuration  wiwth all the necessary dependencies to run the project:

### Prereqs
- VSCode
- Docker
- Docker extension for VSCode
