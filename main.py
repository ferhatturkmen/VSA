from fastapi import FastAPI
from routers import booking_router
from routers import message_router
from routers import payment_router
from routers import review_router
from routers import users_router
from routers import vehicles_router
from db import models
from db.database import engine



app = FastAPI()
app.include_router(booking_router.router)
app.include_router(message_router.router)
app.include_router(payment_router.router)
app.include_router(review_router.router)
app.include_router(users_router.router)
app.include_router(vehicles_router.router)

models.Base.metadata.create_all(engine)




@app.get ("/")
def example() :
    return {"example" : "example data"}

