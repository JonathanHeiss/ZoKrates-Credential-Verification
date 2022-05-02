import hashlib
from zokrates_pycrypto.eddsa import PrivateKey, PublicKey
from zokrates_pycrypto.field import FQ
from zokrates_pycrypto.utils import write_signature_for_zokrates_cli
import struct
import sys

def write_signature_for_zokrates_cli(pk, sig, msg):
    "Writes the input arguments for verifyEddsa in the ZoKrates stdlib to file."
    sig_R, sig_S = sig
    args = [sig_R.x, sig_R.y, sig_S, pk.p.x.n, pk.p.y.n]
    args = " ".join(map(str, args))
    M0 = msg.hex()[:64]
    M1 = msg.hex()[64:]
    b0 = [str(int(M0[i:i+8], 16)) for i in range(0,len(M0), 8)]
    b1 = [str(int(M1[i:i+8], 16)) for i in range(0,len(M1), 8)]
    args = args + " " + " ".join(b0 + b1)
    return args

if __name__ == "__main__":
    signKey = PrivateKey.from_rand()

    # value = "19810902".encode().rjust(64, b"\x00")
    #value = int.to_bytes(19810902, 64, 'little')
    value = int.to_bytes(45054, 64, 'big')

    resultHash = hashlib.sha256(value).digest()
    resultHash += resultHash

    sig = signKey.sign(resultHash)
            
    #Create Public Key
    verifyKey = PublicKey.from_private(signKey)

    outputs = [
        "1337",
        "51966",
        " ".join([str(i) for i in struct.unpack(">16I", value)]),
        write_signature_for_zokrates_cli(verifyKey, sig, resultHash),
    ]
    sys.stdout.write(" ".join(outputs))

