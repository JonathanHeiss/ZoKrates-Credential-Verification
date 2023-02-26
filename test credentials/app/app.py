from flask import Flask, abort
import os
import json
from zokrates_pycrypto.eddsa import PrivateKey, PublicKey
import hashlib

CREDENTIALS_DB = os.environ.get("CREDENTIALS_DB", "../data/credentials.json")

app = Flask(__name__)
signKey = PrivateKey.from_rand()

@app.route("/vc/<credential_id>")
def get_vc(credential_id):
    credential_id = int(credential_id)
    with open(CREDENTIALS_DB, "r") as f:
        data  = json.loads(f.read())
        if credential_id >= len(data):
            abort(404)
        target_credential = data[credential_id]

        output = []
        for key, value in target_credential.items():
            credential_hash = hashlib.sha256(value.encode()).digest()
            credential_hash += credential_hash
            sig = signKey.sign(credential_hash)
            output.append({
                "name": key,
                "value": value,
                "signature": {
                    "r": {
                        "x": str(sig[0].x),
                        "y": str(sig[0].y)
                    },
                    "s": str(sig[1])
                }
            })
        return {
            "vc": output
        }


