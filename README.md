# lrucache_api

Simple LRU Cache backed by a Flask server and deployed with Docker.

## Setup
`docker build --tag=lrucache_api .`

## Running
`docker run -p 4000:80 lrucache_api`

### GET
Either curl `curl XGET ​http://localhost:4000/api/v1/get/{key}` or navigate to `​http://localhost:4000/api/v1/get/{key}`

### PUT
Either `curl XPUT ​http://localhost:4000/api/v1/put/4{key} -d "value={value}"` or navigate to `http://localhost:4000/api/v1/put/{key}?value={value}`
