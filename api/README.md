# API Service

## Local Setup

```
git clone git@github.com:DRP-4/DRP-4.git
cd DRP-4/
npm install
npm run dev
```

This runs the frontend with Hot Reload. Then in another tab, run.

```
cd DRP-4/api/
virtualenv venv
pip install -r requirements.txt
export DATABASE_URL="sqlite:///project.db"
python3 ./create_db.py
flask run --debug
```

This also has HRM

## Prod DB Migration

Setup `.env`

```
export DATABASE_URL=postgres://.....
```

Where the URL comes from "Settings" > "View Credentials" on heroku

```
source .env
python3 ./create_db.py
```

This may change if we need to do more complex migrations. It's probably easier to just to drop the tables.

You can do this with `psql $DATABASE_URL`, but don't do this on lab machines, as it'll leak the password :)