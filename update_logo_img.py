import os
import re

dir_path = r'c:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia'
pattern = re.compile(r'<img[^>]*src="https://i\.postimg\.cc/sxwDpNK0/eastasialogo2\.png"[^>]*>')

count = 0
for root, dirs, files in os.walk(dir_path):
    if 'node_modules' in root.split(os.sep):
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if file == 'index.html' and root == dir_path:
                # Exclude root index.html
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            def replacer(match):
                original = match.group(0)
                # Replace URL
                modified = original.replace('https://i.postimg.cc/sxwDpNK0/eastasialogo2.png', '../assets/images/maristlogo.png')
                # Try expanding h-10 or h-12 slightly to ensure it scales nicely
                # Also add object-contain to be completely sure it scales.
                if 'h-12' in modified:
                    modified = modified.replace('h-12 w-auto', 'h-12 w-auto sm:h-14 object-contain')
                elif 'h-10' in modified:
                    modified = modified.replace('h-10 w-auto', 'h-10 w-auto sm:h-12 object-contain')
                    
                # To be sure we don't break "dark:brightness-125 dark:contrast-125" if they are present, 
                # we just leave them. But if we need to remove them because the new logo is different:
                # The user didn't say to remove dark mode modifiers, but they might apply weirdly to an actual photo-based logo.
                return modified

            new_content = pattern.sub(replacer, content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated {filepath}")

print(f"Total files updated: {count}")
