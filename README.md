# Service Status Thingee

I'm experimenting with FastAPI, and this is the outcome. Terrible, I'm sure.

Let me be clear. This is mostly copy-and-pasted from blogs and YouTube videos. We're all learning together. :)

## What I've Done So Far

I created a FastAPI-based application that gets the status of my ADSB receivers and my blogs. The app is written in Python since that's the only thing I know. LOL

I split the two functions -- ADSB and blogs -- in two different APIRouters for management and ease-of-use.

I added a `Dockerfile` to use the application as a Docker container.

I added a `docker-compose.yml` file to create the app container as well as a Postgres DB to query for stuff. The DB server has a persistent data mount so the same data is available between restarts. The containers also run in a custom Docker network just so I have some practice with that.

Nothing about any of this is secure, but it's fun.