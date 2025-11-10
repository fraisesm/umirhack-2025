from fastapi import FastAPI
from auth.router import router as auth_router
from auth.models import db
from config import settings

db.bind(provider="postgres", user="...", password="...", host="...", database="...")
db.generate_mapping(create_tables=True)

app = FastAPI(title="Agro App")
app.include_router(auth_router)
