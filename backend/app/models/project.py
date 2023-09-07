from typing import Optional
from enum import Enum
from datetime import datetime

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
    created_date: Optional[datetime]
    due_date: Optional[datetime]
    status: Optional[ProjectStatus] = 'not_started'


class ProjectCreate(ProjectBase):
    """
    Create - attributes required to create a new resource - used at POST requests
    """
    title: str
    description: str
    due_date: datetime


class ProjectUpdate(ProjectBase):
    """
    Update - attributes that can be updated - used at PUT requests
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[ProjectStatus] = 'not_started'


class ProjectInDB(IDModelMixin, ProjectBase):
    """
    InDB - attributes present on any resource coming out of the database
    """
    title: str
    description: str
    created_date: datetime
    due_date: datetime
    status: ProjectStatus


class ProjectPublic(IDModelMixin, ProjectBase):
    """
    Public - attributes present on public facing resources being returned from GET, POST, and PUT requests
    """
    pass