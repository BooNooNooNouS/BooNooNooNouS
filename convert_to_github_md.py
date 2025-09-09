#!/usr/bin/env python3
"""
Script to convert a markdown file to a GitHub-compatible markdown file
since GitHub doesn't support HTML with inline styles.
"""

import re
import argparse
import sys
from pathlib import Path
import create_svg


def remove_style_block(content):
    """Remove the entire <style> block."""
    style_pattern = r'<style>.*?</style>'
    return re.sub(style_pattern, '', content, flags=re.DOTALL)

def convert_company_table_to_markdown(company_table):
    """Convert the company table to markdown."""

    # Extract the company name, title, location, and timeline by using the span class names
    company_name = re.search(r'<span class="company-name">(.*?)</span>', company_table).group(1)
    title = re.search(r'<span class="position-title">(.*?)</span>', company_table).group(1)
    location = re.search(r'<span class="company-location">(.*?)</span>', company_table).group(1)
    timeline = re.search(r'<span class="position-timeline">(.*?)</span>', company_table).group(1)
    print("Found an entry for the company: ", company_name, title, location, timeline)

    # Create the SVG file
    filename = create_svg.main(company_name, title, location, timeline)

    markdown_link = f"![{company_name}](./{filename})"
    return markdown_link

def main():
    # Get the input and output files from the command line using argparse
    parser = argparse.ArgumentParser(description='Convert a resume file to GitHub-compatible markdown')
    parser.add_argument('--input_file', type=str, help='The input resume file')
    parser.add_argument('--output_file', type=str, help='The output resume file')
    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_file = Path(args.output_file)
    
    if not input_file.exists():
        print(f"Error: {input_file} not found!")
        sys.exit(1)
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process all of the company tables
    company_table_pattern = r'<!-- START_COMPANY_TABLE -->(.*?)<!-- END_COMPANY_TABLE -->'
    company_table_matches = re.finditer(company_table_pattern, content, re.DOTALL)
    
    # Process matches in reverse order to avoid index issues when replacing
    for match in reversed(list(company_table_matches)):
        full_match = match.group(0)  # The entire match including tags
        company_table_content = match.group(1)  # Just the content between tags
        
        print("Processing:", company_table_content.strip())
        # Convert the company table to markdown
        markdown_link = convert_company_table_to_markdown(company_table_content)
        content = content.replace(full_match, markdown_link)
    
    
    content = remove_style_block(content)
    
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully converted {input_file} to {output_file}")
    print("The file is now GitHub-compatible using standard markdown!")

if __name__ == '__main__':
    main()
