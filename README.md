# Customer-Reviews-of-Bank-Agencies-in-Morocco
## a fully operational ETL pipeline to automate the process of extracting customer reviews from Google Maps and Visualize insights


1. run src/data_collection/main.py to collect data from google maps api , data will be in data/raw
2. go to database folder using `cd database` and run `docker compose --env-file ../.env up -d` to create tow db
3. to connect to db using terminal use `psql -h localhost -p 5433 -U user -d database_POSTGRES_DB_1` or `psql -h localhost -p 5434 -U user -d database_POSTGRES_DB_2` change user with user in .env and will demande password use password in .env
4. you can use `docker compose down` or for delete volume use `docker compose down -v`
5. or use databse/test to testing db

