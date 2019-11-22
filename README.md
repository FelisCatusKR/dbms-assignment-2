# dbms-assignment-2

A DBMS-based contact webapp using FastAPI

## How to deploy

```
$ sudo docker swarm init
$ echo "YOUR_DESIRED_PSQL_PASSWORD" | sudo docker secret create psql-pw -
$ sudo docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
