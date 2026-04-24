import os
import re

dir_path = r'c:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia'
# We want to match exactly the generated line
pattern = re.compile(r'<div class="text-\[10px\] sm:text-xs font-bold text-zinc-500 tracking-\[0\.2em\] uppercase">Marists of Champagnat</div>')

count = 0
for root, dirs, files in os.walk(dir_path):
    if 'node_modules' in root.split(os.sep):
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = pattern.sub(
                r'<div class="text-[10px] sm:text-xs font-bold text-[#c41e3a] tracking-[0.2em] uppercase">Marists of Champagnat</div>',
                content
            )
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated {filepath}")

print(f"Total files updated: {count}")
