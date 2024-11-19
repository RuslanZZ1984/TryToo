from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

import fastapi_users.router
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field

from authentication.authentication import auth_backend
from authentication.database import User
from authentication.schemas import UserRead, UserCreate
from authentication.user_manager import get_user_manager

app = FastAPI(
    title="Trading App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
#
# async def common_parameters(
#         q: Union[str, None] = None, skip: int = 0, limit: int = 100
# ):
#     return {"q": q, "skip": skip, "limit": limit}
#
#
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons
#
# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons
