import os
import json
from threading import Thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import paho.mqtt.client as mqtt
from db import save_sensor_data, get_db
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------
# FASTAPI
# ---------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FallData(BaseModel):
    room_id: str
    status: str
    nilai_sensor: float

@app.post("/fall")
def insert_fall(data: FallData):
    print("[API] Received POST /fall:", data.dict())
    save_sensor_data(data.room_id, data.status, float(data.nilai_sensor))
    return {"message": "saved"}

@app.get("/fall")
def get_all():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM status_setection_fall ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


# ---------------------------------------------------
# MQTT
# ---------------------------------------------------
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("[MQTT RAW PAYLOAD]", msg.payload)
        print("[MQTT] Incoming payload:", payload)

        room_id = payload.get("room_id")
        status = payload.get("status")
        nilai_sensor = payload.get("nilai_sensor")

        if room_id is None or status is None: 
            print("[MQTT] ERROR: Payload tidak lengkap ->", payload)
            return

        save_sensor_data(room_id, status, nilai_sensor)
        print("[MQTT] SAVED:", room_id, status)

    except Exception as e:
        print("[MQTT] ERROR:", e)


def start_mqtt():
    print("[MQTT] Starting MQTT service...")

    client = mqtt.Client()

    # Jika menggunakan username/password MQTT
    if os.getenv("MQTT_USERNAME"):
        print("[MQTT] Using authentication...")
        client.username_pw_set(
            os.getenv("MQTT_USERNAME"),
            os.getenv("MQTT_PASSWORD")
        )

    client.on_message = on_message

    broker = os.getenv("MQTT_BROKER")
    port = int(os.getenv("MQTT_PORT"))
    topic = os.getenv("MQTT_TOPIC")

    print(f"[MQTT] Connecting to broker {broker}:{port} ...")

    try:
        client.connect(broker, port)
        print("[MQTT] Connected successfully!")
    except Exception as e:
        print("[MQTT] FAILED to connect:", e)

    print(f"[MQTT] Subscribing to topic: {topic}")
    client.subscribe(topic)

    print("[MQTT] Listening for incoming messages...")
    client.loop_forever()
    


# ---------------------------------------------------
# START MQTT THREAD
# ---------------------------------------------------
print("[SYSTEM] Starting FastAPI and MQTT service...")
mqtt_thread = Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

