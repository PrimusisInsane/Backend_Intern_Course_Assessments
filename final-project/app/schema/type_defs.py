import os

from ariadne import load_schema_from_path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
type_defs = load_schema_from_path(os.path.join(BASE_DIR, "schema.graphql"))
