#!/bin/bash

set -x

URL="https://hypebeastbaltics.com/products.json"
PER_PAGE=250
PAGE=1

echo "id,title,body_html,vendor,product_type,price,handle" > hbb.csv

while true ; do
    JSON_STR=$(curl "$URL?page=$PAGE&limit=$PER_PAGE")
    echo "$JSON_STR" | jq -r '.products[] | [.id, .title, .body_html, .vendor, .product_type, .variants[0].price, .handle] | @csv' >> hbb.csv
    N_PRODUCTS=$(echo "$JSON_STR" | jq -r '.products | length')
    if [[ "$N_PRODUCTS" -lt "$PER_PAGE" ]]; then
        break
    fi
    PAGE=$((PAGE+1))
done
