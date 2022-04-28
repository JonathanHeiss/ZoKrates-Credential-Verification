#!/bin/bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PATH=$PATH:/Users/$USER/.zokrates/bin

# Attestation

cd $DIR/attestation
python3.9 -m virtualenv venv
source venv/bin/activate

python3.9 zokgen.py > $DIR/artifacts/witness-parameters.txt

# Proving

cd $DIR/proving
zokrates compile -i verify_equality.zok -o $DIR/artifacts/out

START=`date +%s`
cat ../artifacts/witness-parameters.txt | xargs zokrates compute-witness -i $DIR/artifacts/out -o $DIR/artifacts/witness -a 
END=`date +%s`
witnessDur=$(echo "$END - $START" | bc)

mv abi.json $DIR/artifacts/

# Zokrates setup
START=`date +%s`
zokrates setup -i $DIR/artifacts/out -p $DIR/artifacts/proving.key -v $DIR/artifacts/verification.key
END=`date +%s`
setupDur=$(echo "$END - $START" | bc)

# Verification
zokrates export-verifier -i $DIR/artifacts/verification.key -o $DIR/verification/contracts/Verifier.sol

START=`date +%s`
zokrates generate-proof -i $DIR/artifacts/out -j $DIR/artifacts/proof.json -p $DIR/artifacts/proving.key -w $DIR/artifacts/witness
END=`date +%s`
proofDur=$(echo "$END - $START" | bc)

# Test
cd $DIR/verification
truffle test

# Statistics
echo "Witness: $witnessDur sec."
echo "Setup: $setupDur sec."
echo "Proof: $proofDur sec."