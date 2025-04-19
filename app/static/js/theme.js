document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Определяем текущую тему из класса body
    const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    setTheme(currentTheme);
    
    // Обработчик клика
    themeToggle.addEventListener('click', function() {
        const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Отправляем на сервер, если пользователь авторизован
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
            fetch('/set_theme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ theme: newTheme })
            });
        }
    });
    
    function setTheme(theme) {
        // Удаляем оба класса на случай, если какой-то уже есть
        document.body.classList.remove('dark-theme', 'light-theme');
        
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            if (themeIcon) themeIcon.textContent = '☀️';
        } else {
            document.body.classList.add('light-theme');
            if (themeIcon) themeIcon.textContent = '🌙';
        }
        
        updateThemeImages(theme);
    }
    
    function updateThemeImages(theme) {
        const root = document.documentElement;
        const bgImage = theme === 'dark' 
            ? 'url("/static/images/backgrounds/anime-bg-dark.png")' 
            : 'url("/static/images/backgrounds/anime-bg-light.png")';
        root.style.setProperty('--header-bg-image', bgImage);
    }
});