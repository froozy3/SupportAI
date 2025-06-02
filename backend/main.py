from fastapi import FastAPI
from routers import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.include_router(router, prefix="/api")

# relate frontend with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
