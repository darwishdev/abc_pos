from __future__ import annotations
from ..repo.printing_repo import PrintingRepository
from ..usecase.printing_usecase import PrintingUseCase

# Construct once per process at import time
repo = PrintingRepository()
printing_uc = PrintingUseCase(repo=repo)

__all__ = ["printing_uc"]
