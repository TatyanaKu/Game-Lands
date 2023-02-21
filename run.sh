echo $PWD
export POSTGRES_VOLUME_PATH=$PWD/deploy/postgresql/data
export MONGO_INIT_PATH=$PWD/deploy/mongo/init-mongo.js
export MONGO_VOLUME_PATH=$PWD/deploy/mongo/data
docker compose -f deploy/docker-compose.yml up