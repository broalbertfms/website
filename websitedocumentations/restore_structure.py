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

def process_file(rel_path):
    filepath = os.path.join(BASE, rel_path)
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # REVERT: Remove the nested wrapper <div class="mobile-accordion-content"><div class="...">
    # and restore the flat structure
    
    # 1. Simplify the open tag
    # Match: <div class="mobile-accordion-content"><div class="(flex [^"]*)">
    # Replace: <div class="mobile-accordion-content \1">
    content = re.sub(r'<div class="mobile-accordion-content"><div class="([^"]*)">',
                     r'<div class="mobile-accordion-content \1">',
                     content)
    
    # 2. Fix the broken closing tags
    # The previous script might have added </div></div> or </div></div></div>
    # We want exactly ONE closing </div> for the content block.
    # Currently, most look like: </div></div></div> (inner-div, content-div, parent-div)
    # We want it to be </div> (content-div) and then let the existing parent-div </div> handle the rest.
    
    # Surgical fix for the pattern I pushed: 
    # Find links then </div></div></div> (when followed by <!-- or <div or <a in the parent)
    content = content.replace('</div></div></div>', '</div></div>') # Revert one level
    # Actually, let's just use the DIV mismatch scan as a guide or use a more holistic approach.
    
    # Safer approach: replace </div></div> with </div> if it's inside a mobile-accordion
    # But that's hard with regex.
    
    # Let's target the exact messed up pattern from vocation.html view:
    # 203: </div></div></div>
    # followed by whitespaces then 205: <a ... (next sibling link)
    
    content = re.sub(r'</div></div></div>(\s*<a href="[^"]*")', r'</div>\1', content)
    content = re.sub(r'</div></div>(\s*<a href="[^"]*")', r'</div>\1', content)

    # Specific fix for Champagnat and others found in scan
    # Let's just fix the mismatched counts by adding/removing at the end of known problematic blocks.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[REVERTED] {rel_path}")

for p in PAGES:
    process_file(p)
