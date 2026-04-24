import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
apply_enhancements.py
Applies the global enhanced navigation, mobile overlay, and dark footer
to all pages that still use the old legacy template.
Reads each file completely before writing — never truncates.
"""

import os
import re
import sys

BASE = r"C:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia"

# All subdirectory pages use "../" as path prefix
PAGES = [
    # pages/
    r"pages\about.html",
    r"pages\calendar.html",
    r"pages\champagnat.html",
    r"pages\contact.html",
    r"pages\links.html",
    r"pages\maristcommunities.html",
    r"pages\ministry.html",
    r"pages\news.html",
    r"pages\presence.html",
    r"pages\vocation.html",
    # maristlinks/
    r"maristlinks\china.html",
    r"maristlinks\japan.html",
    r"maristlinks\malaysia.html",
    r"maristlinks\philippines.html",
    r"maristlinks\singapore.html",
    r"maristlinks\southkorea.html",
    # vocation/
    r"vocation\aspirancy.html",
    r"vocation\formationteam.html",
    r"vocation\novitiate.html",
    r"vocation\scholasticate.html",
    r"vocation\vocationmaterials.html",
    r"vocation\vocationtalks.html",
]

# ── ENHANCED HEAD ADDITIONS ─────────────────────────────────────────────────
HEAD_ADDITIONS = """    <script src="https://cdn.tailwindcss.com"></script>
    <style>
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

# ── NEW HEADER ───────────────────────────────────────────────────────────────
NEW_HEADER = """    <a href="#main-content"
       class="absolute left-4 top-4 z-[2000] -translate-y-20 bg-red-600 text-white px-6 py-3 rounded-md font-bold transition-transform focus:translate-y-0 focus:outline-none focus:ring-4 focus:ring-red-300">
       Skip to Main Content
    </a>

    <!-- Navigation Header -->
    <header class="bg-white sticky top-0 z-[1000] border-b border-zinc-200 shadow-sm">
        <div class="max-w-[1400px] mx-auto flex justify-between items-center px-8 py-2">
            <div class="logo flex items-center gap-3">
                <img src="https://i.postimg.cc/sxwDpNK0/eastasialogo2.png" alt="marist east asia logo" class="h-12 w-auto">
                <div class="logo-text text-xl font-bold text-[#1e3a5f]">MaristEastAsia</div>
            </div>
            <nav class="hidden lg:block">
                <ul class="flex items-center gap-4">
                    <li><a href="../index.html" class="text-[#1e3a5f] font-bold text-sm hover:text-[#c41e3a]">Home</a></li>
                    <li><a href="../pages/about.html" class="text-[#1e3a5f] font-bold text-sm hover:text-[#c41e3a]">About Us</a></li>

                    <div class="dropdown">
                        <button class="dropbtn">Vocation</button>
                        <div class="dropdown-content">
                            <a href="../pages/vocation.html">Formation Stages</a>
                            <a href="../vocation/formationteam.html">Formation Team</a>
                            <a href="../vocation/vocationtalks.html">Vocation Talks</a>
                            <a href="../vocation/vocationmaterials.html">Vocation Materials</a>
                            <a href="../vocation/aspirancy.html">Aspirancy Formation</a>
                            <a href="../vocation/novitiate.html">Novitiate Formation</a>
                            <a href="../vocation/scholasticate.html">Scholasticate Formation</a>
                        </div>
                    </div>

                    <div class="dropdown">
                        <button class="dropbtn">Ministry</button>
                        <div class="dropdown-content">
                            <a href="#">Marist Mission</a>
                            <a href="../pages/ministry.html">Schools and Non-Schools</a>
                            <a href="../youthministry/youthministry.html">Youth Ministry</a>
                            <a href="../maristvolunteer/maristvolunteer.html">Marist Volunteer</a>
                            <a href="../ecologyministry/ecologyministry.html">Ecology Ministry</a>
                        </div>
                    </div>

                    <li><a href="../pages/news.html" class="text-[#1e3a5f] font-bold text-sm hover:text-[#c41e3a]">News</a></li>

                    <div class="dropdown">
                        <button class="dropbtn">Champagnat</button>
                        <div class="dropdown-content">
                            <a href="../pages/champagnat.html">Charism</a>
                            <a href="#">Marist Spirituality</a>
                            <a href="#">Founding the Marist Brothers</a>
                            <a href="#">Champagnat's Vocation</a>
                        </div>
                    </div>

                    <div class="dropdown">
                        <button class="dropbtn">Presence</button>
                        <div class="dropdown-content">
                            <a href="../pages/maristcommunities.html">Marist Communities</a>
                            <a href="../childsrights/childrensrights.html">Child Rights</a>
                            <a href="../maristlaity/maristlaity.html">Marist Laity</a>
                        </div>
                    </div>

                    <div class="dropdown">
                        <button class="dropbtn">Media</button>
                        <div class="dropdown-content">
                            <a href="../pages/media.html">Videos</a>
                            <a href="../resources/documents.html">Documents</a>
                            <a href="../pages/calendar.html">Calendar</a>
                            <a href="../resources/newsletter.html">Newsletter</a>
                            <a href="../resources/archives.html">Archives</a>
                        </div>
                    </div>

                    <div class="dropdown">
                        <button class="dropbtn">Links</button>
                        <div class="dropdown-content">
                            <a href="../maristlinks/philippines.html">Marist Philippines</a>
                            <a href="../maristlinks/southkorea.html">Marist South Korea</a>
                            <a href="../maristlinks/japan.html">Marist Japan</a>
                            <a href="../maristlinks/malaysia.html">Marist Malaysia</a>
                            <a href="../maristlinks/singapore.html">Marist Singapore</a>
                            <a href="../maristlinks/china.html">Marist China</a>
                        </div>
                    </div>
                </ul>
            </nav>

            <!-- Mobile Hamburger Button -->
            <button id="mobileMenuBtn" aria-label="Open Navigation Menu" aria-expanded="false"
                class="lg:hidden w-12 h-12 flex items-center justify-center text-[#1e3a5f] active:bg-zinc-100 rounded-full transition-all focus:ring-2 focus:ring-[#1e3a5f]">
                <i class="fa-solid fa-bars text-2xl" aria-hidden="true"></i>
            </button>
        </div>
    </header>"""

