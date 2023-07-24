git clone https://github.com/maks232930/RestaurantMenuAPI.git  

cd RestaurantMenuAPI/<br>

sudo docker-compose up --build -d<br>
sudo docker-compose exec web alembic upgrade head<br>

Можно тестировать<br>