python3 -m venv env
source ./env/bin/activate
pip3 install -r ./requirements.txt
alembic init alembic (Initialise Alembic)
alembic revision --autogenerate -m "initial schema" (Create Migration)
alembic upgrade head (Create Tables)
alembic revision --autogenerate -m "add avatar_url to users" (For every new update's on model)
alembic upgrade head (Apply new migration)
uvicorn main:app --reload