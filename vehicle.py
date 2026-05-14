import random
import time
import json
import hashlib
import requests

from datetime import datetime

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# -----------------------------------
# LOAD PRIVATE KEY
# -----------------------------------

with open("private.pem", "rb") as f:

    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# -----------------------------------
# INITIAL GPS LOCATION
# -----------------------------------

latitude = 12.91
longitude = 77.59

# -----------------------------------
# CONTINUOUS BSM GENERATION
# -----------------------------------

while True:

    # -----------------------------------
    # SIMULATE VEHICLE MOVEMENT
    # -----------------------------------

    latitude += random.uniform(-0.01, 0.01)

    longitude += random.uniform(-0.01, 0.01)

    speed = random.randint(20, 120)

    # -----------------------------------
    # RANDOM EVENT TYPE
    # -----------------------------------

    event = random.choice([
        "normal",
        "accident",
        "traffic",
        "emergency"
    ])

    # -----------------------------------
    # RANDOM ATTACK TYPE
    # -----------------------------------

    attack_type = random.choice([
        "normal",
        "spoof",
        "tamper"
    ])

    # -----------------------------------
    # GPS SPOOFING ATTACK
    # -----------------------------------

    if attack_type == "spoof":

        latitude = random.uniform(50, 90)

        longitude = random.uniform(50, 90)

    # -----------------------------------
    # CREATE BSM
    # -----------------------------------

    bsm = {

        "vehicle_id": "V101",

        "timestamp": str(datetime.now()),

        "latitude": round(latitude, 6),

        "longitude": round(longitude, 6),

        "speed": speed,

        "event": event
    }

    # -----------------------------------
    # CONVERT TO JSON
    # -----------------------------------

    bsm_json = json.dumps(bsm)

    # -----------------------------------
    # SHA256 HASH
    # -----------------------------------

    packet_hash = hashlib.sha256(
        bsm_json.encode()
    ).hexdigest()

    # -----------------------------------
    # ECDSA SIGNATURE
    # -----------------------------------

    signature = private_key.sign(

        packet_hash.encode(),

        ec.ECDSA(hashes.SHA256())
    )

    # -----------------------------------
    # FINAL PACKET
    # -----------------------------------

    packet = {

        "bsm": bsm,

        "hash": packet_hash,

        "signature": signature.hex()
    }

    # -----------------------------------
    # TAMPERING ATTACK
    # -----------------------------------

    if attack_type == "tamper":

        packet["bsm"]["speed"] = 200

    # -----------------------------------
    # SEND TO SERVER
    # -----------------------------------

    response = requests.post(

        "http://127.0.0.1:5000/receive",

        json=packet
    )

    # -----------------------------------
    # PRINT RESULTS
    # -----------------------------------

    print("Attack Type:", attack_type)

    print(response.json())

    print("-----------------------------------")

    # -----------------------------------
    # WAIT 2 SECONDS
    # -----------------------------------

    time.sleep(2)