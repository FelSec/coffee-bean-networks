#!/bin/bash
set -e

/opt/couchbase/bin/couchbase-server --start

echo 'Waiting 90 seconds for the couchbase server to start'
sleep 90

if ! [ -f /CBN/configured ]; then
  echo "First run - configuring couchbase DB (This may take some time)..."
  sleep 10
  /bin/bash -c /CBN/cbn-db-init.sh
fi
sleep 10
/bin/bash -c /CBN/cbn-db-loaddata.sh

echo 'Starting Coffee Bean Networks...'
# nohup may be preferred
nohup python /CBN/noteapi.py &
python /CBN/cbn.py
