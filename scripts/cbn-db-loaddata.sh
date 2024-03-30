#!/bin/bash

CLUSTER='localhost'
CUSER='CBN-Admin'
CPASS='7T7YqQ9%DtZ!Sb'

echo '[?] Loading / Refreshing Data in DB'
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b blog_posts -d file:///CBN/data/blog_posts.json -f lines -g %id%
sleep 1
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b borkborkbork -d file:///CBN/data/borkborkbork.json -f lines -g key::%name%::#UUID#
sleep 1
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b flag_two -d file:///CBN/data/flag_two.json -f lines -g key::%name%::#UUID#
sleep 1
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b languages -d file:///CBN/data/languages.json -f lines -g key::%lang%::#UUID#
sleep 1
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b pending_posts -d file:///CBN/data/pending_posts.json -f lines -g %id%
sleep 1
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b products -d file:///CBN/data/products.json -f lines -g %id%
sleep 1
/opt/couchbase/bin/cbimport json -c $CLUSTER -u $CUSER -p $CPASS -b status -d file:///CBN/data/status.json -f lines -g key::%component%::#UUID#
echo '[?] Complete!'