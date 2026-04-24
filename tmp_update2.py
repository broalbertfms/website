import re

path = r'c:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia\palawanmission\palawanmission.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace note color
c = c.replace('text-[10px] text-zinc-400 dark:text-zinc-500 mt-4 italic leading-tight text-center', 'text-[10px] text-red-500 mt-4 italic leading-tight text-center font-semibold')

# Sidebar replacement
old_sidebar = '''                                <li>
                                    <a href="#" class="flex items-center justify-between group">
                                        <span class="text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors">All Products</span>
                                        <span class="bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md">24</span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="flex items-center justify-between group">
                                        <span class="text-forest font-bold transition-colors">Woven Baskets</span>
                                        <span class="bg-forest/10 text-forest font-bold text-xs px-2 py-1 rounded-md">8</span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="flex items-center justify-between group">
                                        <span class="text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors">Beadwork</span>
                                        <span class="bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md">12</span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="flex items-center justify-between group">
                                        <span class="text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors">Forest Goods</span>
                                        <span class="bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md">4</span>
                                    </a>
                                </li>'''

new_sidebar = '''                                <li>
                                    <a href="#" class="category-link flex items-center justify-between group" data-category="all">
                                        <span class="cat-text text-forest font-bold transition-colors">All Products</span>
                                        <span class="cat-badge bg-forest/10 text-forest font-bold text-xs px-2 py-1 rounded-md">24</span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="category-link flex items-center justify-between group" data-category="woven-baskets">
                                        <span class="cat-text text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors">Woven Baskets</span>
                                        <span class="cat-badge bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md">8</span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="category-link flex items-center justify-between group" data-category="beadwork">
                                        <span class="cat-text text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors">Beadwork</span>
                                        <span class="cat-badge bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md">12</span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="category-link flex items-center justify-between group" data-category="forest-goods">
                                        <span class="cat-text text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors">Forest Goods</span>
                                        <span class="cat-badge bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md">4</span>
                                    </a>
                                </li>'''
c = c.replace(old_sidebar, new_sidebar)

# Product cards replacement
c = c.replace('<!-- Product 1 -->\n                            <div class="bg-white', '<!-- Product 1 -->\n                            <div class="product-card bg-white')
c = c.replace('<!-- Product 2 -->\n                            <div class="bg-white', '<!-- Product 2 -->\n                            <div class="product-card bg-white')
c = c.replace('<!-- Product 3 -->\n                            <div class="bg-white', '<!-- Product 3 -->\n                            <div class="product-card bg-white')
c = c.replace('<!-- Product 4 -->\n                            <div class="bg-white', '<!-- Product 4 -->\n                            <div class="product-card bg-white')

# Add data-category to each product card
def add_data_category(html, prod_num, category):
    pattern = r'(<!-- Product ' + str(prod_num) + r' -->\s*<div class="product-card bg-white dark:bg-zinc-950 rounded-\[2rem\] p-4 shadow-sm border border-zinc-100 dark:border-zinc-800 group relative flex flex-col")>'
    return re.sub(pattern, r'\1 data-category="' + category + '">', html)

c = add_data_category(c, 1, 'woven-baskets')
c = add_data_category(c, 2, 'beadwork')
c = add_data_category(c, 3, 'woven-baskets')
c = add_data_category(c, 4, 'forest-goods')

# JS Logic
js_logic = '''
        // Store Category Filter Logic
        document.addEventListener('DOMContentLoaded', () => {
            const categoryLinks = document.querySelectorAll('.category-link');
            const productCards = document.querySelectorAll('.product-card');

            categoryLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    
                    // Reset all categories
                    categoryLinks.forEach(item => {
                        const text = item.querySelector('.cat-text');
                        const badge = item.querySelector('.cat-badge');
                        
                        text.className = 'cat-text text-zinc-600 dark:text-zinc-400 group-hover:text-terra font-medium transition-colors';
                        badge.className = 'cat-badge bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 text-xs px-2 py-1 rounded-md';
                    });

                    // Set active category
                    const text = link.querySelector('.cat-text');
                    const badge = link.querySelector('.cat-badge');
                    text.className = 'cat-text text-forest font-bold transition-colors';
                    badge.className = 'cat-badge bg-forest/10 text-forest font-bold text-xs px-2 py-1 rounded-md';

                    // Filter products
                    const selectedCategory = link.getAttribute('data-category');
                    let visibleCount = 0;
                    productCards.forEach(card => {
                        if (selectedCategory === 'all' || card.getAttribute('data-category') === selectedCategory) {
                            card.style.display = 'flex';
                            visibleCount++;
                        } else {
                            card.style.display = 'none';
                        }
                    });
                    
                    // Update the showing text
                    const showingText = document.querySelector('.text-zinc-500.dark\\\\:text-zinc-400.font-medium.ml-2 span.text-forest.font-bold');
                    if(showingText) {
                        showingText.textContent = `1-${visibleCount}`;
                    }
                });
            });
        });

    </script>
'''

c = c.replace('</script>\n\n    </main>', js_logic + '\n    </main>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Success')
