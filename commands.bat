@echo off
curl -X GET ^
  "http://172.18.8.182:8080/api/reports/formats" ^
  -H "accept: application/json"
pause

@echo off
curl -X 'GET' \
  'http://localhost:8080/api/reports/ranges/JSON' \
  -H 'accept: application/json'
pause

@echo off
curl -X 'GET' \
  'http://localhost:8080/api/dateblock' \
  -H 'accept: application/json'
pause





@echo off
curl -X 'POST' \
  'http://localhost:8080/api/filter/groups' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Заморозка",
  "id": "",
  "type": 1
}'
pause

@echo off
curl -X 'POST' \
  'http://localhost:8080/api/transactions' \
  -H 'accept: application/json' \
  -d ''
pause

@echo off
curl -X 'POST' \
  'http://localhost:8080/api/turnover' \
  -H 'accept: application/json' \
  -d ''
pause