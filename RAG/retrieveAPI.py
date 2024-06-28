from fastapi import FastAPI
from rag import *

import uvicorn

app = FastAPI(title="Exposing")

@app.get("/retrieve")
async def root(query=None, packages=None):
    retrieve(query, packages)


if __name__ == "__main__":
    uvicorn.run(app="fastapi:app", host="127.0.0.1", port=8080, reload=True)
    
    
    