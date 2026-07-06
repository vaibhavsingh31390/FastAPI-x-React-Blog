from fastapi import Depends, FastAPI

app = FastAPI(title="Blog's APP")

db_1 = ["Yes"]


def my_db():
    return db_1


@app.post("/add_to_db")
def add_to_db(item: str, db: list = Depends(my_db)):
    db.append(item)
    return {"status": "success", "data": db}
