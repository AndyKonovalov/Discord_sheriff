# **Discord-bot "bot_sheriff" для слежения за порядком в чате**
## Функционал бота:
1. При запуске файла botrun.py бот подключается к базе данных Sheriff.db и выводит в косоль сообщение, информируя об успешном запуске.
2. Реакция на событие. Добавление нового пользователя (вывод привественного сообщения в основном чате и отправка сообщения с инструкцией личку пользователю).
3. Реакция на событие. Удаление пользователя с канала (вывод прощального сообщения в основном чате).
4. Выполнение простых команд калькулятора (!сложение, !вычитание, !деление, !умножение, !корень).
5. Команда !статус показывает пользователю количество предпреждений за наличие запретных слов в чате. Команда !инфо выводит пользователю список команд бота.
6. Бот удалает сообщение с запретными словами из чата. Заносит в базу данных Sheriff.db id нарушителя и переменную count(счетчик). Обращается к нарушителю с предупреждением, сообщает сколько предупреждений осталось до БАНа.
7. При третьем нарушении бот удалает пользователя из чата по причине "Нецензурные выражения. А также выводит сообщение о причине БАНа в основной чат.
### **файл to_json конвертирует текстовый файл cenz.txt в cenz.json**
### **файл cenz.txt используется для хранения запрещенных слов**
### **файл cenz.json ипользуется для создания множества запрещенных слов**

Для проверки работы бота использовались слова из файла cenz.txt **(грязь, брань, ругань).**