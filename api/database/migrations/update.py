import subprocess


async def upgrade_database():
    subprocess.run(["alembic", "upgrade", "head"])
