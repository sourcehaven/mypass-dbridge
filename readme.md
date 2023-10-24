# MyPass DBridge project

Module should reside on the backend machine.
Its responsibility is to act as a bridge between the device and the database.

Tasks this api should handle
 - Authentication of users against db.
 - Accepting and providing JWTs.
 - Communication with the database.

Note that this app should not handle any sensitive information,
encryption and such should happen on the user's device.

## PostgreSQL database initialization

> psql -U postgres

We will create a user for our db in the next section.

postgres-#

> **CREATE USER** mypass **WITH PASSWORD** '${your password goes here}';\
> **ALTER ROLE** mypass **SET** client_encoding **TO** 'utf8';\
> **ALTER ROLE** mypass **SET** default_transaction_isolation **TO** 'read committed';\
> **ALTER ROLE** mypass **SET** timezone **TO** 'UTC';\


Next, execute the following db creation script:

```sql
CREATE DATABASE mypass
    WITH
    OWNER = mypass
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT ALL ON DATABASE mypass TO mypass;
```

## MySQL and MariaDB initialization

```sql
-- Create a user with a password
CREATE USER 'mypass'@'localhost' IDENTIFIED BY '${your password goes here}';

-- Set user options
SET GLOBAL character_set_client = 'utf8';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
SET GLOBAL time_zone = '+00:00';

-- Create a database
CREATE DATABASE mypass CHARACTER SET utf8 COLLATE utf8_general_ci;

-- Grant privileges on the database to the user
GRANT ALL PRIVILEGES ON mypass.* TO 'mypass'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
```

### Migrations

!!! TODO !!!

## Environment setup

Database connection string should be configured using the environment variable `MYPASS_DB_CONNECTION_URI`.
Should be set to something like: `{protocol}://{dbuser}:{dbpass}@{host}:{port}/{dbname}`, eg.:
`postgresql+psycopg2://mypass:MyPassWord@localhost:5432/mypass`

### Basic test env configuration

`FLASK_ENV=Development;MYPASS_DB_CONNECTION_URI=sqlite+pysqlite:///:memory:;MYPASS_TESTENV=1`

### Setup in PostgreSQL
`postgresql+psycopg2://mypass:MyPassWord@localhost:5432/mypass`

### Setup in MySQL and MariaDB
`mysql://mypass:MyPassWord@localhost:3306/mypass`

### Setup in SQLite

`sqlite:///:memory:`
`sqlite:///path/db/data.db`
`sqlite+pysqlite:///:memory:`

## Development

Run code style guide:

> flake8 mprest

### Cleanup

To clean local binaries, run:

> pyclean -v .

or clean only the package:

> pyclean -v mprest
