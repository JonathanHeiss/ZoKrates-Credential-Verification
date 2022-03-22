# Issuer

## Setup and Run

Using a virtualenv if desired:

```
python -m virtualenv venv
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
          "x": "15609712557955536826919289374624438250046156618562260572300602114561212647167",
          "y": "12509997264749219735980507851583887000555595391604772985283814653021702360102"
        },
        "s": 1.8165960877362573e+76
      },
      "value": "Watson"
    },
    {
      "name": "last_name",
      "signature": {
        "r": {
          "x": "8222203677367940022495967623012889482247688178842779025624735800262613517662",
          "y": "10258647233191611314007033578581878104877087621566394366545921463835689778903"
        },
        "s": 7.895661499864834e+75
      },
      "value": "Evita"
    },
    {
      "name": "age",
      "signature": {
        "r": {
          "x": "20532102700700437045454107211456705406790581748281556146909771417975653729529",
          "y": "1236663826911501295993096964670549175472003145712122490066586530912530551871"
        },
        "s": 2.0437644036899075e+76
      },
      "value": "40"
    }
  ]
}
```
