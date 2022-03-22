# zok-pdapps

## Rob

### Zokrates Notes
Install see [here](https://zokrates.github.io/gettingstarted.html) and ```export PATH=$PATH:/Users/rob/.zokrates/bin```

```
zokrates compute-witness -a 315555217 1079953207
zokrates setup
zokrates export-verifier
zokrates generate-proof
```

### Truffle Notes
Execute ```node migrations/init.js``` for copying the Zokrates programs to separeted Solidity contracts.
Install [Zokrates-JS](https://zokrates.github.io/toolbox/zokrates_js.html).
Run ```truffle test```
