#!/bin/bash

# URLs to be sent
urls=(
    "https://doi.org/10.1056/NEJMoa2312695"
    "https://doi.org/10.1056/NEJMoa1910549"
    "https://doi.org/10.1056/NEJMoa2302983"
    "10.1056/NEJMoa1802357"
    "10.1016/j.ejca.2022.05.007"
    "10.1016/j.annonc.2022.05.519"
    "10.1016/j.ejca.2022.03.040"
    "10.1016/S2468-1253(21)00382"
    "10.1016/S1470-2045(21)00064-4"
    "10.1001/jamaoncol.2018.0013"
)

# Endpoint URL
base_endpoint="https://abstructs.fly.dev/structured-response/json"

# Loop through each URL and send it to the endpoint
for url in "${urls[@]}"; do
    endpoint="$base_endpoint?url=$url"
    curl -X POST $endpoint
    echo "Sent $url"
done
