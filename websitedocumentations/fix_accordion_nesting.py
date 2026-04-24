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

    # FIX MISSING CLOSING DIV from previous script run
    # Previous run produced Pattern:
    # <div class="mobile-accordion-content"><div class="...">...links...</div>
    # We need:
    # <div class="mobile-accordion-content"><div class="...">...links...</div></div>
    
    # We find mobile-accordion-content divs and ensure they have TWO closing tags before the next sibling/container
    # Actually, let's just use a more surgical replace
    
    # Identify the specific blocks
    # We search for <div class="mobile-accordion-content"><div class="flex...
    # and look for the transition to the next block (usually <!-- or </div> or <a )
    
    # A safer way: replace the whole accordion content block with a standardized one.
    # But links are different in each.
    
    # Let's fix the logic:
    # Any <div class="mobile-accordion-content"><div class="..."> that ends with only one </div> before a comment or next div needs another one.
    
    # Actually, I can just do a very specific find/replace since I know exactly what I injected.
    
    # 1. Clean up the messy inject if it happened
    content = content.replace('<div class="mobile-accordion-content"><div class="flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">',
                              'TARGET_OPEN')
    content = content.replace('<div class="mobile-accordion-content"><div class="flex flex-col gap-4 pl-4 pb-4 text-lg text-zinc-400">',
                              'TARGET_OPEN')
    
    # Now find the end of that block.
    # It usually ends with some links then </div>
    # We want it to be </div></div>
    
    # Regex to find TARGET_OPEN ... </div> and make it TARGET_OPEN ... </div></div>
    # ONLY if it's not already closed twice.
    
    # Let's just fix the whole thing properly.
    def fix_nesting(m):
        inner_content = m.group(2)
        # remove any trailing extra divs if I run this multiple times
        inner_content = inner_content.strip()
        return f'<div class="mobile-accordion-content"><div class="{m.group(1)}">{inner_content}</div></div>'

    pattern = re.compile(r'TARGET_OPEN(.*?)(?=\s*</div>\s*(?:<!--|</div>|$))', re.DOTALL)
    # Wait, that regex is getting complex.
    
    # Let's use a simpler approach:
    # Scan for `mobile-accordion-content` and rebuild it.
    
    pass

# Standardize the script again but correctly this time
for p in PAGES:
    filepath = os.path.join(BASE, p)
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    # Fix the broken nesting from the first attempt
    # We look for the pattern I pushed: <div class="mobile-accordion-content"><div class="...">
    # and we find the corresponding </div> and add another one.
    
    # Surgery:
    new_c = re.sub(r'<div class="mobile-accordion-content"><div class="([^"]*)">(.*?)</div>\s*(?=</div>|\s*<!--)', 
                   r'<div class="mobile-accordion-content"><div class="\1">\2</div></div>', 
                   c, flags=re.DOTALL)
    
    if new_c != c:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f"[RE-FIXED] {p}")
    else:
        print(f"[NO BREAK DETECTED or ALREADY FIXED] {p}")

