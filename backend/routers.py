from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from depends import get_session
from schemas import History, UserAsk, UserResponse
from service import (
    get_answer,
    read_history,
)


router = APIRouter()


@router.post("/ask", response_model=UserResponse)
async def post_ask(
    ask: UserAsk, session: AsyncSession = Depends(get_session)
) -> UserResponse:
    return await get_answer(session, ask)


@router.get("/history")
async def get_history(
    session: AsyncSession = Depends(get_session),
) -> list[History]:
    return await read_history(session)
