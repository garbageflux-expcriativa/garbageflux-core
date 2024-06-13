from sqlalchemy.orm import Session
from models import RegisteredGarbage
from models import RFID

def add_id_to_register(session: Session, new_id: str):
    if not session.query(RegisteredGarbage).filter(RegisteredGarbage.value == new_id).first():
        new_registered_garbage = RegisteredGarbage(value=new_id)
        session.add(new_registered_garbage)
        session.commit()
        return True
    return False

def remove_id_from_register(session: Session, removal_id: str):
    registered_garbage = session.query(RegisteredGarbage).filter(RegisteredGarbage.value == removal_id).first()
    if registered_garbage:
        session.delete(registered_garbage)
        session.commit()
        return True
    return False

def add_rfid_to_register(session: Session, new_id: str):
    if not session.query(RFID).filter(RFID.value == new_id).first():
        new_rfid = RFID(value=new_id)
        session.add(new_rfid)
        session.commit()
        return True
    return False

def remove_rfid_from_register(session: Session, removal_id: str):
    rfid = session.query(RFID).filter(RFID.value == removal_id).first()
    if rfid:
        session.delete(rfid)
        session.commit()
        return True
    return False

def is_id_registered(session: Session, check_id: str):
    return session.query(RegisteredGarbage).filter(RegisteredGarbage.value == check_id).first() is not None

def return_ids(session: Session):
    return [registered_garbage.value for registered_garbage in session.query(RegisteredGarbage).all()]

def return_rfids(session: Session):
    return [rfid.value for rfid in session.query(RFID).all()]