# ── MOBILE MENU OVERLAY ──────────────────────────────────────────────────────
MOBILE_OVERLAY = """
    <!-- Mobile Menu Overlay -->
    <div id="mobileMenuOverlay" role="dialog" aria-modal="true" aria-label="Mobile Navigation"
        class="fixed inset-0 z-[2000] bg-black/95 backdrop-blur-md translate-x-full transition-transform duration-300 lg:hidden">
        <div class="flex flex-col h-full p-8 overflow-y-auto">
            <button id="closeMenuBtn" aria-label="Close Navigation Menu"
                class="self-end w-12 h-12 flex items-center justify-center text-white active:scale-90 transition-transform mb-8 focus:ring-2 focus:ring-white">
                <i class="fa-solid fa-xmark text-3xl" aria-hidden="true"></i>
            </button>
            <div class="flex flex-col gap-2 text-xl font-bold text-white mb-12">
                <a href="../index.html" class="py-3 border-b border-white/5 hover:text-red-500 transition-colors">Home</a>
                <a href="../pages/about.html" class="py-3 border-b border-white/5 hover:text-red-500 transition-colors">About Us</a>

                <!-- Vocation Accordion -->
                <div class="mobile-accordion border-b border-white/5">
                    <button class="mobile-accordion-header w-full flex justify-between items-center py-3 text-left hover:text-red-500 transition-colors" onclick="toggleAccordion(this)">
                        <span>Vocation</span>
                        <i class="fas fa-chevron-down text-sm transition-transform"></i>
                    </button>
                    <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
                        <a href="../pages/vocation.html">Formation Stages</a>
                        <a href="../vocation/formationteam.html">Formation Team</a>
                        <a href="../vocation/vocationtalks.html">Vocation Talks</a>
                        <a href="../vocation/vocationmaterials.html">Vocation Materials</a>
                        <a href="../vocation/aspirancy.html">Aspirancy Formation</a>
                        <a href="../vocation/novitiate.html">Novitiate Formation</a>
                        <a href="../vocation/scholasticate.html">Scholasticate Formation</a>
                    </div>
                </div>

                <!-- Ministry Accordion -->
                <div class="mobile-accordion border-b border-white/5">
                    <button class="mobile-accordion-header w-full flex justify-between items-center py-3 text-left hover:text-red-500 transition-colors" onclick="toggleAccordion(this)">
                        <span>Ministry</span>
                        <i class="fas fa-chevron-down text-sm transition-transform"></i>
                    </button>
                    <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
                        <a href="#">Marist Mission</a>
                        <a href="../pages/ministry.html">Schools and Non-Schools</a>
                        <a href="../youthministry/youthministry.html">Youth Ministry</a>
                        <a href="../maristvolunteer/maristvolunteer.html">Marist Volunteer</a>
                        <a href="../ecologyministry/ecologyministry.html">Ecology Ministry</a>
                    </div>
                </div>

                <a href="../pages/news.html" class="py-3 border-b border-white/5 hover:text-red-500 transition-colors">News</a>

                <!-- Champagnat Accordion -->
                <div class="mobile-accordion border-b border-white/5">
                    <button class="mobile-accordion-header w-full flex justify-between items-center py-3 text-left hover:text-red-500 transition-colors" onclick="toggleAccordion(this)">
                        <span>Champagnat</span>
                        <i class="fas fa-chevron-down text-sm transition-transform"></i>
                    </button>
                    <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
                        <a href="../pages/champagnat.html">Charism</a>
                        <a href="#">Marist Spirituality</a>
                        <a href="#">Founding the Marist Brothers</a>
                        <a href="#">Champagnat's Vocation</a>
                    </div>
                </div>

                <!-- Presence Accordion -->
                <div class="mobile-accordion border-b border-white/5">
                    <button class="mobile-accordion-header w-full flex justify-between items-center py-3 text-left hover:text-red-500 transition-colors" onclick="toggleAccordion(this)">
                        <span>Presence</span>
                        <i class="fas fa-chevron-down text-sm transition-transform"></i>
                    </button>
                    <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
                        <a href="../pages/maristcommunities.html">Marist Communities</a>
                        <a href="../childsrights/childrensrights.html">Child Rights</a>
                        <a href="../maristlaity/maristlaity.html">Marist Laity</a>
                    </div>
                </div>

                <!-- Media Accordion -->
                <div class="mobile-accordion border-b border-white/5">
                    <button class="mobile-accordion-header w-full flex justify-between items-center py-3 text-left hover:text-red-500 transition-colors" onclick="toggleAccordion(this)">
                        <span>Media</span>
                        <i class="fas fa-chevron-down text-sm transition-transform"></i>
                    </button>
                    <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
                        <a href="../pages/media.html">Videos</a>
                        <a href="../resources/documents.html">Documents</a>
                        <a href="../pages/calendar.html">Calendar</a>
                        <a href="../resources/newsletter.html">Newsletter</a>
                        <a href="../resources/archives.html">Archives</a>
                    </div>
                </div>

                <!-- Links Accordion -->
                <div class="mobile-accordion border-b border-white/5">
                    <button class="mobile-accordion-header w-full flex justify-between items-center py-3 text-left hover:text-red-500 transition-colors" onclick="toggleAccordion(this)">
                        <span>Related Links</span>
                        <i class="fas fa-chevron-down text-sm transition-transform"></i>
                    </button>
                    <div class="mobile-accordion-content flex flex-col gap-4 pl-4 pb-4 text-lg font-normal text-zinc-400">
                        <a href="../maristlinks/philippines.html">Marist Philippines</a>
                        <a href="../maristlinks/southkorea.html">Marist South Korea</a>
                        <a href="../maristlinks/japan.html">Marist Japan</a>
                        <a href="../maristlinks/malaysia.html">Marist Malaysia</a>
                        <a href="../maristlinks/singapore.html">Marist Singapore</a>
                        <a href="../maristlinks/china.html">Marist China</a>
                    </div>
                </div>

                <a href="../pages/contact.html" class="py-3 text-lg text-zinc-500">Contact Us</a>
            </div>
        </div>
    </div>

    <main id="main-content" tabindex="-1">"""

