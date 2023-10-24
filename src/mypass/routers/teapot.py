from fastapi import APIRouter, status

router = APIRouter(tags=['teapot'])


@router.get('/teapot', status_code=status.HTTP_418_IM_A_TEAPOT)
async def teapot():
    return 'I am a teapot!'
