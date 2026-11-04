const year = document.getElementById('year');
if (year) {
    year.textContent = new Date().getFullYear();
}

const topbar = document.querySelector('.topbar');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (topbar) {
    const updateNavState = () => {
        document.body.classList.toggle('nav-scrolled', window.scrollY > 12);
    };

    updateNavState();
    window.addEventListener('scroll', updateNavState, { passive: true });
}

const revealItems = document.querySelectorAll('.reveal');
if (revealItems.length && !prefersReducedMotion.matches) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -20px 0px'
    });

    revealItems.forEach((item) => observer.observe(item));
} else {
    revealItems.forEach((item) => item.classList.add('is-visible'));
}
