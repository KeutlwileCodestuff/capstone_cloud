#!/bin/bash


# curl -X GET https://uq6kl9x51a.execute-api.eu-west-1.amazonaws.com/v1/storage/units

curl -X POST https://uq6kl9x51a.execute-api.eu-west-1.amazonaws.com/v1/storage/units/book \
-H "Content-Type: application/json" \
-d '{
  "body": "{\"unit_id\": \"unit123\", \"customer_id\": \"cust456\", \"start_date\": \"2024-12-05\", \"end_date\": \"2024-12-15\", \"payment_method\": \"card\"}"
}'
