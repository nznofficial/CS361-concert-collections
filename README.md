# Concert Collections

Remember Where You Made Your Musical Memories

A Flask web app for tracking your favorite artists, logging concerts you have
attended, and planning concerts you want to see. Artist details and concert
plans are provided by five independent microservices.

## Features

- Add favorite artists and view their biography and top songs
- Log past concerts with artist, city, and date
- Plan upcoming concerts and see the weather forecast for each one in Deg F or Deg C

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key_here
```

## Run

```bash
python app.py
```

The app runs at `http://127.0.0.1:5000`.

## Microservices

The Main Program calls four microservices over HTTP. Each runs as a separate
process and must be started before use. 

| Port | Service | Used by |
|------|---------|---------|
| 8002 | Weather Forecast | Planned concerts |
| 8003 | Task | Planned concerts |
| 8004 | Top Songs | Artist detail |
| 8005 | Artist Biography | Artist detail |
| 8006 | Unit Conversion | Planned concerts |

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home |
| `/artists` | Favorite artists |
| `/artists/add` | Add an artist |
| `/artists/<id>` | Artist detail with biography and top songs |
| `/concerts` | Logged concerts |
| `/concerts/add` | Log a concert |
| `/plans` | Planned concerts with weather forecast |
| `/plan_concert` | Plan a concert |