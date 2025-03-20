# FastAPI + HTMX + Firebase auth (+ Docker + uv + direnv)

### Local without docker:

install uv

install direnv:

https://github.com/direnv/direnv/blob/master/docs/installation.md

add direnv hook:

https://github.com/direnv/direnv/blob/master/docs/hook.md

uvicorn api.main:app --host 0.0.0.0 --port 1234 --workers 1

### Local with docker

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


### Viewing HTMX Todo list:

http://127.0.0.1:1234/htmx/todo_index


### Testing Firebase

1. Create a user in your Firebase Auth App

2. Generate a TokenID
```
POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=[WEBAPIKEY]
{
	"email": "email@gmail.com",
	"password":"password",
	"returnSecureToken":true
}
```

3. Send a request to the FastAPI protected endpoint
```
GET http://127.0.0.1:1234/firebase/firebase_user
Authorization: TokenID
```
