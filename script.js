// Theme Manager
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'auto';
        this.init();
    }

    init() {
        this.applyTheme();
        this.bindEvents();
        this.updateToggleIcon();
    }

    bindEvents() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleTheme());
        }

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
            if (this.theme === 'auto') {
                this.applyTheme();
            }
        });
    }

    toggleTheme() {
        const themes = ['light', 'dark', 'auto'];
        const currentIndex = themes.indexOf(this.theme);
        this.theme = themes[(currentIndex + 1) % themes.length];
        
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
        this.updateToggleIcon();
        this.playThemeAnimation();
    }

    applyTheme() {
        const html = document.documentElement;
        
        if (this.theme === 'dark') {
            html.setAttribute('data-theme', 'dark');
        } else if (this.theme === 'light') {
            html.removeAttribute('data-theme');
        } else {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark) {
                html.setAttribute('data-theme', 'dark');
            } else {
                html.removeAttribute('data-theme');
            }
        }
    }

    updateToggleIcon() {
        const toggleIcon = document.querySelector('.theme-icon');
        if (!toggleIcon) return;

        const icons = {
            light: '🌙',
            dark: '☀️',
            auto: '🌓'
        };

        toggleIcon.textContent = icons[this.theme];
    }

    playThemeAnimation() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        toggleBtn.style.transform = 'scale(0.8)';
        setTimeout(() => {
            toggleBtn.style.transform = '';
        }, 150);

        // Crear partículas kawaii
        this.createThemeParticles();
    }

    createThemeParticles() {
        const particles = ['✨', '💖', '🌸', '⭐', '💫'];
        const toggleBtn = document.getElementById('theme-toggle');
        
        if (!toggleBtn) return;

        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.textContent = particles[Math.floor(Math.random() * particles.length)];
            particle.style.cssText = `
                position: fixed;
                pointer-events: none;
                font-size: 1.5rem;
                z-index: 9999;
                opacity: 1;
                transition: all 1s ease-out;
            `;
            
            const rect = toggleBtn.getBoundingClientRect();
            particle.style.left = rect.left + rect.width/2 + 'px';
            particle.style.top = rect.top + rect.height/2 + 'px';
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.style.transform = `translate(${(Math.random() - 0.5) * 100}px, ${-50 - Math.random() * 50}px)`;
                particle.style.opacity = '0';
            }, 50);
            
            setTimeout(() => {
                if (document.body.contains(particle)) {
                    document.body.removeChild(particle);
                }
            }, 1000);
        }
    }
}

// Scroll animations
function addScrollAnimations() {
    const cards = document.querySelectorAll('.feature-card, .command-card, .stat-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Character interaction
function addCharacterInteraction() {
    const character = document.querySelector('.character-img');
    if (!character) return;
    
    character.addEventListener('click', () => {
        character.style.animation = 'bounce 0.6s ease';
        
        // Crear corazones
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                createFloatingHeart(character);
            }, i * 200);
        }
        
        setTimeout(() => {
            character.style.animation = '';
        }, 600);
    });
}

function createFloatingHeart(element) {
    const heart = document.createElement('div');
    heart.textContent = '💖';
    heart.style.cssText = `
        position: absolute;
        font-size: 1.5rem;
        pointer-events: none;
        z-index: 1000;
        opacity: 1;
        transition: all 1.5s ease-out;
    `;
    
    const rect = element.getBoundingClientRect();
    heart.style.left = rect.left + rect.width/2 + Math.random() * 40 - 20 + 'px';
    heart.style.top = rect.top + rect.height/2 + 'px';
    
    document.body.appendChild(heart);
    
    setTimeout(() => {
        heart.style.transform = `translateY(-100px)`;
        heart.style.opacity = '0';
    }, 50);
    
    setTimeout(() => {
        if (document.body.contains(heart)) {
            document.body.removeChild(heart);
        }
    }, 1500);
}

// CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    addScrollAnimations();
    addCharacterInteraction();
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
