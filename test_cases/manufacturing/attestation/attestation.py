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
    #Manufacturing Signature
    signKey = PrivateKey.from_rand()
    verifyKey = PublicKey.from_private(signKey)

    attr = int.to_bytes(0, 64, "big") #  pholder
    vc_value = int.to_bytes(120, 64, "big") #activity data: distance per ride

    resultHash = hashlib.sha256(b"".join([attr[-32:], vc_value[-32:]])).digest()
    resultHash += resultHash

    sig = signKey.sign(resultHash)
            
    #Manufacturing Certificate
    certSecKey = PrivateKey.from_rand()
    certPubKey = PublicKey.from_private(certSecKey)

    attrC = int.to_bytes(0, 64, "big") #  pholder
    cert = int.to_bytes(120, 64, "big") #verifyKey:public key device 
    #int((certPubKey.p.x.n), int(certPubKey.p.y.n))

    resultHash_2 = hashlib.sha256(b"".join([attrC[-32:], cert[-32:]])).digest()
    resultHash_2 += resultHash_2

    sigCert = certSecKey.sign(resultHash_2)

    outputs = [
        #Manufacturing
        "40", #EF_elec
        "5", #AF_elec
        " ".join([str(i) for i in struct.unpack(">16I", attr)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", vc_value)][-8:]),
        write_signature_for_zokrates_cli(verifyKey, sig, resultHash),

        " ".join([str(i) for i in struct.unpack(">16I", attrC)][-8:]),
        " ".join([str(i) for i in struct.unpack(">16I", cert)][-8:]),
        write_signature_for_zokrates_cli(certPubKey, sigCert, resultHash_2),

    ]
    
    sys.stdout.write(" ".join(outputs))

