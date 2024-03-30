#!/bin/bash

# CBN COUCHBASE INIT SCRIPT
CLUSTER='localhost'
CUSER='CBN-Admin'
CPASS='7T7YqQ9%DtZ!Sb'

echo '[!] Task 1 of 6 - Creating couchbase cluster...'
# create cluster
/opt/couchbase/bin/couchbase-cli cluster-init -c $CLUSTER --cluster-username $CUSER --cluster-password $CPASS --cluster-name cbn-db --services data,index,query

# setup buckets
echo '[!] Task 2 of 6 - Creating buckets...'
echo '[!] Task 2a of 6 - Creating blog_posts bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket blog_posts --bucket-type couchbase --bucket-ramsize 200 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2b of 6 - Creating borkborkbork bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket borkborkbork --bucket-type couchbase --bucket-ramsize 100 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2c of 6 - Creating flag_two bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket flag_two --bucket-type couchbase --bucket-ramsize 100 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2d of 6 - Creating languages bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket languages --bucket-type couchbase --bucket-ramsize 200 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2e of 6 - Creating pending_posts bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket pending_posts --bucket-type couchbase --bucket-ramsize 100 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2f of 6 - Creating products bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket products --bucket-type couchbase --bucket-ramsize 300 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2g of 6 - Creating status bucket...'
/opt/couchbase/bin/couchbase-cli bucket-create -c $CLUSTER --username $CUSER --password $CPASS --bucket status --bucket-type couchbase --bucket-ramsize 100 --bucket-replica 1 --enable-flush 1 --wait
sleep 1
echo '[!] Task 2 of 6 - Buckets created.'

# create users
echo '[!] Task 3 of 6 - Setting up users...'
/opt/couchbase/bin/couchbase-cli user-manage -c $CLUSTER --username $CUSER --password $CPASS --rbac-username fletcher_one --rbac-password fletcher_one --set --auth-domain local --roles query_select[blog_posts],query_select[pending_posts],data_reader[blog_posts],data_reader[pending_posts]
/opt/couchbase/bin/couchbase-cli user-manage -c $CLUSTER --username $CUSER --password $CPASS --rbac-username fletcher_two --rbac-password fletcher_two --set --auth-domain local --roles query_select[flag_two],query_select[status],query_update[status],data_reader[flag_two],data_reader[status]
/opt/couchbase/bin/couchbase-cli user-manage -c $CLUSTER --username $CUSER --password $CPASS --rbac-username fletcher_three --rbac-password fletcher_three --set --auth-domain local --roles query_select[languages],query_select[borkborkbork],data_reader[languages],data_reader[borkborkbork]
/opt/couchbase/bin/couchbase-cli user-manage -c $CLUSTER --username $CUSER --password $CPASS --rbac-username fletcher_four --rbac-password fletcher_four --set --auth-domain local --roles query_select[products],data_reader[products],query_external_access

# configure CURL
sleep 1
echo '[!] Task 4 of 6 - Changing couchbase configurations...'
/opt/couchbase/bin/couchbase-cli setting-query -c $CLUSTER --username $CUSER --password $CPASS --set --curl-access unrestricted
echo '[!] Task 4 of 6 - Configuration updated'
sleep 5
echo '[!] Task 5 of 6 - Creating bucket indexes...'
# create indexes for data
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON blog_posts' -u $CUSER -p $CPASS
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON borkborkbork' -u $CUSER -p $CPASS
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON flag_two' -u $CUSER -p $CPASS
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON languages' -u $CUSER -p $CPASS
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON pending_posts' -u $CUSER -p $CPASS
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON products' -u $CUSER -p $CPASS
/opt/couchbase/bin/cbq -s 'CREATE PRIMARY INDEX ON status' -u $CUSER -p $CPASS
echo '[!] Task 5 of 6 - Indexes created'
sleep 10

# import data
echo '[!] Task 6 of 6 - Importing documents...'
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
echo '[!] Task 6 of 6 - Documents imported'

echo '[!] Couchbase setup complete'

touch /CBN/configured