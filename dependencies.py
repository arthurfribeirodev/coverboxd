from models import db,Users
from sqlalchemy.orm import Session, sessionmaker
from main import SECRET_KEY, ALGORITHM, oauth2_schme
from jose import jwt,JWTError
from fastapi import HTTPException, Depends

def session_grab():

    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schme), session: Session = Depends(session_grab)):
        try: 
            dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = dic_info.get("sub")
        except JWTError as error:
            print(error)
            raise HTTPException(status_code=401, detail="Token inválido")
        
        usertk = session.query(Users).filter(Users.id==user_id).first()
        if not usertk:
             raise HTTPException(status_code=401, detail="Acesso Inválido")
        return usertk