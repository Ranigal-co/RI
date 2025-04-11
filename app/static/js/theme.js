document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Проверяем сохранённую тему
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
    
    // Обработчик клика
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setTheme(currentTheme);
        localStorage.setItem('theme', currentTheme);
    });
    
    function setTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            themeIcon.textContent = '☀️';
            updateThemeImages('dark');
        } else {
            document.body.classList.remove('dark-theme');
            themeIcon.textContent = '🌙';
            updateThemeImages('light');
        }
        
        // Отправляем на сервер, если пользователь авторизован
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
            fetch('/set_theme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ theme: theme })
            });
        }
    }
    
    function updateThemeImages(theme) {
        const root = document.documentElement;
        if (theme === 'dark') {
            root.style.setProperty('--header-bg-image', `url("${window.location.origin}/static/images/backgrounds/anime-bg-dark.png")`);
        } else {
            root.style.setProperty('--header-bg-image', `url("${window.location.origin}/static/images/backgrounds/anime-bg-light.png")`);
        }
    }
});