# Set up
Here's a convenient setup script:
- run `chmod +x setup.sh`
- run `./setup.sh`
  
If for some reason something went wrong (maybe you're using Linux distro with weird dependencies or not using Linux at all) run the following or your system's equivalent:
- `docker-compose up --build`
- `docker-compose exec web python manage.py makemigrations`
- `docker-compose exec web python manage.py migrate`

# Some details
As per the request, everything is running inside a docker container. PostgreSQL is set up at port 5432, Django opens up at 8000.
You can generate an instance of Wallet at `http://localhost:8000/api/v1/walletgen/`. Django is set up so that you can send only GET to `http://localhost:8000/api/v1/wallets/{WALLET_UUID}/`, wasn't really sure whether it's a strict requiremnt, though. At `http://localhost:8000/api/v1/wallets/{WALLET_UUID}/operations/` you can send POST requests. The views are set up with Django REST Framework, therefore you can just open up the URLs in the browser. However, if you want to CURL you still can.
Finally, automatic testing should've been performed when you ran `./setup.sh`, but if you haven't done it you can run the tests with this `docker-compose exec web python manage.py test`
