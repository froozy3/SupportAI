import cohere
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
import numpy as np

from constans import COHERE_API_KEY, FAQ_DATA, SIMILARITY_THRESHOLD
from models import HistoryDB
from schemas import History, UserAsk, UserResponse


co = cohere.AsyncClientV2(api_key=COHERE_API_KEY)  # create cohere client


def cosine_similiarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    # Calculate cosine similarity between two vectors
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


async def get_embeddings(texts: list[str]) -> list[np.ndarray]:
    # Get embeddings for a list of texts from Cohere API
    response = await co.embed(
        model="embed-english-v2.0",
        input_type="text",
        embedding_types=["float"],
        texts=texts,
    )
    return response.embeddings.float_


async def retreive_relevant_faq(
    question: str, faq_embeddings: list[np.ndarray], top_k=2
) -> list[str]:
    # Get embedding for the question
    question_embedding = (await get_embeddings([question]))[0]  # get vector
    # Calculate similarity with each FAQ embedding
    similarities = [
        cosine_similiarity(question_embedding, faq_emb) for faq_emb in faq_embeddings
    ]
    max_similirity = max(similarities)

    # If no FAQ is similar enough, raise error
    if max_similirity < SIMILARITY_THRESHOLD:
        raise HTTPException(400, "No relevant FAQ found for this question.")

    # Find top-k similar FAQs
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    relevant_faqs = {FAQ_DATA[i] for i in top_indices}
    return relevant_faqs


async def request_to_AI(question: str, context: list[str]) -> UserResponse:
    # Build prompt for AI with question and context
    prompt = (
        f"Question: {question}\n"
        f"Context:\n" + "\n".join(context) + "\n"
        "Please answer the question referencing the context above."
        "Give sentences to 30-40 symbols."
    )
    # Send chat request to Cohere AI model
    response = await co.chat(
        model="command-a-03-2025",
        messages=[cohere.UserChatMessageV2(content=prompt)],
    )
    answer = response.message.content[0].text
    return UserResponse(response=answer, context=context)


async def get_answer(session: AsyncSession, ask: UserAsk) -> UserResponse:
    # Main function to get answer for user question
    question = ask.question
    faq_embeddings = await get_embeddings(FAQ_DATA)  # embed FAQ data
    relevant_faq = await retreive_relevant_faq(
        question, faq_embeddings
    )  # get relevant FAQ
    answer = await request_to_AI(question, relevant_faq)  # get AI answer
    # Save Q&A to history
    history = History(
        question=question,
        context=relevant_faq,
        answer=answer.response,
    )
    await history_record(session, history)

    return answer


async def history_record(session: AsyncSession, history: History) -> None:
    # Save history record to database
    record_db = history.to_db()
    record_db.context = "\n".join(history.context)
    session.add(record_db)
    await session.commit()


async def read_history(session: AsyncSession) -> list[History]:
    # Read all history records from database
    stmt = select(HistoryDB)
    result = await session.execute(stmt)
    records = result.scalars().all()
    history_list = []
    for record in records:
        record.context = record.context.split("\n") if record.context else []
        history_list.append(History.model_validate(record))
    return history_list
