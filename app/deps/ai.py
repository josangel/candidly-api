"""Dependencies for the application."""

from app.core.config import settings
from app.services.assembly.mock import MockAssemblyService
from app.services.assembly.prod import AssemblyService

if settings.assembly_mock:
    ia_service = MockAssemblyService()
else:
    ia_service = AssemblyService()
