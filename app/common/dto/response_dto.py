from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel, Field
from math import ceil


T = TypeVar('T')


class PageResult(BaseModel, Generic[T]):
    """Page result for paginated responses"""
    items: List[T]
    page: int
    page_size: int
    total: int
    total_pages: int


class ApiResponse(BaseModel):
    """Standard API response"""
    success: bool = True
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
    data: Optional[Any] = None


def paginate(
    items: List[T],
    page: int,
    page_size: int,
    total: int
) -> PageResult[T]:
    """Create paginated result"""
    return PageResult(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=ceil(total / page_size) if page_size > 0 else 0
    )
