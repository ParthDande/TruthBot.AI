// theme.js
function initializeTheme() {
    // Check if user has a saved preference
    const savedTheme = localStorage.getItem('theme');

    // If no saved preference, check system preference
    if (!savedTheme) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        localStorage.setItem('theme', prefersDark ? 'dark' : 'light');
    } else {
        // Apply the saved theme
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    // Update the theme attribute
    document.documentElement.setAttribute('data-theme', newTheme);

    // Save the new theme to localStorage
    localStorage.setItem('theme', newTheme);
}

// Initialize theme when page loads
document.addEventListener('DOMContentLoaded', initializeTheme);



   
 