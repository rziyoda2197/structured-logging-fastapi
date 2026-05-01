import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import uuid

app = FastAPI()

# Structured logging uchun logger yaratamiz
logger = logging.getLogger(__name__)

# Request_id uchun funksiya yaratamiz
def get_request_id(request: Request):
    return request.headers.get("X-Request-Id", str(uuid.uuid4()))

# Structured logging uchun format yaratamiz
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(request_id)s - %(message)s")

# Request_id uchun middleware yaratamiz
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = get_request_id(request)
    logger.info(f"Request started: {request_id}")
    response = await call_next(request)
    logger.info(f"Request finished: {request_id}")
    return response

# Structured logging uchun funksiya yaratamiz
def log_request(request: Request, status_code: int, message: str):
    request_id = get_request_id(request)
    logger.info(f"Request {request_id} finished with status code {status_code}: {message}")

# Route uchun funksiya yaratamiz
@app.get("/hello")
async def hello_world(request: Request):
    log_request(request, 200, "Hello world!")
    return {"message": "Hello world!"}

# Route uchun funksiya yaratamiz
@app.get("/error")
async def error_world(request: Request):
    log_request(request, 500, "Error!")
    return JSONResponse(content={"message": "Error!"}, status_code=500)
```

Bu kodda FastAPI uchun request_id ni qo'shish uchun middleware yaratildi. Ushbu middleware har bir request uchun request_id ni yaratib, logga yozadi. Shuningdek, har bir route uchun log funksiyasi yaratildi, u request_id, status_code va message ni logga yozadi.
