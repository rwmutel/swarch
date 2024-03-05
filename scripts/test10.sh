#!/bin/bash

for i in {1..10}; do
    url="http://127.0.0.1:8000/msg$i"
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$url")
    echo "Response code for $url: $response"
done

