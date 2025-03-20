"""Template App
"""
from fastapi import APIRouter, Depends

from api.firebase_auth import get_firebase_user


firebase_router = APIRouter()


@firebase_router.get('/firebase_user')
async def firebase_user(
    user = Depends(get_firebase_user)
):
    """Test endpoint that depends on authenticated firebase
    """
    return user