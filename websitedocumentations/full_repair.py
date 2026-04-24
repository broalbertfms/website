import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r"C:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia"

PAGES = [
    r"index.html",
    r"pages\about.html", r"pages\calendar.html", r"pages\champagnat.html",
    r"pages\contact.html", r"pages\links.html", r"pages\maristcommunities.html",
    r"pages\ministry.html", r"pages\news.html", r"pages\presence.html",
    r"pages\vocation.html",
    r"maristlinks\china.html", r"maristlinks\japan.html", r"maristlinks\malaysia.html",
    r"maristlinks\philippines.html", r"maristlinks\singapore.html", r"maristlinks\southkorea.html",
    r"vocation\aspirancy.html", r"vocation\formationteam.html", r"vocation\novitiate.html",
    r"vocation\scholasticate.html", r"vocation\vocationmaterials.html",
    r"vocation\vocationtalks.html",
    r"childsrights\childrensrights.html",
    r"maristlaity\maristlaity.html",
]

# The standard CSS block to restore (Phase 3 style)
STYLE_BLOCK = """    <style>
        .dropdown { position: relative; display: inline-block; }
        .dropdown:hover .dropdown-content { display: block !important; }
        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #ffffff;
            min-width: 200px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.1);
            z-index: 100;
            border-radius: 4px;
            top: 100%;
            left: 0;
        }
        .dropdown-content a {
            color: #1e3a5f;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            font-size: 14px;
            font-weight: 700;
        }
        .dropdown-content a:hover { background-color: #f1f1f1; color: #c41e3a; }
        .mobile-accordion-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }
        .mobile-accordion-header.active i { transform: rotate(180deg); }
        .dropbtn {
            background-color: transparent;
            color: #1e3a5f;
            padding: 16px;
            font-size: 14px;
            border: none;
            font-weight: 1000;
            cursor: pointer;
        }
    </style>"""

def repair_file(rel_path):
    filepath = os.path.join(BASE, rel_path)
    if not os.path.exists(filepath): return

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 1. Restore the <style> block if missing
    if '.mobile-accordion-content' not in content:
        content = content.replace('</head>', STYLE_BLOCK + '\n</head>')

    # 2. Repair the Mobile Menu Overlay Structure (The main source of "destruction")
    # We will look for the mobileMenuOverlay div and rebuild its internal accordions to be flat.
    
    overlay_match = re.search(r'(<div id="mobileMenuOverlay".*?)(<div class="flex flex-col h-full p-8 overflow-y-auto">)(.*?)(</div>\s*</div>\s*</div>\s*<main)', content, re.DOTALL)
    if not overlay_match:
        # Try finding by closer markers
        overlay_match = re.search(r'(<div id="mobileMenuOverlay".*?)(<div class="flex flex-col h-full p-8 overflow-y-auto">)(.*?)(</div>\s*</div>\s*</div>)', content, re.DOTALL)

    if overlay_match:
        prefix = overlay_match.group(1)
        inner_wrapper = overlay_match.group(2)
        inner_content = overlay_match.group(3)
        suffix = overlay_match.group(4)
        
        # Clean the inner content!
        # This is where the mismatched divs are.
        # We want to find each accordion and flatten it.
        
        # Pattern to find an accordion: <div class="mobile-accordion ..."> ... </div> (variable closing tags)
        # We'll use a more surgical approach: find every start and reset the endings.
        
        # a. Remove all the nested wrappers I added
        inner_content = inner_content.replace('<div class="mobile-accordion-content"><div class="flex flex-col gap-4 pl-4 pb-4 text-lg text-zinc-400">',
                                              '<div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg text-zinc-400">')
        inner_content = inner_content.replace('<div class="mobile-accordion-content"><div class="flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">',
                                              '<div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">')

        # b. Fix the closing tag madness
        # Every <div class="mobile-accordion ..."> should have exactly TWO closing </div> tags at the end of its content.
        # One for the content div, one for the accordion div.
        
        # Identify all accordion starts
        acc_starts = list(re.finditer(r'<div class="mobile-accordion[^"]*">', inner_content))
        
        new_inner = ""
        last_pos = 0
        for i in range(len(acc_starts)):
            start_match = acc_starts[i]
            # Copy text between last accordion and this one
            new_inner += inner_content[last_pos:start_match.start()]
            
            # Find the end of this accordion
            # It's either the next start or the end of the inner_content
            next_start = acc_starts[i+1].start() if i+1 < len(acc_starts) else len(inner_content)
            acc_block = inner_content[start_match.start():next_start]
            
            # Strip all closing </div> from this block and re-add exactly two at the logical end.
            # Logical end is before any trailing whitespace/newlines
            acc_block = acc_block.strip()
            # Remove all trailing </div>
            while acc_block.endswith('</div>'):
                acc_block = acc_block[:-6].strip()
            
            # Now we have the block from <div... to the last <a> or tag.
            # Re-add TWO closings.
            new_inner += acc_block + "\n                    </div>\n                </div>\n"
            last_pos = next_start
            
        new_inner += inner_content[last_pos:]
        
        # Replace the overlay in the full content
        content = content[:overlay_match.start(3)] + new_inner + content[overlay_match.end(3):]

    # Final sweep for any leftover triple-closes outside the overlay if they exist
    # but the overlay rebuilding should handle 99% of it.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[REPAIRED] {rel_path}")

for p in PAGES:
    repair_file(p)