# ── MAIN CLOSE + NEW FOOTER + JS ─────────────────────────────────────────────
FOOTER_AND_JS = """    </main>

    <!-- Footer -->
    <footer class="bg-zinc-950 text-white pt-20 pb-10">
        <div class="max-w-[1400px] mx-auto px-8">
            <div class="grid md:grid-cols-4 gap-16 border-b border-white/10 pb-16">
                <!-- About Section -->
                <div class="space-y-6">
                    <h4 class="text-[#c41e3a] text-sm font-black uppercase tracking-widest">About Us</h4>
                    <p class="text-zinc-400 text-sm leading-relaxed font-medium">
                        The Marist Brothers of East Asia serve through education and pastoral ministry, continuing the legacy of St. Marcellin Champagnat, our Founder.
                    </p>
                    <div class="flex gap-4 pt-2">
                        <a href="https://www.facebook.com/profile.php?id=100083355408027" class="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center hover:bg-[#c41e3a] transition-all duration-300" target="_blank">
                            <i class="fab fa-facebook-f text-sm"></i>
                        </a>
                        <a href="#" class="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center hover:bg-[#c41e3a] transition-all duration-300">
                            <i class="fab fa-twitter text-sm"></i>
                        </a>
                        <a href="#" class="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center hover:bg-[#c41e3a] transition-all duration-300">
                            <i class="fab fa-instagram text-sm"></i>
                        </a>
                    </div>
                </div>

                <!-- Navigation -->
                <div class="space-y-6">
                    <h4 class="text-[#c41e3a] text-sm font-black uppercase tracking-widest">Navigation</h4>
                    <ul class="space-y-4">
                        <li><a href="../index.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">Home Portal</a></li>
                        <li><a href="../pages/about.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">About Our Mission</a></li>
                        <li><a href="../pages/vocation.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">Vocations</a></li>
                        <li><a href="../pages/news.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">Latest News</a></li>
                    </ul>
                </div>

                <!-- Resources -->
                <div class="space-y-6">
                    <h4 class="text-[#c41e3a] text-sm font-black uppercase tracking-widest">Resources</h4>
                    <ul class="space-y-4">
                        <li><a href="../pages/champagnat.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">St. Marcellin Champagnat</a></li>
                        <li><a href="../resources/documents.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">Public Documents</a></li>
                        <li><a href="../resources/newsletter.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">Regional Newsletter</a></li>
                        <li><a href="../pages/calendar.html" class="text-zinc-400 hover:text-white text-sm font-bold transition-colors">Events Calendar</a></li>
                    </ul>
                </div>

                <!-- Contact -->
                <div class="space-y-6">
                    <h4 class="text-[#c41e3a] text-sm font-black uppercase tracking-widest">Contact Info</h4>
                    <ul class="space-y-4">
                        <li class="flex gap-3 text-zinc-400 text-sm font-medium">
                            <i class="fas fa-map-marker-alt pt-1 text-[#c41e3a]"></i>
                            <span>Marist Brothers Province Center, NDDU-IBED Campus, Lagao, General Santos City, 9500 Philippines</span>
                        </li>
                        <li class="flex gap-3 text-zinc-400 text-sm font-medium">
                            <i class="fas fa-envelope pt-1 text-[#c41e3a]"></i>
                            <a href="mailto:info@maristeastasia.org" class="hover:text-white transition-colors">info@maristeastasia.org</a>
                        </li>
                        <li class="flex gap-3 text-zinc-400 text-sm font-medium">
                            <i class="fas fa-phone pt-1 text-[#c41e3a]"></i>
                            <a href="tel:(083) 552-5994" class="hover:text-white transition-colors">(083) 552-5994</a>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="pt-10 flex flex-col md:flex-row justify-between items-center gap-6">
                <p class="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-600 text-center md:text-left">
                    &copy; 2026 Marist Brothers of East Asia. All rights reserved.
                </p>
                <div class="flex gap-8 text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-600">
                    <a href="../websitedocumentations/dataprivacypolicy.html" class="hover:text-white transition-colors">Privacy Policy</a>
                    <a href="../websitedocumentations/termsofservice.html" class="hover:text-white transition-colors">Terms of Service</a>
                    <a href="../websitedocumentations/sitemap.html" class="hover:text-white transition-colors">Sitemap</a>
                </div>
            </div>
        </div>
    </footer>

    <div id="status-announcer" class="sr-only" aria-live="polite"></div>

    <script>
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

        mobileMenuBtn.onclick = () => toggleMobileMenu(true);
        closeMenuBtn.onclick = () => toggleMobileMenu(false);
        mobileMenuOverlay.querySelectorAll('a').forEach(link => {
            link.onclick = () => toggleMobileMenu(false);
        });
    </script>
    <script src="../assets/js/script.js"></script>"""


