import pytest
from httpx import ASGITransport, AsyncClient
from main import app  # import FastAPI app instance


@pytest.mark.asyncio
async def test_api_ask_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Prepare the request body with the question
        data = {"question": "What i need to do what recover my account?"}

        # Send POST request to /api/ask endpoint
        response = await ac.post("/api/ask", json=data)
        json_data = response.json()

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200

        # Check that the response contains 'email' and 'phone' keywords
        assert "email" in json_data["response"]
        assert "phone" in json_data["response"]
