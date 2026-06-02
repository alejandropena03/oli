from __future__ import annotations

from fastapi import APIRouter

from packages.model_router import get_model_status, test_model
from packages.model_router.status import ModelStatus, ModelTestResult

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/status", response_model=ModelStatus)
def model_status() -> ModelStatus:
    return get_model_status()


@router.post("/test", response_model=ModelTestResult)
def model_test() -> ModelTestResult:
    return test_model()