def has_old_template(content):
    return 'cdn.tailwindcss.com' not in content


def inject_head_additions(content):
    """Inject Tailwind + dropdown CSS before </head>"""
    return content.replace('</head>', HEAD_ADDITIONS + '\n</head>', 1)


def replace_header(content):
    """Replace old <header>...</header> block with enhanced header + skip link."""
    # Remove old skip-button if present
    content = re.sub(r'<a [^>]*Skip to Main Content[^>]*>.*?</a>', '', content, flags=re.DOTALL)
    # Replace old header block
    new = re.sub(
        r'<!-- Navigation Header -->\s*<header>.*?</header>',
        NEW_HEADER,
        content,
        flags=re.DOTALL
    )
    if new == content:
        # Fallback: replace header without comment
        new = re.sub(r'<header>.*?</header>', NEW_HEADER, content, flags=re.DOTALL)
    return new


def inject_mobile_overlay_and_main(content):
    """Insert mobile overlay + <main> wrapper after </header>."""
    return content.replace('</header>', '</header>' + MOBILE_OVERLAY, 1)


def replace_footer(content):
    """Replace old <footer>...</footer> and trailing script with new footer+JS."""
    # Remove old script tags at end
    content = re.sub(r'\s*<script src="[^"]*script\.js[^"]*"></script>', '', content)
    content = re.sub(r'\s*<script src="[^"]*cookieconsent[^"]*"></script>', '', content)
    # Replace old footer
    new = re.sub(
        r'<!-- Footer -->\s*<footer>.*?</footer>',
        FOOTER_AND_JS,
        content,
        flags=re.DOTALL
    )
    if new == content:
        new = re.sub(r'<footer>.*?</footer>', FOOTER_AND_JS, content, flags=re.DOTALL)
    return new


