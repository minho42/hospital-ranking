# hospital-ranking

[https://hospitals-aus.netlify.app/](https://hospitals-aus.netlify.app/)

Scrapes Google ratings information (stars and review count) for Australian hospitals without using Google Maps API

## Requirement

- Python 3
- Google Chrome
- Chromedriver

## Raw data

`all_hospitals.xlsx`

from [https://www1.health.gov.au/internet/main/publishing.nsf/Content/hospitals2.htm](https://www1.health.gov.au/internet/main/publishing.nsf/Content/hospitals2.htm)

## Input

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

## Output

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

`ranking.json`

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


Download raw data from the link above.
Change filename to `all_hospitals.xlsx`

```
$ python
>>> from app import prep_get_hospitals
>>> prep_get_hospitals()
```

Run the script (this takes a long time)
```
$ python app.py
```
