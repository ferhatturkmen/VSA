from fastapi import FastAPI
from routers import bookings_router, payments_router, reviews_router, users_router, vehicles_router
from auth import authentication
from db import models
from db.database import engine



app = FastAPI()
app.include_router(bookings_router.router)
app.include_router(payments_router.router)
app.include_router(reviews_router.router)
app.include_router(users_router.router)
app.include_router(vehicles_router.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)




@app.get ("/")
def example() :
    return {"example" : "example data"}

