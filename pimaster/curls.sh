curl -i http://localhost:5000/tlaloc/api/v1.0/modules

curl -i http://localhost:5000/tlaloc/api/v1.0/modules/1

curl -i -H "Content-Type: application/json" -X POST -d '{"id":3,"name":"basilic","seconds":6}' http://localhost:5000/tlaloc/api/v1.0/modules

curl -i http://localhost:5000/tlaloc/api/v1.0/modules

curl -i -H "Content-Type: application/json" -X PUT -d '{"id":3,"name":"basilic","seconds":7}' http://localhost:5000/tlaloc/api/v1.0/modules/3

curl -i http://localhost:5000/tlaloc/api/v1.0/modules

curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/tlaloc/api/v1.0/modules/3

curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/tlaloc/api/v1.0/modules/3
