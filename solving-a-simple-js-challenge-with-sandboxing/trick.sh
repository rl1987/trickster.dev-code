#!/bin/bash

set -x

curl "https://opencorporates.com" | \
    xmllint --html --xpath '//script/text()' - | \
    tail +2 > in.js # Deleting "<![CDATA[<!--" line

curl "https://opencorporates.com" -H "cookie: $(node sandbox.js)"

