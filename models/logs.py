from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base

class Log(Base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    
    @classmethod
    def insert(cls, session: Session, action: str, description: str):
        new_log = cls(action=action, description=description)
        session.add(new_log)
        session.commit()
        session.refresh(new_log)
        return new_log
    
    @classmethod
    def get(cls, session: Session, log_id: int):
        return session.query(cls).filter(cls.id == log_id).first()
    
    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()