def close_main_before_footer(content):
    """Ensure </main> is before <footer class=..."""
    # Already added in FOOTER_AND_JS as "    </main>\n\n    <!-- Footer -->"
    return content


def fix_body_tag(content):
    """Update <body> to add bg-white font-sans classes if not already present."""
    content = re.sub(r'<body\b([^>]*)>', r'<body class="bg-white font-sans"\1>', content, count=1)
    # Avoid double class attrs
    content = re.sub(r'<body class="bg-white font-sans"([^>]*)\s+class="[^"]*"', r'<body class="bg-white font-sans"\1', content)
    return content


def close_body(content):
    """Make sure </body></html> is at the end."""
    content = content.rstrip()
    if not content.endswith('</html>'):
        content += '\n</body>\n</html>'
    return content


def process_file(filepath):
    print(f"\nProcessing: {filepath}")
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    if not has_old_template(content):
        print(f"  [SKIP] Already enhanced")
        return False

    original_size = len(content)
    content = inject_head_additions(content)
    content = replace_header(content)
    content = inject_mobile_overlay_and_main(content)
    content = replace_footer(content)
    content = fix_body_tag(content)
    content = close_body(content)

    if len(content) < original_size * 0.5:
        print(f"  [ERROR]: Output ({len(content)} bytes) is suspiciously smaller than input ({original_size} bytes). SKIPPING.")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] Done ({original_size} -> {len(content)} bytes)")
    return True


def main():
    updated = 0
    skipped = 0
    errors = 0

    for rel_path in PAGES:
        filepath = os.path.join(BASE, rel_path)
        if not os.path.exists(filepath):
            print(f"  [NOT FOUND]: {filepath}")
            errors += 1
            continue
        try:
            result = process_file(filepath)
            if result:
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  [EXCEPTION] on {filepath}: {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"COMPLETE: {updated} updated, {skipped} skipped, {errors} errors.")


if __name__ == '__main__':
    main()
