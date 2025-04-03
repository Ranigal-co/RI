# @Ranigal-co
"""
    Запуск сервера
"""
import os

from app import create_app, db

app = create_app()

if __name__ == "__main__":
    """
        для тестов на tuna (тест-деплой в интернет)
        Потом еще немного изменим для полноценного деплоя на glitch
    """
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)