FastAPI + Docker + uv + direnv + Cloud Run
==========================================

Local without docker:
=====================

install uv

install direnv:

https://github.com/direnv/direnv/blob/master/docs/installation.md

add direnv hook:

https://github.com/direnv/direnv/blob/master/docs/hook.md

uvicorn server:app --host 0.0.0.0 --port 1234 --workers 1 --app-dir src

Local with docker
===================

Create .env, and add:

PROJECT_ID=<YOUR_UNIQUE_LOWER_CASE_PROJECT_ID>
APP=<app name>
PORT=1234
TAG="gcr.io/$PROJECT_ID/$APP"
REGION="europe-west1"

Then:

```
export TAG="gcr.io/$PROJECT_ID/$APP"
```

docker build -t $TAG .
docker run --rm -dp $PORT:$PORT -e PORT=$PORT $TAG

Cloud run:
==========

Set up project, billing project etc (some hints at https://github.com/sekR4/FastAPI-on-Google-Cloud-Run)

To build

```
gcloud builds submit --tag $TAG
```

To deploy:

``
gcloud run deploy $APP --image $TAG --platform managed --region $REGION
```
