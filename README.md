# coffee-app-be

## Details
coffee-app-be is a RESTful API for coffee-app-fe, a studies project. Features:

- storing available coffees
- storing orders

## Tech stack
- Python
- FastAPI

## Docs
Interactive docs can be found at https://localhost:8000/docs. Available endpoints:

`GET /coffees`

#### Response
All available coffees.

---

`GET /coffees/:id`

#### Response
Returns a single coffee.

---

`POST /order`
#### Request
Payload: order data.

#### Response
Returns: Created order.
