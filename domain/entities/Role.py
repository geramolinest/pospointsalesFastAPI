from uuid import uuid4, UUID

from sqlalchemy import Uuid as ALQUUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils import Config

from .Base import Base

class Role(Base):
    
    __tablename__ = 'roles'
    
    id: Mapped[UUID] = mapped_column(ALQUUID, primary_key=True, default=uuid4)
    role_name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    normalized_role_name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False, index=True)
    users: Mapped[list['User']] = relationship(secondary='roles_users', back_populates='roles') # type: ignore

    @staticmethod
    def get_admin_role( config: Config):

        admin_role_name: str = config.get_value('ADMIN_ROLE') or 'ADMIN'

        role: Role = Role(role_name = admin_role_name.strip(), normalized_role_name = admin_role_name.upper().strip())

        return role
    