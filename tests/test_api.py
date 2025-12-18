import pytest
from httpx import AsyncClient, ASGITransport
from security import create_refresh_token, create_access_token
from queries import get_user_info

from main import app


@pytest.mark.asyncio
async def test_client_get():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/users/me/",
                                headers={
                                    "Authorization": f"Bearer {create_access_token(get_user_info('anton'))}"
                                }
                                )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_client_access_token():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.post("/access_token",
                                 data={"username": "anton", "password": "1234", "grant_type": "password"}
                                 )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_client_refresh_token():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.post("/refresh_token",
                                 headers={
                                     "Authorization": f"Bearer {create_refresh_token(get_user_info('anton'))}"
                                 }
                                 )
        assert response.status_code == 200
