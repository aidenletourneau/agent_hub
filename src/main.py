from fastapi import FastAPI
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://root:password@localhost:5432/project")

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}