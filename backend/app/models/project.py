from typing import Optional
from enum import Enum
from datetime import date

from app.models.core import IDModelMixin, CoreModel


class ProjectStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    done = "full_clean"


class ProjectBase(CoreModel):
    """
    Base - all shared attributes of a Project resource
    Optional type declaration will specify that any attribute not passed in when creating the model instance will be set to None
    """
    title: Optional[str]
    description: Optional[str]
    created_date: Optional[date]
    due_date: Optional[date]
    status: Optional[ProjectStatus]


class ProjectCreate(ProjectBase):
    """
    Create - attributes required to create a new resource - used at POST requests
    """
    title: str
    description: str
    due_date: date


class ProjectUpdate(ProjectBase):
    """
    Update - attributes that can be updated - used at PUT requests
    """
    title: str
    description: str
    created_date: date
    due_date: date
    status: ProjectStatus


class ProjectInDB(IDModelMixin, ProjectBase):
    """
    InDB - attributes present on any resource coming out of the database
    """
    title: str
    description: str
    created_date: date
    due_date: date
    status: ProjectStatus


class ProjectPublic(IDModelMixin, ProjectBase):
    """
    Public - attributes present on public facing resources being returned from GET, POST, and PUT requests
    """
    pass