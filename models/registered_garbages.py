from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base

class RegisteredGarbage(Base):
    __tablename__ = 'registered_garbages'
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(256), unique=True, nullable=False)
    
    @classmethod
    def insert(cls, session: Session, value: str):
        new_garbage = cls(value=value)
        session.add(new_garbage)
        session.commit()
        session.refresh(new_garbage)
        return new_garbage
    
    @classmethod
    def delete(cls, session: Session, garbage_id: int):
        garbage = session.query(cls).filter(cls.id == garbage_id).first()
        if garbage:
            session.delete(garbage)
            session.commit()
            return True
        return False
    
    @classmethod
    def get(cls, session: Session, garbage_id: int):
        return session.query(cls).filter(cls.id == garbage_id).first()
    
    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()
