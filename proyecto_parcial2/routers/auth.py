import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from proyecto_parcial2.db.database import get_session
from proyecto_parcial2.db.models import User
from proyecto_parcial2.security.security import (
    verify_password,
    dummy_verify,
    create_access_token,
)

EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "3"))

router = APIRouter(tags=["auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user:
        dummy_verify()
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(user.username)

    response = JSONResponse(content={"access_token": token, "token_type": "bearer"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=EXPIRE_MINUTES * 60,
        samesite="lax",
    )
    return response