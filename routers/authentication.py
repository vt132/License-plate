from fastapi_utils.inferring_router import InferringRouter
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from common.security import AuthAPI
from schemas.token import Token

router = InferringRouter()


@router.post("/login", response_model=Token)
async def login(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    return await AuthAPI.login(request, form_data)
