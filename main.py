from fastapi import FastAPI, HTTPException, Depends, Query
from typing import Annotated, List, Optional
from operator import attrgetter
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class AccountBase(BaseModel):
    username : str
    email : str
    existing_user : Optional[bool] = False
    date_requested : str
    date_au_created : Optional[str] = ""
    date_training_assigned : Optional[str] = ""
    date_account_created : Optional[str] = ""
    date_account_activated : Optional[str] = ""
    date_account_inactivated : Optional[str] = ""

class AccountModel(AccountBase):
    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

@app.get("/accounts/{sortOrder}", response_model = List[AccountModel])
async def read_account(
    db: db_dependency,
    skip: int = 0,
    limit: int = 100,
    sortOrder: Optional[str] = '',
    filter: Optional[str] = Query(None, alias="filter")
):
    accounts = db.query(models.Account).offset(skip).limit(limit).all()

    if filter:
        accounts = [account for account in accounts if not getattr(account, filter, None)]

    if sortOrder:
        sortField = sortOrder.split(' ', 1)[0] if ' ' in sortOrder else sortOrder
        return sorted(accounts, key=attrgetter(sortField), reverse=sortOrder.endswith(" desc"))
    return accounts

@app.get("/account/{id}")
async def read_account(id : int, db: db_dependency):
    account = db.query(models.Account).get(id)
    return account

@app.post("/accounts/", response_model = AccountModel)
async def create_account(account: AccountBase, db: db_dependency):
    if not account.username or not account.email or not account.date_requested:
        raise HTTPException(status_code=404, detail="Required fields: username or email or date_requested not populated")
    db_account = models.Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.put("/account/{id}", response_model = AccountModel)
async def update_account(id : int, db: db_dependency, account_data: AccountBase):
    account = db.query(models.Account).filter(models.Account.id == id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    for field in account_data.__dict__:
        setattr(account, field, getattr(account_data, field))
    db.commit()
    return account

@app.delete("/account/{id}")
async def delete_account(id: int, db: db_dependency):
    account = db.query(models.Account).filter(models.Account.id == id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return account