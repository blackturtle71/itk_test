#!/bin/sh
docker-compose up -d --build

DB_CONTAINER=$(docker-compose ps -q db)
WEB_CONTAINER=$(docker-compose ps -q web)

# might hang if containers don't start, but I don't know about hardware config and network connectivity, so yeah, that'll do
wait_for_container() {
    local container_name="$1"

    echo "Waiting for $container_name to start..."
    until [ "$(docker inspect -f '{{.State.Running}}' "$container_name")" = "true" ]; do
        sleep 5
    done
}

wait_for_container "$DB_CONTAINER"
wait_for_container "$WEB_CONTAINER"

docker-compose exec web python manage.py makemigrations
sleep 2
docker-compose exec web python manage.py migrate
sleep 2
docker-compose exec web python manage.py test
sleep 2
# for whatever reason you can't connect to the API right after setup, reset helps :)
docker-compose stop
sleep 2
docker-compose up -d
echo "Setup complete. Wallet generator is available at http://localhost:8000/api/v1/walletgen/"
