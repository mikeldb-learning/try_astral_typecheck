from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
async def root():
    print("Hello World")
    return {"message": "Hello World"}
