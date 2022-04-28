# zok-pdapps

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

Run:

```
cd app
flask run
```

By default the application uses `data/credentials.json` as the credentials db.
Override by setting `CREDENTIALS_DB` env variable to a desired path.

## End points

```
/vc/<id:int>
```

Returns VC based on the credential at index `id` in the credentials db.
Example response:

```json
{
  "vc": [
    {
      "name": "first_name",
      "signature": {
        "r": {
          "x": "16186741509368722243096758946239189910015670459397802427521670489156754200016",
          "y": "3351638091635298599205912516976706381137677095846652856179006461604404983176"
        },
        "s": "15563119992355797653607862848468794678925511172655648433603249827995731876428"
      },
      "value": "Watson"
    },
    {
      "name": "last_name",
      "signature": {
        "r": {
          "x": "6446853697758819516394107443625644251738227832769656237379623305689138379563",
          "y": "1488152011954199231821001088562661880442303912737469165427297265127394908344"
        },
        "s": "10054924674489381086075379083441696909505817741144174735178894587728377757855"
      },
      "value": "Evita"
    },
    {
      "name": "date_of_birth",
      "signature": {
        "r": {
          "x": "19988854867353371685744940471375959479117379991763866059332804422731070017082",
          "y": "18086400849902694229265887147098563246524423448211070365836254575267975926433"
        },
        "s": "16763594360016908614547304515050641435625366696519137579085658563374197263809"
      },
      "value": "19400101"
    }
  ]
}
```


### Zokrates
Install see [here](https://zokrates.github.io/gettingstarted.html) and ```export PATH=$PATH:/Users/$USER/.zokrates/bin```

```
zokrates compile -i minAge.zok
zokrates compute-witness -a 315555217 1079953207
zokrates setup
zokrates export-verifier
zokrates generate-proof
```
