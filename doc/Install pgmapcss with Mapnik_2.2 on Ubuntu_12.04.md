Installation on a plain Ubuntu 12.04.3 Server:

Install additional packages:
```sh
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:mapnik/v2.2.0
sudo add-apt-repository ppa:kakrueger/openstreetmap
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib postgresql-9.1-postgis python-mapnik git osm2pgsql python3 python3-setuptools python3-postgresql python3-dev postgresql-plpython3
```

More dependencies:
* pghstore

```sh
git clone https://github.com/plepe/pghstore.git
cd pghstore
python3 setup.py build
sudo python3 setup.py install
```

Create database:
```sh
sudo su - postgres
createdb test
createuser -P user
# you may say 'y' for superuser
exit
```
Initialize database:
```sh
psql -d "dbname=test user=user host=localhost password=PASSWORD" -c "create extension hstore"
psql -d "dbname=test user=user host=localhost password=PASSWORD" -c "create language plpython3u"
psql -d "dbname=test user=user host=localhost password=PASSWORD" -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d "dbname=test user=user host=localhost password=PASSWORD" -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
```

Download an OSM file and import to database:
```sh
osm2pgsql -dtest -Uuser -Hlocalhost -W -s -S /usr/share/osm2pgsql/default.style --hstore --hstore-all -G azores-latest.osm.bz2
```

Clone pgmapcss:
```sh
git clone https://github.com/plepe/pgmapcss.git
cd pgmapcss
python3 setup.py build
sudo python3 setup.py install
```

Compile 'test.mapcss' file and install database functions:
```
pgmapcss -dtest -uuser -pPASSWORD -tmapnik-2.0 test
```

You have a file test.mapnik which you can use in your preferred render front-end (e.g. renderd/mod_tile) OR generate an image with generate_image.py (if the Azores where not used as data, change "bounds" in file accordingly):
```sh
./generate_image.py
```
