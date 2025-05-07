# Automatically created __init__.py
import os

from .mock import MockAssemblyService
from .prod import RealAssemblyService

env = os.getenv("ENV", "local")

if env == "prod":
    ia_service = RealAssemblyService()
if env == "dev":
    ia_service = RealAssemblyService()
else:
    ia_service = MockAssemblyService()
