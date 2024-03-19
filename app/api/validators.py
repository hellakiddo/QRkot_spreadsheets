from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models.charity_project import CharityProject

PROJECT_NOT_FOUND_ERROR = 'Проект не найден'
PROJECT_EXISTS_ERROR = 'Проект с таким названием уже есть.'
FORBIDDEN_UPDATE_ERROR = 'Закрытый проект нельзя редактировать.'
INVESTED_RPOJECT_DELETE_ERROR = (
    'В проект инвестировали, невозможно удалить.'
)
INVALID_INVESTED_AMOUNT_ERROR = (
    'Новая сумма должна быть больше ранее внесенной'
)


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charityproject_crud.get(
        object_id=project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=PROJECT_NOT_FOUND_ERROR
        )
    return charity_project


async def check_project_was_closed(
    charity_project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charityproject_crud.get(
        charity_project_id, session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            detail=FORBIDDEN_UPDATE_ERROR,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = (
        await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
    ).scalars().first()
    if charity_project_id:
        raise HTTPException(
            detail=PROJECT_EXISTS_ERROR,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_project_was_invested(
    charity_project: CharityProject,
):
    if charity_project.invested_amount > 0:
        raise HTTPException(
            detail=INVESTED_RPOJECT_DELETE_ERROR,
            status_code=HTTPStatus.BAD_REQUEST
        )


async def check_correct_full_amount_for_update(
    project_id: int,
    session: AsyncSession,
    full_amount_to_update: PositiveInt
):
    db_project_invested_amount = await (
        charityproject_crud.get(
            project_id, session
        )
    )
    if full_amount_to_update < db_project_invested_amount.invested_amount:
        raise HTTPException(
            detail=INVALID_INVESTED_AMOUNT_ERROR,
            status_code=HTTPStatus.BAD_REQUEST
        )
    if full_amount_to_update == db_project_invested_amount.invested_amount:
        db_project_invested_amount.fully_invested = True
