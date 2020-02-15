#!/bin/bash
# Script to format switchboard file for tagging with NCRFpp package

INPUT=$1
COL=$2
FILE=$3

# cut words and add extra spaces
cut -d$'\t' -f$COL $INPUT > $FILE
sed -i G $FILE

# add symbol for empty sentences
echo "add symbol for empty sentences"
sed -i "/\['\/\/']/ s//#/g" $FILE
sed -i "/\['--']/ s//#/g" $FILE
sed -i "/\[]/ s//#/g" $FILE

# remove header
echo "remove header"
tail -n +3 $FILE > "$FILE.tmp" && mv "$FILE.tmp" $FILE

# divide words by newline
sed -i '/, / s//\n/g' $FILE

# remove special chars
echo "remove special chars"
sed -i '/\/\// d' $FILE
sed -i '/--/ d' $FILE
sed -i "/\['/ s///g" $FILE
sed -i "/']/ s///g" $FILE
sed -i "/^'/ s///g" $FILE
sed -i "/'$/ s///g" $FILE
sed -i '/"/ s///g' $FILE
sed -i '/\[/ s///g' $FILE
sed -i '/]/ s///g' $FILE

# a hacky fix because NCRFpp requires label info on decoding
echo "add labels"
sed -i '/$/ s//\tSYM/g' $FILE
sed -i '/^\tSYM/ s///g' $FILE
