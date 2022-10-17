# Тестирую Yatube 1.2

### Покрываю тестами Models:
- Тестируем модели приложения posts в Yatube.
- Добавляю в классы Post и Group метод __str__ :
  - для класса Post — первые пятнадцать символов поста: post.text[:15];
  - для класса Group — название группы.
- Тестирую, правильно ли отображается значение поля __str__ в объектах моделей.

### Тестирование URLs:
Проверяю доступность страниц и названия шаблонов приложения Posts проекта Yatube. Проверяю учитываются ли права доступа.
Проверяю, что запрос к несуществующей странице вернёт ошибку 404.

### Проверка namespase:name и шаблонов:
Тесты, проверяющие, что во view-функциях используются правильные html-шаблоны.

### Тестирование контекста:
Проверяю, соответствует ли ожиданиям словарь context, передаваемый в шаблон при вызове.

### Дополнительная проверка при создании поста:
- Проверяю, что если при создании поста указана группа, то этот пост появляется
  - на главной странице сайта,
  - на странице выбранной группы,
  - в профайле пользователя.
- Проверьте, что этот пост не попал в группу, для которой не был предназначен.

### Тестирую Forms:
В проекте Yatube так же написанны тесты, которые проверяют, что
- при отправке валидной формы со страницы создания поста reverse('posts:create_post') создаётся новая запись в базе данных;
- при отправке валидной формы со страницы редактирования поста reverse('posts:post_edit', args=('post_id',)) происходит изменение поста с post_id в базе данных.




### Структура проекта:
```
ilshat2
 └── hw04_test
     ├── .gihub/workflows
     ├── tests/ 
     ├── yatube  <-- рабочая папка проекта с кодом проекта
     |   ├── manage.py
     |   └── yatube
     |       ├── __init__.py
     |       ├── settings.py
     |       ├── urls.py
     |       └── wsgi.py
     ├── .gitignore
     ├── README.md 
     ├── pytest.ini
     ├── requirements.txt
     └── setup.cfg
```
