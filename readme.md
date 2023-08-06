Для приложения и тестов через Postman<br>
sudo docker-compose up --build -d<br>
Можно тестировать<br>

Для удаления всего:<br>
sudo docker-compose down --volumes
<br>
<br>
<br>
Для pytest:<br>
sudo docker-compose -f docker-compose.tests.yml up -d --build<br>
sudo docker-compose exec web_test pytest -s -v

Для удаления всего:<br>
sudo docker-compose -f docker-compose.tests.yml down --volumes


НОВОЕ ЗАДАНИЕ!<br>
Я немного изменил .pre-commit-config.yaml<br>
А именно добавил: "exclude: 'alembic'" в mypy, так как ошибки были в alembic
