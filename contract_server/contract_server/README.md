# Contract Server
## In Development Stage
### Add Oracle Server into DB

		$ python manage.py shell
		>>> from oracles.model import Oracle
		>>> oracle = Oracle(name="test server", url="http://localhost:8080")
		>>> oracle.save()
		>>> exit()

and to check the result

		$ python manage.py runserver
		
		// open another terminal
		$ curl localhost:8000/oracles/
		
you'll get the result