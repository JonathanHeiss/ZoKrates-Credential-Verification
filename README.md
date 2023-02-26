# Verifiable Carbon Accounting: ZoKrates-based Evaluation

### Zokrates
Install see [here](https://zokrates.github.io/gettingstarted.html) and ```export PATH=$PATH:/Users/$USER/.zokrates/bin```

```
zokrates compile -i minAge.zok
zokrates compute-witness -a 315555217 1079953207
zokrates setup
zokrates export-verifier
zokrates generate-proof
```

## Setup and Run

Using a virtualenv if desired:

```
python3.9 -m virtualenv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

To run the test cases execute script ./test_cases/eval_all.sh.
For each test case it executes the stages: attestation, proving, and verification. 
Measurements are collected in ./eval/all.txt.
