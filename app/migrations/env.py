from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core import get_settings  
from app.db.models import Base 
from dotenv import load_dotenv

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = get_settings().DATABASE_URL
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        # `config.get_section(config.config_ini_section)` is retrieving the configuration section
        # specified by `config.config_ini_section` from the Alembic configuration. This section
        # typically contains database connection settings and other configuration options needed for
        # running migrations online.
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()