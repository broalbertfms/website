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

updated = 0
skipped = 0

for rel_path in PAGES:
    filepath = os.path.join(BASE, rel_path)
    if not os.path.exists(filepath):
        print(f"[NOT FOUND] {rel_path}")
        continue

    with open(filepath, encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Add loading="lazy" to img tags that don't already have it
    # Skip logo img tags (they are above the fold)
    def add_lazy(m):
        tag = m.group(0)
        if 'loading=' in tag:
            return tag  # already has loading attribute
        if 'eastasialogo' in tag or 'logo' in tag.lower():
            return tag  # skip logo — above fold
        return tag[:-1] + ' loading="lazy">'

    new_content = re.sub(r'<img\b[^>]*>', add_lazy, content)

    if new_content == content:
        skipped += 1
        print(f"[SKIP - no change] {rel_path}")
        continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    count = new_content.count('loading="lazy"')
    print(f"[OK] {rel_path} ({count} lazy images)")
    updated += 1

print(f"\nDone: {updated} updated, {skipped} skipped.")
