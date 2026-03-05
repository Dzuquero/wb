Запуск проекта:



1\. Убедитесь, что установлены Docker и Docker Compose.



2\. Собираем и запускаем контейнеры:

&nbsp;  'docker compose up --build'



3\. После запуска сервер будет доступен по адресу:

&nbsp;  'http://localhost:8000'



4\. Для запуска тестов внутри контейнера (в новом терминале):

&nbsp;  'docker compose exec app pytest'



5\. Чтобы остановить проект:

&nbsp;  'Ctrl + C' 



