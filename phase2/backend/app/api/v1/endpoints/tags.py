"""Tag API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.task_service import TagService
from app.schemas.task import TagSchema, TagCreate
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=SuccessResponse)
async def list_tags(
    session: AsyncSession = Depends(get_session)
):
    """List all tags for the current user."""
    tags = await TagService.list_tags(session)
    tag_responses = [TagSchema.model_validate(tag) for tag in tags]

    return SuccessResponse(data=[t.model_dump() for t in tag_responses])


@router.post("", response_model=SuccessResponse, status_code=201)
async def create_tag(
    tag_data: TagCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new tag."""
    tag = await TagService.create_tag(
        session,
        name=tag_data.name,
        color=tag_data.color
    )

    tag_response = TagSchema.model_validate(tag)
    return SuccessResponse(
        data=tag_response.model_dump(),
        message="Tag created successfully"
    )
