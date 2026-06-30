from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.resolvers.mutations import mutation
from app.resolvers.queries import activity_log_type, project_type, query, task_type
from app.routes import auth, health
from app.schema.context import get_context
from app.schema.type_defs import type_defs

schema = make_executable_schema(
    type_defs, query, mutation, task_type, activity_log_type, project_type
)

graphql_app = GraphQL(schema, context_value=get_context, debug=settings.ENVIRONMENT != "production")

app = FastAPI(title="Backend Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/graphql", graphql_app)

app.include_router(health.router)
app.include_router(auth.router)


@app.middleware("http")
async def close_db_session(request, call_next):
    response = await call_next(request)
    db = getattr(request.state, "db_session", None)
    if db:
        db.close()
    return response


@app.get("/")
def root():
    return {"message": "GraphQL API running — visit /graphql"}
