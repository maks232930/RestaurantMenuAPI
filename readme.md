sudo apt update

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv

git clone https://github.com/maks232930/RestaurantMenuAPI.git  

cd RestaurantMenuAPI/<br>

python3 -m venv venv<br>
source venv/bin/activate<br>
pip install -r requirements.txt<br>

Запускаем postgres: sudo docker-compose up --build -d<br>

запустили: uvicorn src.main:app --reload<br>

Потом закрыли и: alembic upgrade head

запустили: uvicorn src.main:app --reload<br>

Можно тестировать
