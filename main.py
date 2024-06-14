from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, UserGameResult 
from pydantic import BaseModel
from typing import List

app = FastAPI()


@app.post("/update_victory_count/")
async def update_victory_count(game_results: List[GameResultModel]):
    db = SessionLocal()
    try:
        for result in game_results:
            existing_user = db.query(UserGameResult).filter(UserGameResult.name == result.name).first()
            if existing_user:
                if result.status == "WIN":
                    existing_user.victories += 1
                else:
                    existing_user.victories -= 1
                db.commit()
            else:
                new_user = UserGameResult(name=result.name)
                db.add(new_user)
                if result.status == "WIN":
                    new_user.victories = 1
                db.commit()
        return {"message": "Victory counts updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()