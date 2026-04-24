import os, glob, re

standard_footer = """    <!-- Footer -->
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
                    <a href="dataprivacypolicy.html" class="hover:text-white transition-colors">Privacy Policy</a>
                    <a href="termsofservice.html" class="hover:text-white transition-colors">Terms of Service</a>
                    <a href="sitemap.html" class="hover:text-white transition-colors">Sitemap</a>
                </div>
            </div>
        </div>
    </footer>"""

d = r'c:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia\websitedocumentations'
files = glob.glob(d + '/*.html')
for f in files:
    content = open(f, encoding='utf-8').read()
    new_content = re.sub(r'<!-- Footer -->.*?</footer>', standard_footer, content, flags=re.DOTALL)
    open(f, 'w', encoding='utf-8').write(new_content)
