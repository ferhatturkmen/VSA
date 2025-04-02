from fastapi import APIRouter

router = APIRouter(
    prefix = "/bookings",
    tags = ["bookings"]
)

@app.get ("/")
def example() :
    return {"example" : "This is an example of Booking Router"}