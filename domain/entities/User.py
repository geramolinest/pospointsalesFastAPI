from uuid import uuid4, UUID
from sqlalchemy import Uuid as ALQUUID, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils import Config
from utils.security import BCrypt

from . import Base

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[UUID]  = mapped_column(ALQUUID, primary_key=True, unique=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(25), unique=True,nullable=False)
    normalized_username: Mapped[str] = mapped_column(String(25), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    normalized_email: Mapped[str] = mapped_column(String(25), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles: Mapped[list['Role']] = relationship(secondary='roles_users', back_populates='users', lazy='selectin') # type: ignore

    @staticmethod
    def get_admin_user( config: Config ):
    
        admin_username: str = config.get_value('ADMIN_USER') or 'ADMIN'


        admin_email: str = config.get_value('ADMIN_USER_EMAIL') or 'email@example.com'

        admin_password: str = config.get_value('ADMIN_USER_PASS') or 'PASSWORD123!'

        bcrypt: BCrypt = BCrypt()

        return User( 
                    username=admin_username.strip(), 
                    normalized_username=admin_username.upper().strip(), 
                    email=admin_email.strip(),
                    normalized_email=admin_email.upper().strip(),
                    password=bcrypt.hash_password(admin_password.strip())
                )
    