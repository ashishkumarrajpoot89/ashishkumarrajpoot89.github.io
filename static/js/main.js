// Mobile nav toggle (with accessible aria-expanded state)
const toggle = document.getElementById('navToggle');
const links = document.getElementById('navLinks');
if (toggle && links) {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', 'navLinks');
    toggle.addEventListener('click', () => {
        const open = links.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
}

// Skills filter
document.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', () => {
        const filter = pill.dataset.filter;
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        document.querySelectorAll('.skill-group').forEach(group => {
            if (filter === 'all' || group.dataset.group === filter) {
                group.style.display = '';
            } else {
                group.style.display = 'none';
            }
        });
    });
});

// Skills collapse / expand (CSS hides `.extra` chips only when <html class="js">)
(function () {
    const groups = Array.from(document.querySelectorAll('.skill-group'));
    const allBtn = document.getElementById('skillsToggleAll');
    function setGroup(group, open) {
        group.classList.toggle('expanded', open);
        const btn = group.querySelector('.skill-more');
        if (!btn) return;
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        btn.textContent = open ? 'Show less' : btn.dataset.more;
    }
    function syncAll() {
        if (!allBtn) return;
        const withMore = groups.filter(g => g.querySelector('.skill-more'));
        const allOpen = withMore.length > 0 && withMore.every(g => g.classList.contains('expanded'));
        allBtn.textContent = allOpen ? 'Collapse all' : 'Expand all';
        allBtn.setAttribute('aria-pressed', allOpen ? 'true' : 'false');
    }
    groups.forEach(group => {
        const btn = group.querySelector('.skill-more');
        if (btn) btn.addEventListener('click', () => {
            setGroup(group, !group.classList.contains('expanded'));
            syncAll();
        });
    });
    if (allBtn) allBtn.addEventListener('click', () => {
        const open = allBtn.getAttribute('aria-pressed') !== 'true';
        groups.forEach(g => setGroup(g, open));
        syncAll();
    });
    syncAll();
})();
// Reveal on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) { e.target.style.opacity = 1; e.target.style.transform = 'none'; }
    });
}, { threshold: 0.1 });
document.querySelectorAll('.card, .skill-tile, .tl-item, .stat').forEach(el => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity .5s ease, transform .5s ease';
    observer.observe(el);
});

// Project-detail sidebar: highlight section in view + smooth scroll
const detailNav = document.querySelector('.detail-nav');
if (detailNav) {
    detailNav.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
        });
    });
    const sections = document.querySelectorAll('.detail-section');
    const navObserver = new IntersectionObserver(entries => {
        entries.forEach(en => {
            if (en.isIntersecting) {
                detailNav.querySelectorAll('a').forEach(l => l.classList.remove('active'));
                const link = detailNav.querySelector('a[href="#' + en.target.id + '"]');
                if (link) link.classList.add('active');
            }
        });
    }, { rootMargin: '-40% 0px -50% 0px' });
    sections.forEach(s => navObserver.observe(s));
}

// ---- Single-page: smooth scroll + scroll-spy nav highlighting ----
(function () {
    const navLinks = Array.from(document.querySelectorAll('.nav-links a'));
    // Only run on the one-page layout (links start with "#")
    const anchorLinks = navLinks.filter(a => a.getAttribute('href') && a.getAttribute('href').startsWith('#'));

    // Smooth scroll for any in-page anchor + close mobile menu
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const id = a.getAttribute('href');
            if (id.length < 2) return;
            const target = document.querySelector(id);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
                const menu = document.getElementById('navLinks');
                if (menu) menu.classList.remove('open');
                history.replaceState(null, '', id);
            }
        });
    });

    if (!anchorLinks.length) return;
    const sections = document.querySelectorAll('section[id]');
    const spy = new IntersectionObserver(entries => {
        entries.forEach(en => {
            if (en.isIntersecting) {
                anchorLinks.forEach(l => l.classList.remove('active'));
                const link = anchorLinks.find(l => l.getAttribute('href') === '#' + en.target.id);
                if (link) link.classList.add('active');
            }
        });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => spy.observe(s));
})();
