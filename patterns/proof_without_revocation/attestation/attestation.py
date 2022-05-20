import hashlib
from zokrates_pycrypto.eddsa import PrivateKey, PublicKey
from zokrates_pycrypto.field import FQ
from zokrates_pycrypto.utils import write_signature_for_zokrates_cli
from eth_abi import encode_single
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

    attr1 = int.to_bytes(13, 64, "big") # Attr for prename
    vc_prename = encode_single("string", "Paul")

    threshold = 20030101
    vc_dob = int.to_bytes(19990101, 64, "big") # Attr for dateofbirth
    attr2 = int.to_bytes(24, 64, "big") # Attr for dateofbirth


    resultHash1 = hashlib.sha256(b"".join([attr1[-32:], vc_prename[32:]])).digest()
    resultHash1 += resultHash1

    resultHash2 = hashlib.sha256(b"".join([attr2[-32:], vc_dob[-32:]])).digest()
    resultHash2 += resultHash2

    sig1 = signKey.sign(resultHash1)
    sig2 = signKey.sign(resultHash2)
            
    #Create Public Key
    verifyKey = PublicKey.from_private(signKey)

    outputs = [
        " ".join([str(i) for i in struct.unpack(">16I", attr1)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", vc_prename)][-8:]),
        write_signature_for_zokrates_cli(verifyKey, sig1, resultHash1),
        " ".join([str(i) for i in struct.unpack(">16I", attr2)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", vc_dob)][-8:]),
        str(threshold),
        write_signature_for_zokrates_cli(verifyKey, sig2, resultHash2),
    ]
    sys.stdout.write(" ".join(outputs))

