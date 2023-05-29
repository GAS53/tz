from fastapi import FastAPI
import uvicorn
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

import servece
from db.db_func import create_db

app = FastAPI()


@app.post('/')
def get_questions(questions_num: int):
    while True:
        questions_num, last = servece.get_questions(questions_num)
        if questions_num == 0:
            return last


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return Response('wrong API!!!', 400)


if __name__ == "__main__":
    create_db()
    uvicorn.run(app, host='0.0.0.0', port=8000)
