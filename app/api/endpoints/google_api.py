from starlette import status

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

google_api_router = APIRouter()


@google_api_router.post(
    '/',
    response_model=list[dict[str, int]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(
        wrapper_services
    )
    drive_service = await set_user_permissions(
        spreadsheet_id,
        wrapper_services,
    )
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            await charityproject_crud.get_projects_by_completion_rate(
                session,
            ),
            wrapper_services,
        )
    except ValueError as error:
        await wrapper_services.as_service_account(
            drive_service.files.delete(fileId=spreadsheet_id),
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        )
    return spreadsheet_url
