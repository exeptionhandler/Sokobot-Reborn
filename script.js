// Navegación móvil
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });
}

// Smooth scrolling para enlaces
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

// Animación de números en estadísticas
function animateNumbers() {
    const stats = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalNumber = parseInt(target.getAttribute('data-target'));
                animateValue(target, 0, finalNumber, 2000);
                observer.unobserve(target);
            }
        });
    });
    
    stats.forEach(stat => observer.observe(stat));
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    let current = start;
    
    const timer = setInterval(() => {
        current += increment * Math.ceil(range / 100);
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = current.toLocaleString();
    }, stepTime);
}

// Efectos de scroll para navbar
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 5px 20px rgba(255, 182, 193, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Animaciones de entrada para las tarjetas
function animateCards() {
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
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Partículas flotantes de fondo
function createFloatingEmojis() {
    const emojis = ['💕', '✨', '📦', '🎀', '💖', '🌟', '⭐', '💫'];
    const container = document.body;
    
    function createEmoji() {
        const emoji = document.createElement('div');
        emoji.innerHTML = emojis[Math.floor(Math.random() * emojis.length)];
        emoji.style.position = 'fixed';
        emoji.style.left = Math.random() * 100 + 'vw';
        emoji.style.top = '110vh';
        emoji.style.fontSize = Math.random() * 20 + 15 + 'px';
        emoji.style.opacity = Math.random() * 0.3 + 0.1;
        emoji.style.pointerEvents = 'none';
        emoji.style.zIndex = '-1';
        emoji.style.transition = 'transform 15s linear, opacity 15s ease-out';
        
        container.appendChild(emoji);
        
        // Animar hacia arriba
        setTimeout(() => {
            emoji.style.transform = `translateY(-120vh) rotate(${Math.random() * 360}deg)`;
            emoji.style.opacity = '0';
        }, 100);
        
        // Remover después de la animación
        setTimeout(() => {
            if (container.contains(emoji)) {
                container.removeChild(emoji);
            }
        }, 15000);
    }
    
    // Crear emoji cada cierto tiempo
    setInterval(createEmoji, 3000);
}

// Efecto de hover para botones
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px) scale(1.05)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Easter egg - clic múltiple en el logo
let logoClicks = 0;
const logo = document.querySelector('.logo-img');

if (logo) {
    logo.addEventListener('click', () => {
        logoClicks++;
        
        if (logoClicks === 1) {
            setTimeout(() => logoClicks = 0, 2000);
        }
        
        if (logoClicks >= 5) {
            // Easter egg activado
            document.body.style.filter = 'hue-rotate(180deg)';
            setTimeout(() => {
                document.body.style.filter = 'none';
            }, 3000);
            
            // Crear explosión de emojis
            for (let i = 0; i < 20; i++) {
                setTimeout(() => {
                    createSpecialEmoji();
                }, i * 100);
            }
            
            logoClicks = 0;
        }
    });
}

function createSpecialEmoji() {
    const emoji = document.createElement('div');
    emoji.innerHTML = '🎉';
    emoji.style.position = 'fixed';
    emoji.style.left = Math.random() * 100 + 'vw';
    emoji.style.top = Math.random() * 100 + 'vh';
    emoji.style.fontSize = '30px';
    emoji.style.pointerEvents = 'none';
    emoji.style.zIndex = '9999';
    emoji.style.animation = 'explode 2s ease-out forwards';
    
    document.body.appendChild(emoji);
    
    setTimeout(() => {
        if (document.body.contains(emoji)) {
            document.body.removeChild(emoji);
        }
    }, 2000);
}

// CSS para la animación de explosión
const style = document.createElement('style');
style.textContent = `
    @keyframes explode {
        0% {
            transform: scale(0) rotate(0deg);
            opacity: 1;
        }
        50% {
            transform: scale(1.5) rotate(180deg);
            opacity: 1;
        }
        100% {
            transform: scale(0.5) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Inicializar todas las funciones cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    animateNumbers();
    animateCards();
    createFloatingEmojis();
    
    // Agregar efecto de parallax suave al hero
    const hero = document.querySelector('.hero');
    const heroContent = document.querySelector('.hero-content');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.3;
        
        if (heroContent) {
            heroContent.style.transform = `translateY(${rate}px)`;
        }
    });
    
    // Precargar imágenes importantes
    const importantImages = [
        'https://via.placeholder.com/40x40/FFB6C1/FFF?text=S',
        'https://via.placeholder.com/300x300/FFB6C1/FFF?text=Sokoromi'
    ];
    
    importantImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
});

// Función para copiar el enlace de invitación
function copyInviteLink() {
    const inviteUrl = 'https://discord.com/oauth2/authorize?client_id=1419121189611372574&permissions=563364418145344&integration_type=0&scope=bot';
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(inviteUrl).then(() => {
            showNotification('¡Enlace copiado! 💕');
        }).catch(err => {
            console.error('Error al copiar: ', err);
        });
    }
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.innerHTML = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #FFB6C1, #FFC0CB);
        color: white;
        padding: 15px 25px;
        border-radius: 50px;
        font-weight: 600;
        z-index: 10000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.3);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}
// Gestión de tema oscuro/claro
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

        // Escuchar cambios en la preferencia del sistema
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
        
        // Animación kawaii al cambiar tema
        this.playThemeChangeAnimation();
    }

    applyTheme() {
        const html = document.documentElement;
        
        if (this.theme === 'dark') {
            html.setAttribute('data-theme', 'dark');
        } else if (this.theme === 'light') {
            html.removeAttribute('data-theme');
        } else {
            // Auto - seguir preferencia del sistema
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark) {
                html.setAttribute('data-theme', 'dark');
            } else {
                html.removeAttribute('data-theme');
            }
        }
    }

    updateToggleIcon() {
        const toggleIcon = document.querySelector('.theme-toggle-icon');
        if (!toggleIcon) return;

        const icons = {
            light: '🌙',
            dark: '☀️',
            auto: '🌓'
        };

        toggleIcon.textContent = icons[this.theme];
        
        // Tooltip
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            const labels = {
                light: 'Cambiar a modo oscuro',
                dark: 'Cambiar a modo automático',
                auto: 'Cambiar a modo claro'
            };
            toggleBtn.setAttribute('aria-label', labels[this.theme]);
        }
    }

    playThemeChangeAnimation() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        toggleBtn.style.transform = 'scale(0.8)';
        setTimeout(() => {
            toggleBtn.style.transform = '';
        }, 150);

        // Efectos kawaii opcionales
        this.createThemeParticles();
    }

    createThemeParticles() {
        const particles = ['✨', '💖', '🌸', '⭐', '💜'];
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.textContent = particles[Math.floor(Math.random() * particles.length)];
            particle.style.cssText = `
                position: fixed;
                pointer-events: none;
                font-size: 1.2rem;
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
                document.body.removeChild(particle);
            }, 1000);
        }
    }
}

// Inicializar cuando cargue el DOM
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
});
