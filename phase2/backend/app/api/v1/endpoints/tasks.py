"""Task API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.database import get_session
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.common import SuccessResponse
from app.models.task import PriorityEnum

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=SuccessResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task.

    - **title**: Required, 1-200 characters
    - **description**: Optional, max 1000 characters
    - **priority**: high, medium (default), or low
    - **due_date**: Optional ISO 8601 datetime
    - **tags**: Array of tag names (creates new tags if needed)
    """
    task = await TaskService.create_task(session, task_data)
    task_response = TaskResponse.model_validate(task)

    return SuccessResponse(
        data=task_response.model_dump(),
        message="Task created successfully"
    )


@router.get("", response_model=SuccessResponse)
async def list_tasks(
    status: str = Query("all", regex="^(all|active|completed)$"),
    priority: Optional[PriorityEnum] = None,
    tag: Optional[List[str]] = Query(None),
    sort: str = Query("created_desc", regex="^(created_desc|created_asc|priority_desc|due_asc|title_asc)$"),
    limit: int = Query(100, le=1000, ge=1),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    """
    List tasks with filtering and sorting.

    Filters:
    - **status**: all (default), active, completed
    - **priority**: Filter by priority level
    - **tag**: Filter by tag name (can specify multiple)

    Sorting:
    - created_desc (default), created_asc, priority_desc, due_asc, title_asc

    Pagination:
    - **limit**: Max results (default 100, max 1000)
    - **offset**: Skip N results
    """
    tasks, total = await TaskService.list_tasks(
        session,
        status=status,
        priority=priority,
        tags=tag,
        sort_by=sort,
        limit=limit,
        offset=offset
    )

    task_responses = [TaskResponse.model_validate(task) for task in tasks]

    return SuccessResponse(
        data={
            "tasks": [t.model_dump() for t in task_responses],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    )


@router.get("/{task_id}", response_model=SuccessResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a specific task by ID."""
    task = await TaskService.get_task_by_id(session, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with ID {task_id} not found"
                }
            }
        )

    task_response = TaskResponse.model_validate(task)
    return SuccessResponse(data=task_response.model_dump())


@router.patch("/{task_id}", response_model=SuccessResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Update a task (partial update).

    All fields are optional. Only provided fields will be updated.
    """
    # Validate at least one field provided
    if not any(task_data.model_dump(exclude_unset=True).values()):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "At least one field must be provided"
                }
            }
        )

    task = await TaskService.update_task(session, task_id, task_data)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with ID {task_id} not found"
                }
            }
        )

    task_response = TaskResponse.model_validate(task)
    return SuccessResponse(
        data=task_response.model_dump(),
        message="Task updated successfully"
    )


@router.delete("/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a task permanently."""
    success = await TaskService.delete_task(session, task_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with ID {task_id} not found"
                }
            }
        )

    return SuccessResponse(
        data=None,
        message="Task deleted successfully"
    )
