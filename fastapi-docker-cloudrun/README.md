FastAPI + Docker + uv + direnv + Cloud Run
==========================================

Local without docker:
=====================

install uv

install direnv:

https://github.com/direnv/direnv/blob/master/docs/installation.md

add direnv hook:

https://github.com/direnv/direnv/blob/master/docs/hook.md

uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 1

Local with docker
===================

Copy .env.template, and update PROJECT_ID and APP accordingly.

Then, after ensuring direnv has updated to the latest env vars:

docker build -t $TAG .
docker run --rm -dp 5000:5000 $TAG

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

or to make it publically accessible:

``
gcloud run deploy $APP --image $TAG --platform managed --region $REGION  --allow-unauthenticated
```

