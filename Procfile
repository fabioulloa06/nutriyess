web: python -m pip install -r requirements.txt && python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)" && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
