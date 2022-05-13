#!/bin/bash

ALL_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

declare -a proofs=("equality" "range" "uniqueness" "min-age" "merkle")

mkdir $ALL_DIR/eval 2> /dev/null
ALL_EVALS="$ALL_DIR/eval/all.txt"

if [ ! -f "$ALL_EVALS" ] 
then
	echo "proof,timestamp,gas_call,witness_s,setup_s,proof_s,compiled_size,proving_key_size,verification_key_size" > $ALL_EVALS
fi

for proof in "${proofs[@]}"
do
	cd $ALL_DIR/$proof
	echo "Eval: $proof"
	$ALL_DIR/$proof/eval.sh > $ALL_DIR/eval/$proof.txt

	cd $ALL_DIR/eval
	gas_call=$(cat $ALL_DIR/eval/$proof.txt | grep "Gas used: " | sed "s/^.*[^0-9] //")
	witness_s=$(cat $ALL_DIR/eval/$proof.txt | grep "Witness: " | sed "s/^.*[^0-9] //")
	setup_s=$(cat $ALL_DIR/eval/$proof.txt | grep "Setup: " | sed "s/^.*[^0-9] //")
	proof_s=$(cat $ALL_DIR/eval/$proof.txt | grep "Proof: " | sed "s/^.*[^0-9] //")
	compiled_size=$(cat $ALL_DIR/eval/$proof.txt | grep "Compiled size: " | sed "s/^.*[^0-9] //")
	proving_key_size=$(cat $ALL_DIR/eval/$proof.txt | grep "Proving key size: " | sed "s/^.*[^0-9] //")
	verification_key_size=$(cat $ALL_DIR/eval/$proof.txt | grep "Verification key size: " | sed "s/^.*[^0-9] //")

	row="$proof,$(date +%s),$gas_call,$witness_s,$setup_s,$proof_s,$compiled_size,$proving_key_size,$verification_key_size"

	echo $row >> $ALL_EVALS
	
	echo $row
done