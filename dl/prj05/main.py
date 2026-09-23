from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/book")
def select_book():
    print("select_book called ~~~")
    return {
        "title": "harry potter",
        "price": 4099,
    }