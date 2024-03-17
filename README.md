# ff-dashboard


## Install notes

### Backend

```
cd backend && pip install -r requirements.txt --use-pep517
```


If you're running on a mac and are using `Postgres.app`, you need to install `psycopg2-binary` by handing it the binary that `Postgres.app` comes with with the following command:

```
PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH" pip install --force-reinstall psycopg2-binary
```
