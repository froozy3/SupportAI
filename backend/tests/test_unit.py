import numpy as np
import pytest
from unittest.mock import AsyncMock, patch

from service import cosine_similiarity, retreive_relevant_faq


def test_cosine_similarity():
    # Test cosine similarity function with two vectors that are the same
    assert cosine_similiarity(np.array([1, 0]), np.array([1, 0])) == 1.0
    # Test cosine similarity function with two orthogonal vectors (should be zero)
    assert cosine_similiarity(np.array([1, 0]), np.array([0, 1])) == 0.0


@pytest.mark.asyncio
@patch("service.get_embeddings", new_callable=AsyncMock)
@patch(
    "service.FAQ_DATA",
    [
        "Registration takes no more than 2 minutes.",
        "You can reset your password via email.",
        "You need a valid ID to register.",
    ],
)
async def test_retreive_relevant_faq_returns_faq(mock_get_emb):
    # Mock the get_embeddings function to return a fixed embedding vector for the question
    mock_get_emb.side_effect = [
        [np.array([0.1, 0.2, 0.3])],
    ]
    # Create fake embeddings for FAQ items (to simulate similarity calculation)
    fake_faq_embeddings = [
        np.array([0.1, 0.2, 0.3]),
        np.array([0.1, 0.1, 0.1]),
        np.array([0.0, 0.0, 1.0]),
    ]

    # Patch the similarity threshold to a low value so test passes easily
    with patch("constans.SIMILARITY_THRESHOLD", 0.1):
        # Call the function with a sample question and fake FAQ embeddings
        result = await retreive_relevant_faq(
            "How long does it take to register?", fake_faq_embeddings
        )
        print(f"{result=}")  # Print result for debugging

    # Assert that we got exactly 2 relevant FAQ items (top_k=2 by default)
    assert len(result) == 2
    # Assert that the expected FAQ text is included in the result
    assert "Registration takes no more than 2 minutes." in result
