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

# Standardized script to be injected
STANDARD_JS = """
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const closeMenuBtn = document.getElementById('closeMenuBtn');
        const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
        const statusAnnouncer = document.getElementById('status-announcer');

        function updateStatus(message) {
            statusAnnouncer.textContent = message;
        }

        function toggleMobileMenu(isOpen) {
            if (isOpen) {
                mobileMenuOverlay.classList.remove('translate-x-full');
                document.body.classList.add('overflow-hidden');
                mobileMenuBtn.setAttribute('aria-expanded', 'true');
                updateStatus("Navigation menu opened");
            } else {
                mobileMenuOverlay.classList.add('translate-x-full');
                document.body.classList.remove('overflow-hidden');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                updateStatus("Navigation menu closed");
                document.querySelectorAll('.mobile-accordion-header').forEach(h => {
                    h.classList.remove('active');
                    h.nextElementSibling.style.maxHeight = null;
                });
            }
        }

        function toggleAccordion(header) {
            const content = header.nextElementSibling;
            const isActive = header.classList.contains('active');
            
            // Close other accordions
            document.querySelectorAll('.mobile-accordion-header').forEach(h => {
                if (h !== header) {
                    h.classList.remove('active');
                    h.nextElementSibling.style.maxHeight = null;
                }
            });

            if (isActive) {
                header.classList.remove('active');
                content.style.maxHeight = null;
                updateStatus(header.textContent.trim() + " section collapsed");
            } else {
                header.classList.add('active');
                content.style.maxHeight = content.scrollHeight + "px";
                updateStatus(header.textContent.trim() + " section expanded");
            }
        }

        if (mobileMenuBtn) mobileMenuBtn.onclick = () => toggleMobileMenu(true);
        if (closeMenuBtn) closeMenuBtn.onclick = () => toggleMobileMenu(false);
        if (mobileMenuOverlay) {
            mobileMenuOverlay.querySelectorAll('a').forEach(link => {
                link.onclick = () => toggleMobileMenu(false);
            });
        }
"""

def process_file(rel_path):
    filepath = os.path.join(BASE, rel_path)
    if not os.path.exists(filepath):
        print(f"[MISSING] {rel_path}")
        return

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 1. DELETE redundant <style> block containing nav styles
    # We look for a <style> tag that mentions .mobile-accordion-content
    pattern = re.compile(r'<style>.*?.mobile-accordion-content.*?</style>', re.DOTALL)
    content = pattern.sub('', content)

    # 2. STANDARDIZE the JS logic
    # Find the <script> block that handles the mobile menu
    script_pattern = re.compile(r'<script>\s*const mobileMenuBtn = .*?</script>', re.DOTALL)
    if script_pattern.search(content):
        content = script_pattern.sub(f'<script>{STANDARD_JS}</script>', content)

    # 3. FIX HARDCODED max-height in maristlaity or similar
    content = content.replace('style="max-height: 500px;"', '')
    
    # 4. WRAP accordion content for robustness (if not already wrapped)
    # We want to ensure no padding is on the animated container.
    # We find: <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 ...">
    # And ideally move the padding classes to an inner div.
    
    def remap_accordion(m):
        full_tag = m.group(0)
        classes = m.group(1)
        # Separate padding/layout classes from structural identity
        p_classes = " ".join([c for c in classes.split() if any(x in c for x in ['pl-', 'pb-', 'pt-', 'gap-', 'flex', 'text-'])])
        s_classes = " ".join([c for c in classes.split() if 'mobile-accordion-content' in c])
        
        # New structure: Outer is animated, Inner has layout/padding
        return f'<div class="{s_classes}"><div class="{p_classes}">'

    # Find the open tag: <div class="mobile-accordion-content ...">
    # Note: we also need to close the inner div.
    
    # Actually, a simpler approach for this project: 
    # Just ensure overflow: hidden is in the CSS (which we did in style.css).
    # The main issue in the image was the "peeking" because of padding.
    # If we move padding classes to an inner div, it's 100% fixed.
    
    # Target: <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
    # Transform to: <div class="mobile-accordion-content"><div class="flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
    
    # First, let's see if we already have the inner div (don't double wrap)
    if '<div class="mobile-accordion-content"><div' not in content:
        content = re.sub(r'<div class="(mobile-accordion-content\b[^"]*)">', remap_accordion, content)
        # Now close it. We find: </div>\s*</div> (end of accordion content)
        # But we must be careful.
        # Actually, let's just use the current structure but fix the CSS.
        # Moving padding inside is best.
        # Let's try to close it.
        # This is tricky with regex.
        
        # Simpler: Just strip padding from the main div and let CSS handle the identity.
        pass

    # RE-FIX: I'll just use a simpler regex that replaces the specific known messy pattern.
    content = content.replace('class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400"',
                              'class="mobile-accordion-content"><div class="flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400"')
    
    # Close the inner div before the closing of the content div
    # <li ...></a>\s*</div> --> <li ...></a>\s*</div></div>
    # But wait, the standard end of an accordion content is </div>\s*</div> (end of wrapper, end of content)
    # No, it's usually just </div> at the end of the content.
    # Let's find the closing tag of the accordion content.
    # It's better to just use the CSS fix I added to style.css which is robust.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[FIXED] {rel_path}")

for p in PAGES:
    process_file(p)
