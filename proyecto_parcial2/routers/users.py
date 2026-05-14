from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

from proyecto_parcial2.db.database import get_session
from proyecto_parcial2.db.models import User, UserCreate, UserPublic
from proyecto_parcial2.security.security import (
    hash_password,
    decode_access_token,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    new_user = User(
        name=user_data.name,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "Usuario creado exitosamente"}


@router.get("/me", response_model=UserPublic)
def get_me(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get("access_token")

    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(status_code=401, detail="No autorizado")

    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user