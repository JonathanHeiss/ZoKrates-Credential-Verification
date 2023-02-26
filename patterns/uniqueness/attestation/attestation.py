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

    attr = int.to_bytes(1337, 64, "big") # attr id
    vc_value = int.to_bytes(19810902, 64, "big")

    #print(sys.argv[0])

    dapp_id = int.to_bytes(int(sys.argv[1]), 64, "big")

    resultHash = hashlib.sha256(b"".join([attr[-32:], vc_value[-32:]])).digest()
    resultHash += resultHash

    sig = signKey.sign(resultHash)
            
    #Create Public Key
    verifyKey = PublicKey.from_private(signKey)

    outputs = [
        " ".join([str(i) for i in struct.unpack(">16I", dapp_id)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", attr)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", vc_value)][-8:]),        #"19890519",
        write_signature_for_zokrates_cli(verifyKey, sig, resultHash),
        # " ".join([str(i) for i in (sig[0].x, sig[0].y, sig[1], verifyKey.p.x.n, verifyKey.p.y.n)]),
        # " ".join([str(i) for i in struct.unpack(">16I", resultHash)]),
    ]
    sys.stdout.write(" ".join(outputs))

