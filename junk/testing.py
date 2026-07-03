# from fastapi import Depends, FastAPI, HTTPException

# Blog = {
#     1: {
#         "id": 1,
#         "name": "Blog 1",
#         "description": "Blog 1 description",
#     },
#     2: {
#         "id": 2,
#         "name": "Blog 2",
#         "description": "Blog 2 description",
#     },
#     3: {
#         "id": 3,
#         "name": "Blog 3",
#         "description": "Blog 3 description",
#     },
# }

# Users ={
#     1: {
#         "id": 1,
#         "name": "User 1",
#         "email": "user1@example.com",
#     },
#     2: {
#         "id": 2,
#         "name": "User 2",
#         "email": "user2@example.com",
#     },
#     3: {
#         "id": 3,
#         "name": "User 3",
#         "email": "user3@example.com",
#     },
# }


# app = FastAPI(title="Blog's APP")

# class QuerySingleObj():
#     def __init__(self, model: any):
#         self.model = model

#     def __call__(self, id: int):
#         if id not in self.model:
#             raise HTTPException(status_code=404, detail=f"Object with id {id} not found")
#         return self.model[id]

# @app.get("/blogs/{id}")
# def get_blog(blog: dict = Depends(QuerySingleObj(Blog))):
#     return blog

# @app.get("/users/{id}")
# def get_user(user: dict = Depends(QuerySingleObj(Users))):
#     return user

# from fastapi import FastAPI

# app = FastAPI(title="File Management System")
# FILE_PATH = "file.txt"


# @app.get("/list_files")
# def list_files():
#     try:
#         with open(FILE_PATH, "r") as f:
#             content = f.read()
#         return {"status": "success", "data": content}
#     except FileNotFoundError:
#         return {"status": "success", "data": ""}


# @app.post("/add_to_file")
# def add_to_file(body: dict):
#     content = body["content"]
#     with open(FILE_PATH, "a") as f:
#         f.write(content)
#     with open(FILE_PATH, "r") as f:
#         file_content = f.read()
#     return {"status": "success", "data": file_content}

# from fastapi import Depends, FastAPI, HTTPException

# app = FastAPI(title="Blog's APP")

# db_1 = ["Yes"]

# def my_db():
#     return db_1


# @app.post("/add_to_db")
# def add_to_db(item: str):
#     db_1.append(item)
#     return {"status": "success", "data": db_1}



# import time
# # import requests
# import aiohttp
# import asyncio

# async def make_request(session, request_count):
#     url="https://httpbin.org/get"
#     print(f"Request no-{request_count}")
#     async with session.get(url) as response:
#         if response.status == 200:
#             pass

# async def main():
#     request_count = 20
#     async with aiohttp.ClientSession() as session:
#         await asyncio.gather(*[make_request(session, i) for i in range(request_count)])


# if __name__ == "__main__":
#     start_time = time.time()
#     asyncio.run(main())
#     print(f"Time taken: {time.time() - start_time} seconds")
# def main():
#     request_count = 20
#     url="https://httpbin.org/get"
#     session = requests.Session()
#     for _ in range(request_count):
#         print(f"Request {_ + 1} of {request_count}")
#         response = session.get(url)
#         if response.status_code == 200:
#             pass

# start_time = time.time()
# main()
# end_time = time.time()
# print(f"Time taken: {end_time - start_time} seconds")
import asyncio


import asyncio

numbers = []

async def increment(num):
    numbers.append(num)
    asyncio.sleep(0.01)
    

async def countdown():
    for i in range(1, 101):
        await asyncio.gather(*[increment(i) for i in range(1, 101)])
    print(numbers)

if __name__ == "__main__":
    asyncio.run(countdown())
