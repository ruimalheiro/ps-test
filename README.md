# Ps-test

## Dependencies
- Install Docker and Docker Compose

## Instructions after cloning the repository
- `docker-compose build`
- `docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate && python manage.py seed_transactions"`
    
Note - `seed_transactions` will take ± 1.5 minutes.

- `docker-compose up`

The API should be accessible through `localhost:8000`

    
## Tests    
- `dock-compose run --rm app sh -c "python manage.py test && flake8"`

## API
### GET:
- `/api/transaction/list/`
- `/api/transaction/list/<transaction uuid>`
- `/api/transaction/breakdown/<account uuid>`
- `/api/transaction/breakdown/<account uuid>?start_date=<date>&end_date=<date>`
### POST:
- `/api/transaction/create`
### DELETE:
- `/api/transaction/list/<transaction uuid>`