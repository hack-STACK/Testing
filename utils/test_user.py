import uuid


def generate_user() -> dict:
    """Generate a unique isolated test user.
    
    Creates a complete user identity for each test to acquire its own isolated test account.
    No persistence between test runs.
    
    Returns:
        dict: User object with keys:
            - "name" (str): User display name
            - "email" (str): Unique email address
            - "password" (str): Valid password for the application
    """
    return {
        "name": "Juan Testing",
        "email": f"juan.testing.{uuid.uuid4().hex[:8]}@gmail.com",
        "password": "Binus123!"
    }
