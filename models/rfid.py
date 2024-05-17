from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import Base

class RFID(Base):
    __tablename__ = 'rfid'
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(256), unique=True, nullable=False)
    
    @classmethod
    def insert(cls, session: Session, value: str):
        new_rfid = cls(value=value)
        session.add(new_rfid)
        session.commit()
        session.refresh(new_rfid)
        return new_rfid
    
    @classmethod
    def delete(cls, session: Session, rfid_id: int):
        rfid = session.query(cls).filter(cls.id == rfid_id).first()
        if rfid:
            session.delete(rfid)
            session.commit()
            return True
        return False
    
    @classmethod
    def get(cls, session: Session, rfid_id: int):
        return session.query(cls).filter(cls.id == rfid_id).first()
    
    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()
