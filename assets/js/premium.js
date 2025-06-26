// Premium Landing Page JavaScript

// GSAP Registration
gsap.registerPlugin(ScrollTrigger);

// DOM Elements
const navbar = document.getElementById('navbar');
const heroSection = document.getElementById('hero');
const scrollIndicator = document.querySelector('.scroll-indicator');
const contactForm = document.getElementById('contactForm');

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initScrollAnimations();
    initSmoothScrolling();
    initFormHandling();
    initMicroInteractions();
});

// Navbar scroll effect
function initNavbar() {
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScrollY = currentScrollY;
    });
}

// GSAP Scroll Animations
function initScrollAnimations() {
    // Hero animations are handled by CSS animations
    
    // Intro section animation
    gsap.fromTo('.intro-headline', 
        { 
            opacity: 0, 
            y: 60 
        },
        {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: "power3.out",
            scrollTrigger: {
                trigger: '.intro',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );
    
    gsap.fromTo('.intro-text', 
        { 
            opacity: 0, 
            y: 40 
        },
        {
            opacity: 1,
            y: 0,
            duration: 1,
            delay: 0.2,
            ease: "power3.out",
            scrollTrigger: {
                trigger: '.intro',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );
    
    // About section animations
    gsap.fromTo('.about-image', 
        { 
            opacity: 0, 
            x: -60 
        },
        {
            opacity: 1,
            x: 0,
            duration: 1,
            ease: "power3.out",
            scrollTrigger: {
                trigger: '.about',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );
    
    gsap.fromTo('.about-content', 
        { 
            opacity: 0, 
            x: 60 
        },
        {
            opacity: 1,
            x: 0,
            duration: 1,
            delay: 0.2,
            ease: "power3.out",
            scrollTrigger: {
                trigger: '.about',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );
    
    // Work cards stagger animation
    gsap.fromTo('.work-card', 
        { 
            opacity: 0, 
            y: 60 
        },
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: "power3.out",
            stagger: 0.2,
            scrollTrigger: {
                trigger: '.work-grid',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );
    
    // Contact section animation
    gsap.fromTo('.contact-content', 
        { 
            opacity: 0, 
            y: 60 
        },
        {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: "power3.out",
            scrollTrigger: {
                trigger: '.contact',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );
    
    // Parallax effect for hero background
    gsap.to('.hero-background', {
        yPercent: -50,
        ease: "none",
        scrollTrigger: {
            trigger: '.hero',
            start: 'top bottom',
            end: 'bottom top',
            scrub: true
        }
    });
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    // Scroll indicator click
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            document.getElementById('intro').scrollIntoView({
                behavior: 'smooth'
            });
        });
    }
    
    // Navigation links smooth scroll
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for navbar height
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Form handling with animations
function initFormHandling() {
    if (!contactForm) return;
    
    const inputs = contactForm.querySelectorAll('input, textarea');
    const submitBtn = contactForm.querySelector('.submit-btn');
    
    // Input focus animations
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            gsap.to(input, {
                scale: 1.02,
                duration: 0.3,
                ease: "power2.out"
            });
        });
        
        input.addEventListener('blur', () => {
            gsap.to(input, {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });
    
    // Form submission
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Animate submit button
        gsap.to(submitBtn, {
            scale: 0.95,
            duration: 0.1,
            yoyo: true,
            repeat: 1,
            ease: "power2.inOut"
        });
        
        // Simulate form submission
        setTimeout(() => {
            showNotification('Message sent successfully!', 'success');
            contactForm.reset();
        }, 1000);
    });
}

// Micro-interactions and hover effects
function initMicroInteractions() {
    // Work card hover effects
    document.querySelectorAll('.work-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card.querySelector('.work-img'), {
                scale: 1.1,
                duration: 0.6,
                ease: "power2.out"
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card.querySelector('.work-img'), {
                scale: 1,
                duration: 0.6,
                ease: "power2.out"
            });
        });
    });
    
    // Social link hover effects
    document.querySelectorAll('.social-link').forEach(link => {
        link.addEventListener('mouseenter', () => {
            gsap.to(link, {
                y: -3,
                duration: 0.3,
                ease: "power2.out"
            });
        });
        
        link.addEventListener('mouseleave', () => {
            gsap.to(link, {
                y: 0,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });
    
    // Button hover effects
    document.querySelectorAll('.submit-btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, {
                y: -2,
                boxShadow: "0 10px 30px rgba(1, 95, 252, 0.3)",
                duration: 0.3,
                ease: "power2.out"
            });
        });
        
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, {
                y: 0,
                boxShadow: "0 0px 0px rgba(1, 95, 252, 0)",
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '16px 24px',
        backgroundColor: type === 'success' ? '#10B981' : '#015FFC',
        color: 'white',
        borderRadius: '12px',
        fontWeight: '500',
        zIndex: '10000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
    });
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Intersection Observer for performance
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
        }
    });
}, observerOptions);

// Observe elements for animations
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.work-card, .about-image, .about-content');
    animatedElements.forEach(el => observer.observe(el));
});

// Preloader (if needed)
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Smooth scroll polyfill for older browsers
if (!('scrollBehavior' in document.documentElement.style)) {
    const smoothScrollPolyfill = () => {
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    const offsetTop = target.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    };
    smoothScrollPolyfill();
}

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debouncing to scroll-heavy operations
const debouncedScrollHandler = debounce(() => {
    // Any heavy scroll operations can go here
}, 16); // ~60fps

window.addEventListener('scroll', debouncedScrollHandler);

// Accessibility improvements
document.addEventListener('keydown', (e) => {
    // Escape key to close any open modals or overlays
    if (e.key === 'Escape') {
        // Handle escape key functionality
    }
    
    // Tab navigation improvements
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-navigation');
});

// Reduced motion support
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (prefersReducedMotion.matches) {
    // Disable or reduce animations for users who prefer reduced motion
    gsap.globalTimeline.timeScale(0.1);
}

// Console signature (optional easter egg)
console.log(`
%c
╔══════════════════════════════════════╗
║                                      ║
║        Jay Cuthrell Portfolio        ║
║     Built with premium design        ║
║        and smooth animations         ║
║                                      ║
╚══════════════════════════════════════╝

`, 'color: #015FFC; font-family: monospace; font-size: 12px;');