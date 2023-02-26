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

def write_hash_for_zokrates_cli(msg):
    M0 = msg.hex()[:64]
    M1 = msg.hex()[64:]
    b0 = [str(int(M0[i:i+8], 16)) for i in range(0,len(M0), 8)]
    b1 = [str(int(M1[i:i+8], 16)) for i in range(0,len(M1), 8)]
    args = " ".join(b0 + b1)
    return args

if __name__ == "__main__":
    #Upstream PCF 1
    upPCF_holer1 = int.to_bytes(0, 64, "big") #  pholder
    upPCF1 = int.to_bytes(120, 64, "big") # upstream PCF 1

    resultHash_5 = hashlib.sha256(b"".join([upPCF_holer1[-32:], upPCF1[-32:]])).digest()
    resultHash_5 += resultHash_5


    #Upstream PCF 2
    upPCF_holer2 = int.to_bytes(0, 64, "big") #  pholder 2
    upPCF2 = int.to_bytes(120, 64, "big") # upstream PCF 2

    resultHash_6 = hashlib.sha256(b"".join([upPCF_holer2[-32:], upPCF2[-32:]])).digest()
    resultHash_6 += resultHash_6

    #Upstream PCF 3
    upPCF_holer3 = int.to_bytes(0, 64, "big") #  pholder 3
    upPCF3 = int.to_bytes(120, 64, "big") # upstream PCF 3

    resultHash_7 = hashlib.sha256(b"".join([upPCF_holer3[-32:], upPCF3[-32:]])).digest()
    resultHash_7 += resultHash_7

    outputs = [
        #Upstream PCF 1
        " ".join([str(i) for i in struct.unpack(">16I", upPCF_holer1)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", upPCF1)][-8:]),
        write_hash_for_zokrates_cli(resultHash_5),

        #Upstream PCF 2
        " ".join([str(i) for i in struct.unpack(">16I", upPCF_holer2)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", upPCF2)][-8:]),
        write_hash_for_zokrates_cli(resultHash_6),

        #Upstream PCF 3
        " ".join([str(i) for i in struct.unpack(">16I", upPCF_holer3)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", upPCF3)][-8:]),
        write_hash_for_zokrates_cli(resultHash_7)
    ]
    
    sys.stdout.write(" ".join(outputs))

