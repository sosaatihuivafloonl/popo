from fastapi import FastAPI


app = FastAPI()


@app.get("/test")
async def get_test():
    return "message: hello!"
