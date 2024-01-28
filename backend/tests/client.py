from fastapi.testclient import TestClient

from app.main import app 

# TODO follow this guide for testing: 
# 1) https://dev.to/jbrocher/fastapi-testing-a-database-5ao5
# 2) https://www.jeffastor.com/blog/testing-fastapi-endpoints-with-docker-and-pytest/

client = TestClient(app=app)

