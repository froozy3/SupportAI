from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from depends import get_session
from schemas import History, UserAsk, UserConfirm, UserResponse
from service import (
    FAQ_DATA,
    get_answer,
    get_embeddings,
    history_record,
    read_history,
    request_to_AI,
    retreive_relevant_faq,
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
