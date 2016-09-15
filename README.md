# deploy_django.dev

Deploy Django and Postgresql with Docker in two commands in project dir.

	clone <URL> .
	fab deploy_dev

Start Docker containers with:
	
	fab up
	
Then visit localhost:8000

---

Dependencies:
- docker-compose v2
- virtualenvwrapper
- Fabric3

