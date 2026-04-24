import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r"C:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia"

PAGES = [
    r"pages\calendar.html", r"pages\champagnat.html", r"pages\contact.html",
    r"pages\links.html", r"pages\maristcommunities.html", r"pages\ministry.html",
    r"pages\news.html", r"pages\presence.html", r"pages\vocation.html",
    r"maristlinks\china.html", r"maristlinks\japan.html", r"maristlinks\malaysia.html",
    r"maristlinks\philippines.html", r"maristlinks\singapore.html", r"maristlinks\southkorea.html",
    r"vocation\aspirancy.html", r"vocation\formationteam.html", r"vocation\novitiate.html",
    r"vocation\scholasticate.html", r"vocation\vocationmaterials.html", r"vocation\vocationtalks.html",
]


def upgrade_breadcrumb(content):
    """
    Upgrade old-style breadcrumb to Tailwind style matching maristlaity.html.
    Transforms:
      <div class="breadcrumb">
        <div class="container">
          <ul>
            <li><a href="../index.html">Home</a></li>
            <li><span>PageName</span></li>   (or intermediate links)
          </ul>
        </div>
      </div>
    Into maristlaity Tailwind style.
    """
    # Step 1: Find the entire breadcrumb block
    breadcrumb_pat = re.compile(
        r'(<div\s+class="breadcrumb">\s*<div\s+class="container">\s*<ul>)(.*?)(</ul>\s*</div>\s*</div>)',
        re.DOTALL
    )

    def transform_breadcrumb(m):
        inner = m.group(2)  # the <li>...</li> content

        # Parse all list items
        items = re.findall(r'<li>(.*?)</li>', inner, re.DOTALL)
        new_items = []

        for i, item in enumerate(items):
            item = item.strip()
            is_last = (i == len(items) - 1)

            if is_last:
                # Current page — extract text from <span> or <a>
                span_m = re.search(r'<span>(.*?)</span>', item, re.DOTALL)
                a_m = re.search(r'<a[^>]*>(.*?)</a>', item, re.DOTALL)
                text = (span_m or a_m).group(1).strip() if (span_m or a_m) else item

                if new_items:  # Add chevron separator
                    new_items.append('                    <li><i class="fas fa-chevron-right text-[8px] opacity-30"></i></li>')
                new_items.append(f'                    <li class="text-[#c41e3a]">{text}</li>')
            else:
                # Intermediate item — keep as link or plain
                a_m = re.search(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', item, re.DOTALL)
                if a_m:
                    href = a_m.group(1)
                    text = a_m.group(2).strip()
                    if new_items:
                        new_items.append('                    <li><i class="fas fa-chevron-right text-[8px] opacity-30"></i></li>')
                    new_items.append(f'                    <li><a href="{href}" class="hover:text-[#c41e3a] transition-colors">{text}</a></li>')
                else:
                    if new_items:
                        new_items.append('                    <li><i class="fas fa-chevron-right text-[8px] opacity-30"></i></li>')
                    new_items.append(f'                    <li>{item}</li>')

        new_inner = '\n'.join(new_items)

        return (
            '<div class="breadcrumb bg-zinc-50 border-b border-zinc-200 py-4">\n'
            '            <div class="max-w-[1400px] mx-auto px-8">\n'
            '                <ul class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-zinc-400">\n'
            + new_inner + '\n'
            '                </ul>\n'
            '            </div>\n'
            '        </div>'
        )

    new_content = breadcrumb_pat.sub(transform_breadcrumb, content)
    return new_content


updated = 0
skipped = 0
errors = 0

for rel_path in PAGES:
    filepath = os.path.join(BASE, rel_path)
    if not os.path.exists(filepath):
        print(f"[NOT FOUND] {filepath}")
        errors += 1
        continue

    with open(filepath, encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content
    new_content = upgrade_breadcrumb(content)

    if new_content == original:
        print(f"[SKIP - no old breadcrumb found] {rel_path}")
        skipped += 1
        continue

    if len(new_content) < len(original) * 0.5:
        print(f"[ERROR - output too small] {rel_path}")
        errors += 1
        continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] {rel_path}")
    updated += 1

print(f"\nDone: {updated} updated, {skipped} skipped, {errors} errors.")
