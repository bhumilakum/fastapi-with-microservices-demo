# Generic single-database configuration

## Create a Migration Script
```
alembic revision -m "message" --autogenerate
```

## Run Latest Migration
```
alembic upgrade head
```

## Get Current Revision Information
```
alembic current
```

## Get History
```
alembic history --verbose
```
