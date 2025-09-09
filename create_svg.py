#!/usr/bin/env python3
"""
Script to convert RESUME.md to GH_RESUME.md by inlining CSS styles
and removing the <style> block for GitHub compatibility.
"""

import re
import argparse
import sys
from pathlib import Path

FONT_COLOR = "#00A0FA"
Y_POSITION = "28"

# all keys in the form a_b will be converted to a-b in the SVG
definitions = {
    "company": {
        "font_size": "32",
        "font_weight": "bold",
        "text_anchor": "start",
        "fill": FONT_COLOR,
        "y": Y_POSITION,
        "x": "0",
    },
    "title": {
        "font_size": "12.8",
        "font_style": "italic",
        "text_anchor": "middle",
        "fill": FONT_COLOR,
        "y": Y_POSITION,
        "x": "50%",
    },
    "location": {
        "font_size": "12.8",
        "text_anchor": "end",
        "fill": FONT_COLOR,
        "y": Y_POSITION,
        "x": "85%",
    },
    "timeline": {
        "font_size": "12.8",
        "text_anchor": "end",
        "fill": FONT_COLOR,
        "y": Y_POSITION,
        "x": "100%",
    }
}

def get_svg_text_content(definition, content):

    groupped_values = " ".join([f"""{k.replace("_", "-")}=\"{v}\"""" for k,v in definition.items()])
    return f'<text {groupped_values}>{content}</text>'

    

def main():
    # Get the input and output files from the command line using argparse
    parser = argparse.ArgumentParser(description='Convert a resume file to a GitHub compatible format')
    parser.add_argument('--company', type=str, help='Name of the company', required=True)
    parser.add_argument('--title', type=str, help='Title held', required=True)
    parser.add_argument('--location', type=str, help='Location of the company', required=True)
    parser.add_argument('--timeline', type=str, help='Employment timeline', required=True)
    args = parser.parse_args()

    filename = f"{args.company}_{args.title}.svg".lower().replace(" ", "_")
    
    if Path(filename).exists():
        print(f"Replacing existing file: {filename}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Example SVG:
#         <svg width="100%" height="40">
#   <text x="0" y="28" font-size="32" font-weight="bold">Redfin</text>
#   <text x="50%" y="28" font-style="italic" text-anchor="middle">Technical Lead</text>
#   <text x="75%" y="28" font-size="12.8" text-anchor="end">Seattle, WA, USA</text>
#   <text x="100%" y="28" font-size="12.8" text-anchor="end">01/19 - 11/24</text>
# </svg>

        f.write(f'<svg width="100%" height="40" viewBox="0 0 600 40" xmlns="http://www.w3.org/2000/svg">')
        for definition_name, definition in definitions.items():
            content = getattr(args, definition_name)
            f.write(get_svg_text_content(definition, content))
            
        f.write(f"""
        </svg>""")
        
    print(f"Successfully created {filename}")

if __name__ == '__main__':
    main()
