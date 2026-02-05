from fastapi import FastAPI
import models
from database import engine
from routers import admin, auth, user, task
from fastapi.middleware.cors import CORSMiddleware
import os 
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:5173",
    "https://internship-assignment-frontend.vercel.app",  # Add your Vercel domain later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("ENV") == "dev":
    models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(task.router)