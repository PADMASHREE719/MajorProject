from database import save_to_dataset
from flask import Flask, request
import hashlib
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# Load public key
with open("../vehicle/public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

previous_location = None

@app.route('/receive', methods=['POST'])
def receive():

    global previous_location

    data = request.json

    bsm = data['bsm']
    received_hash = data['hash']
    signature = bytes.fromhex(data['signature'])

    # Recalculate hash
    recalculated_hash = hashlib.sha256(
        json.dumps(bsm).encode()
    ).hexdigest()

    # Integrity verification
    if recalculated_hash != received_hash:
        save_to_dataset(bsm,"REJECT")
        return {
            "status": "REJECT",
            "reason": "Hash mismatch"
        }

    # Signature verification
    try:
        public_key.verify(
            signature,
            received_hash.encode(),
            ec.ECDSA(hashes.SHA256())
        )
    except:
        save_to_dataset(bsm,"REJECT")
        return {
            "status": "REJECT",
            "reason": "Invalid signature"
        }

    # --------------------------
    # GPS Spoof Detection Layer
    # --------------------------

    lat = bsm['latitude']
    lon = bsm['longitude']

    if previous_location:

        prev_lat, prev_lon = previous_location

        # Very simple spoof logic
        if abs(lat - prev_lat) > 0.5:
            save_to_dataset(bsm,"SUSPICIOUS")
            return {
                "status": "SUSPICIOUS",
                "reason": "Possible GPS spoofing"
            }

    previous_location = (lat, lon)

    save_to_dataset(bsm,"ACCEPT")
    return {
        "status": "ACCEPT",
        "reason": "Trusted BSM"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)