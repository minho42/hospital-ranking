# Australian hospital ranking

Scrape Google ratings information (stars and review count) without using Google Maps API

## Requirement

- Python 3
- Google Chrome
- Chromedriver

## Raw data

`all hospitals.xlsx`

from [https://www1.health.gov.au/internet/main/publishing.nsf/Content/hospitals2.htm](https://www1.health.gov.au/internet/main/publishing.nsf/Content/hospitals2.htm)

## Input

`all hospitals.json`

```json
[
  {
    "sector": "PUBLIC",
    "state": "NSW",
    "name": "CONCORD REPATRIATION HOSPITAL"
  }
]
```

## Output

`ranking.json`

```json
[
  {
    "sector": "PUBLIC",
    "state": "NSW",
    "name": "CONCORD REPATRIATION HOSPITAL",
    "stars": "2.9",
    "reviews": "288"
  }
]
```

## Usage

Copy the source code

```shell
$ git clone https://github.com/minho42/hospital-ranking.git
$ cd hospital-ranking/
```

Optional: Use virtual environment

```shell
$ python -m venv venv
$ source venv/bin/activate
```

Install required packages

```shell
$ pip install -r requirements.txt
```

[Download](https://chromedriver.chromium.org/downloads) Chromedriver

Change variables in `app.py`
e.g. CHROME_DRIVER_PATH

Run the script (this takes a long time)

```
$ python app.py
```
