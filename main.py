from fastapi import FastAPI, File, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

class DataRecord(BaseModel):
    lab_id: int
    count: int
    timestamp: str  # Usa ISO 8601 format (e.g., "2024-12-13T15:03:00Z")

app = FastAPI()

DATABASE_URL = "postgresql://postgres:wdf3VquQsgwQachtnDGr@database-iot.cbo0oy8e43y8.us-east-2.rds.amazonaws.com/postgres"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.get("/data")
async def get_all_data():

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM iot.message")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data 

@app.get("/data/{id}")
async def get_data_by_id(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM iot.message WHERE id = %s", (id,))
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Data not found")

    return data

@app.post("/data")
async def add_data(record: DataRecord):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
      INSERT INTO iot.message (lab_id, count, timestamp)
      VALUES (%s, %s, %s)
    """

    cursor.execute(insert_query, (record.lab_id, record.count, record.timestamp))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Data added successfully"}

@app.put("/data/{id}")
async def update_data(id: int, record: DataRecord):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_query = """
      UPDATE iot.message
      SET lab_id = %s, count = %s, timestamp = %s
      WHERE id = %s
    """

    cursor.execute(update_query, (record.lab_id, record.count, record.timestamp, id))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Data updated successfully"}

@app.delete("/data/{id}")
async def delete_data(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM iot.message WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Data deleted successfully"}
  