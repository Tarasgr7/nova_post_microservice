from fastapi import HTTPException,status

def verify_worker_role(user):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    if user.get('role') != "worker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only workers can perform this action")