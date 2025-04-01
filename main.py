from fastapi import FastAPI
from routers import bookings_router
from routers import payments_router
from routers import reviews_router
from routers import users_router
from routers import vehicles_router
from db import models
from db.database import engine



app = FastAPI()
app.include_router(bookings_router.router)
app.include_router(payments_router.router)
app.include_router(reviews_router.router)
app.include_router(users_router.router)
app.include_router(vehicles_router.router)

models.Base.metadata.create_all(engine)




@app.get ("/")
def example() :
    return {"example" : "example data"}

