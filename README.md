# hospital-ranking

[https://hospital-ranking.netlify.app](https://hospital-ranking.netlify.app)

Scrapes Google ratings information (stars and review count) for Australian hospitals without using Google Maps API

----

## Requirement

- Python 3
- Google Chrome
- Chromedriver


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

Change variable `CHROME_DRIVER_PATH` in `app.py`


[Download](https://www1.health.gov.au/internet/main/publishing.nsf/Content/hospitals2.htm) raw data


Change filename to `all_hospitals.xlsx`

Run the script (this takes a long time)
```
$ python app.py
```

----

## Variables in app.py
### RAW_DATA_FILE

`all_hospitals.xlsx`

### EXTRACTED_DATA_FILE

`all_hospitals.json`

```json
[
  {
    "sector": "PUBLIC",
    "state": "NSW",
    "name": "CONCORD REPATRIATION HOSPITAL"
  }
]
```

## RATING_FILE

`rating.json`

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

### RANKING_FILE

`frontend/ranking.json`

```json
[
  {
    "sector": "PUBLIC",
    "state": "NSW",
    "name": "CONCORD REPATRIATION HOSPITAL",
    "stars": "2.9",
    "reviews": "288",
    "ranking": "2.9022899952150216"
  }
]
```

