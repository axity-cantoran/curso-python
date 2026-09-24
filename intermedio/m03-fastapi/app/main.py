from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.orders import router as orders_router

app = FastAPI(
    title="Orders API",
    version="1.0.0",
)


""" @app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        user = session.query(User).filter_by(
            email="ana@example.com"
        ).first()

        if user is None:
            session.add(
                User(
                    email="ana@example.com",
                    hashed_password=hash_password("secreto"),
                )
            )
            session.commit() """


app.include_router(orders_router)
app.include_router(auth_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
