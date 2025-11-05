from alembic import context
from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
import sys

# Добавляем путь до нашего приложения
sys.path.append(os.getcwd())

# Импортируем модели и метаданные базы данных
from models import Base

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def process_revision_directives(context, revision, directives):
        script_directory = ScriptDirectory.from_config(context.config)
        head_revision = script_directory.get_current_head()

        if head_revision is None:
            new_rev_id = 1
        else:
            last_rev_id = int(head_revision.lstrip('0'))
            new_rev_id = last_rev_id + 1

        formatted_new_rev_id = f"{new_rev_id:04}"
        directives[0].rev_id = formatted_new_rev_id

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          process_revision_directives=process_revision_directives)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()