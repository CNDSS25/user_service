from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.core.models import User
from app.core.use_cases import UserUseCases
from fastapi.responses import JSONResponse
from app.dependencies import get_db_adapter, get_jwt_adapter



router = APIRouter()


@router.post("/token/verify", tags=["Authentication"])
async def verify_token(token: str, jwt_adapter=Depends(get_jwt_adapter)):
    """
    Verifiziert ein JWT-Token und gibt die Payload-Daten zurück.
    """
    try:
        payload = jwt_adapter.decode_access_token(token)
        return payload  # Gibt die Payload-Daten wie 'sub' (E-Mail) zurück
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")


@router.get("/users/me", response_model=User, tags=["Users"])
async def get_current_user(
    request: Request,
    db_adapter=Depends(get_db_adapter),
    jwt_adapter=Depends(get_jwt_adapter)
):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt_adapter.decode_access_token(session_id)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await db_adapter.find_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Gebe auch den Token zurück
        return {**user.dict(), "session_token": session_id}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

@router.post("/login/", tags=["Authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_adapter=Depends(get_db_adapter),
    jwt_adapter=Depends(get_jwt_adapter)  # JWTAdapter als Dependency hinzufügen
):
    """
    Authentifiziert einen Benutzer und setzt ein Session-Cookie.
    """
    use_cases = UserUseCases(db=db_adapter)

    # Prüfe Anmeldedaten
    user = await use_cases.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Session-ID erstellen (z. B. zufälliger Token oder JWT)
    session_id = jwt_adapter.create_access_token(data={"sub": user.email})

    # Setze das Cookie in der Antwort
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="session_id",  # Name des Cookies
        value=session_id,  # Token oder eindeutige ID
        httponly=False,  # Verhindert JavaScript-Zugriff
        max_age=36000,  # Ablaufzeit in Sekunden (10 Stunde)
        secure=False,  # Setze auf True, wenn HTTPS verwendet wird
        samesite="Lax",  # Verhindert Cross-Site-Attacken
    )
    return response

@router.post("/logout/", tags=["Authentication"])
async def logout(response: JSONResponse):
    """
    Logout des Benutzers: Löscht das Session-Cookie.
    """
    response = JSONResponse({"message": "Logout successful"})
    response.delete_cookie("session_id")
    return response

@router.post("/register/", response_model=User , tags=["Users"])
async def register_user(user: User, db_adapter=Depends(get_db_adapter)):
    """
    Registriert einen neuen Benutzer.
    """
    use_cases = UserUseCases(db=db_adapter)
    try:
        return await use_cases.register_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: str, db_adapter=Depends(get_db_adapter)):
    """
    Ruft einen Benutzer anhand seiner ID ab.
    """
    use_cases = UserUseCases(db=db_adapter)
    try:
        return await use_cases.get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(user_id: str, user_update: dict, db_adapter=Depends(get_db_adapter)):
    """
    Aktualisiert einen Benutzer anhand seiner ID.
    """
    use_cases = UserUseCases(db=db_adapter)
    try:
        return await use_cases.update_user(user_id, user_update)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: str, db_adapter=Depends(get_db_adapter)):
    """
    Löscht einen Benutzer anhand seiner ID.
    """
    use_cases = UserUseCases(db=db_adapter)
    success = await use_cases.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/")
async def root():
    """
    Test-Endpunkt, um sicherzustellen, dass die API läuft.
    """
    return {"message": "User Service is running"}