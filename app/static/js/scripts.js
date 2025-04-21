document.addEventListener('DOMContentLoaded', function() {
  // Находим все блоки с классом clickable-block
  const clickableBlocks = document.querySelectorAll('.project');

  // Для каждого блока добавляем обработчик
  clickableBlocks.forEach(block => {
    block.addEventListener('click', function() {
      // Создаем новую форму
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = '/projects';
      form.style.display = 'none';

      // Собираем все data-атрибуты
      const allData = this.dataset;

      // Добавляем каждый data-атрибут в форму
      for (const [key, value] of Object.entries(allData)) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = `data_${key}`;
        input.value = value;
        form.appendChild(input);
      }

      // Добавляем action для проверки нажатия
      const action = document.createElement('input');
      action.type = 'hidden';
      action.name = 'action';
      action.value = 'open_link';
      form.appendChild(action);

      // Добавляем форму в DOM и отправляем
      document.body.appendChild(form);
      form.submit();

      // Удаляем форму после отправки
      setTimeout(() => form.remove(), 100);
    });
  });
});