#!/usr/bin/env python3
"""
Script to convert a markdown file to PDF while preserving hyperlinks.
Uses markdown2, weasyprint, and custom CSS to ensure links are clickable in the PDF.
"""

import argparse
import sys
import re
import base64
from pathlib import Path
import markdown2
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def convert_markdown_to_pdf(input_file, output_file, css_file=None):
    """
    Convert a markdown file to PDF while preserving hyperlinks.
    
    Args:
        input_file (Path): Path to the input markdown file
        output_file (Path): Path to the output PDF file
        css_file (Path, optional): Path to custom CSS file for styling
    """
    
    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML with extras for better formatting
    html_content = markdown2.markdown(
        markdown_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'toc',
            'target-blank-links'
        ],
    )
    
    # Convert relative image paths to base64 data URIs for embedding
    base_dir = input_file.parent.absolute()

    def replace_img_src(match):
        src = match.group(1)
        if (src.startswith('./') or
                (not src.startswith('http') and not src.startswith('/'))):
            # If the path is relative, embed the content of the file as a base64 data URI
            if src.startswith('./'):
                src = src[2:]  # Remove './'
            absolute_path = base_dir / src
            
            try:
                # Read the image file and convert to base64
                with open(absolute_path, 'rb') as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                    
                    # Determine MIME type based on file extension
                    ext = absolute_path.suffix.lower()
                    if ext == '.svg':
                        mime_type = 'image/svg+xml'
                    elif ext == '.png':
                        mime_type = 'image/png'
                    elif ext == '.jpg' or ext == '.jpeg':
                        mime_type = 'image/jpeg'
                    elif ext == '.gif':
                        mime_type = 'image/gif'
                    else:
                        mime_type = 'image/png'  # default
                    
                    data_uri = f'data:{mime_type};base64,{img_base64}'
                    print(f"Embedding {src} as base64 data URI")
                    return f'src="{data_uri}"'
                    
            except Exception as e:
                print(f"Warning: Could not embed image {src}: {e}")
                return match.group(0)  # Return original if embedding fails
                
        return match.group(0)

    # Replace relative image paths with base64 data URIs
    html_content = re.sub(r'src="([^"]+)"', replace_img_src, html_content)
    
    # Load HTML template
    template_file = input_file.parent / 'template.html'
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        full_html = template_content.replace('{content}', html_content)
    else:
        # Fallback to inline template if external template not found
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
    
    # Load CSS styles
    css_styles = []
    
    # Load default styles.css if it exists
    default_css_file = input_file.parent / 'styles.css'
    if default_css_file.exists():
        with open(default_css_file, 'r', encoding='utf-8') as f:
            css_styles.append(CSS(string=f.read()))
    
    # Load custom CSS if provided
    if css_file and css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            css_styles.append(CSS(string=f.read()))
    
    # Create font configuration for better text rendering
    font_config = FontConfiguration()
    
    # Generate PDF
    try:
        html_doc = HTML(string=full_html)
        html_doc.write_pdf(
            output_file,
            stylesheets=css_styles,
            font_config=font_config
        )
        print(f"Successfully converted {input_file} to {output_file}")
        print("Hyperlinks have been preserved and should be clickable in the PDF")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert a markdown file to PDF'
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='The input markdown file'
    )
    parser.add_argument(
        'output_file',
        type=str,
        help='The output PDF file'
    )
    parser.add_argument(
        '--css',
        type=str,
        help='Optional custom CSS file for styling'
    )
    
    args = parser.parse_args()
    
    input_file = Path(args.input_file)
    output_file = Path(args.output_file)
    css_file = Path(args.css) if args.css else None
    
    # Validate input file
    if not input_file.exists():
        print(f"Error: {input_file} not found!")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert markdown to PDF
    convert_markdown_to_pdf(input_file, output_file, css_file)


if __name__ == '__main__':
    main()

