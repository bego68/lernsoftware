from fastapi import FastAPI
from .database.database import engine
from .database import models
from .routers import users, cards

# This line creates the database tables if they don't exist.
# In a production environment, you would typically use a migration tool like Alembic.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="APT-Erfolg Lernplattform API",
    description="API für die webbasierte Lernplattform zur Vorbereitung auf die IHK-Abschlussprüfung.",
    version="0.1.0"
)

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Willkommen bei der APT-Erfolg API!"}

app.include_router(users.router, prefix="/api")
app.include_router(cards.router, prefix="/api")
