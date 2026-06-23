from fastapi import FastAPI
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL

from app.schema.type_defs import type_defs
from app.schema.context import get_context
from app.resolvers.queries import query, task_type
from app.resolvers.mutations import mutation

from app.models import user_model, project_model, task_model, membership_model

schema = make_executable_schema(type_defs, query, mutation, task_type)

graphql_app = GraphQL(schema, context_value=get_context, debug=True)

app = FastAPI(title="Backend Project")
app.mount("/graphql", graphql_app)


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