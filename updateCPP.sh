#!usr/bin/bash


# creat cron to run every 30 days
#

########################
# 1. fetch data with: fetch.py 
# 2. load new data to db with: loadDB.py
# 3. generate new matrix with: mining.py
# 4. move matrix file to cpp folder for use.
# 5. Restart the server with CPP
#
#
#
#
#
#python fetch.py
#python loadDB.py
#python mining.py
mongoexport --db minepm --collection bladdercancer  --out bladder.json --jsonArray
mv bladder.json ../cpp/src/assets/json
mongoexport --db minepm --collection lungcancer --out lung.json --jsonArray
mv lung.json ../cpp/src/assets/json
mongoexport --db minepm --collection coloncancer --out colon.json --jsonArray
mv colon.json ../cpp/src/assets/json
mongoexport --db minepm --collection pancreaticcancer --out pancreatic.json --jsonArray
mv pancreatic.json ../cpp/src/assets/json
mongoexport --db minepm --collection prostatecancer --out prostate.json --jsonArray
mv prostate.json ../cpp/src/assets/json
