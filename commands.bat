@echo off
:: GET запросы через порт 8000
curl -X GET "http://localhost:8000/api/reports/formats" -H "accept: application/json"
pause

curl -X GET "http://localhost:8000/api/reports/ranges/JSON" -H "accept: application/json"
pause

curl -X GET "http://localhost:8000/api/dateblock" -H "accept: application/json"
pause



:: POST запросы через порт 8001
curl -X POST "http://localhost:8001/api/filter/groups" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Заморозка\", \"id\": \"\", \"type\": 1}"
pause

curl -X POST "http://localhost:8001/api/transactions" -H "accept: application/json" -d ""
pause

curl -X POST "http://localhost:8001/api/turnover" -H "accept: application/json" -d ""
pause