#!/bin/bash
# Script to format switchboard alignment file, removing special chars from text which are not used in processing

INPUT=$1
OUTPUT=$2

# remove special chars from swb
echo "remove special chars"

sed "/'\/\/', / s///g" $INPUT > $OUTPUT
sed -i "/, '\/\/'/ s///g" $OUTPUT
sed -i "/\['\/\/']/ s//\[]/g" $OUTPUT

sed -ri "/'-+', / s///g" $OUTPUT
sed -ri "/, '-+'/ s///g" $OUTPUT
sed -ri "/\['-+']/ s//\[]/g" $OUTPUT

sed -i '2, $s/[a|b]_//g' $OUTPUT

sed -ri "/'\"+([a-z]+)\"+'/ s//'\1'/g" $OUTPUT
