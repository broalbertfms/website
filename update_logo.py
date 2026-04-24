import os
import re

dir_path = r'c:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia'
pattern = re.compile(r'<([a-z]+)\s+class="([^"]*?)"\s*>MaristEastAsia</\1>')

count = 0
for root, dirs, files in os.walk(dir_path):
    if 'node_modules' in root.split(os.sep):
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            def replacer(match):
                tag = match.group(1)
                classes = match.group(2)
                # Keep original classes but ensure leading-tight for top, if not present
                new_classes = classes
                if 'leading-tight' not in new_classes:
                    new_classes += ' leading-tight'
                return f'''<div class="flex flex-col">
                    <div class="{new_classes}">MaristEastAsia</div>
                    <div class="text-[10px] sm:text-xs font-bold text-zinc-500 tracking-[0.2em] uppercase">Marists of Champagnat</div>
                </div>'''

            new_content = pattern.sub(replacer, content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated {filepath}")

print(f"Total files updated: {count}")
