from uuid import uuid4

class Utility:
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid4())