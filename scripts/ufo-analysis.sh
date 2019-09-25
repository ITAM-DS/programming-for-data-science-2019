#! /bin/bash

BASE_URL="http://www.nuforc.org/webreports/ndxe"

function extract_table() {
    sed -n '/<TABLE .*>/,/<\/TABLE>/p' $1  | sed  's/<[^>]*>\n//g'
}


function load_data() {
    for url in "${BASE_URL}"{1960..2019}{01..12}".html"
    do
        echo ${url}
        curl -k ${url} | extract_table
    done
}
