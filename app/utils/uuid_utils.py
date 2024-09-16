import uuid

def get_uuid() -> str:
    return uuid.uuid4()

def verify_uuid(id: str)-> bool:
    try:
        uuid.UUID(id)
        return True
    except Exception:
        return False