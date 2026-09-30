from fastapi import FastAPI

from orders_api.api.routes import router

app = FastAPI(
    title="Final Orders API",
    version="0.1.0",
    description="API de órdenes para una tienda de figuras de acción.",
)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router)
