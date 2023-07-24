sudo apt update

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv

git clone  

cd project<br>

python3 -m venv venv<br>
source venv/bin/activate<br>
pip install -r requirements.txt1<br>

Запускаем postgres: sudo docker-compose up --build -d<br>

uvicorn src.main:app --reload

В новой консоли: 
alembic upgrade head
