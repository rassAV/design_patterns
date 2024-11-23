@echo off
curl -X GET ^
  "http://172.18.8.182:8080/api/reports/formats" ^
  -H "accept: application/json"
pause