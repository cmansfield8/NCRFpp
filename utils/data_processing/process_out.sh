#!/bin/bash
# create a file that can append to switchboard annotation from NCRFpp output

INPUT=$1
FILE=$2
COLUMN=$3

# remove misc. text and tokens, put tags side by side
sed '/# 1.0000/ d' $INPUT > "${FILE}.tmp"
cut -d' ' -f2 "${FILE}.tmp" > $FILE

# remove contractions
sed "/^'/ d" $FILE

# surround tag with apostrophe
sed -i -E "/^(.)/ s//'\1/g" $FILE
sed -i -E "/(.)$/ s//\1'/g" $FILE

# put tag sequence on each line seperated by commas
sed -i -E ':a;N;$!ba;s/(.)\n/\1, /g' $FILE

# add brackets to beginning and end of each unit
sed -i -E '/^(.)/ s//[\1/g' $FILE
sed -i '/, $/ s//]/g' $FILE

# add header
sed -i '1 i\'$COLUMN $FILE

rm "${FILE}.tmp"
