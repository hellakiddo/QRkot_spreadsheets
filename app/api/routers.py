from fastapi import APIRouter

from app.api.endpoints import charityproject_router, donations, users
from app.api.endpoints.google_api import google_api_router

USER_PREFIX = ''
DONATION_PREFIX = '/donation'
CHARITY_PROJECT_PREFIX = '/charity_project'

GOOGLE_PREFIX = '/google'
GOOGLE_TAGS = ['Google']

USER_TAGS = []
DONATION_TAGS = ['Donations']
CHARITY_PROJECT_TAGS = ['Charity Projects']

main_router = APIRouter()

main_router.include_router(
    users.router,
    prefix=USER_PREFIX,
    tags=USER_TAGS
)

main_router.include_router(
    donations.router,
    prefix=DONATION_PREFIX,
    tags=DONATION_TAGS
)

main_router.include_router(
    charityproject_router.router,
    prefix=CHARITY_PROJECT_PREFIX,
    tags=CHARITY_PROJECT_TAGS
)
main_router.include_router(
    google_api_router,
    prefix=GOOGLE_PREFIX,
    tags=GOOGLE_TAGS
)