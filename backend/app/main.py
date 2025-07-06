from fastapi import FastAPI
from app.database import engine
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(    
    title="Issue Tracker API",
    description="API for tracking issues with role-based access and background stats.",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend Running"}

from app.auth import routes as auth_route
from app.issues import routes as issue_routes
from app.users import routes as user_routes
from app.stats import route as stats


app.include_router(auth_route.router, prefix="/auth")
app.include_router(issue_routes.router)
app.include_router(user_routes.router)
app.include_router(stats.router)
