from sqlalchemy import Table, Column, String, Boolean
from database import metadata

tasks = Table(
    "tasks",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("title", String(100), nullable=False),
    Column("description", String(255)),
    Column("completed", Boolean, default=False),
)