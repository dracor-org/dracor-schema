#!/bin/sh

if [ -z "$2" ]; then
  echo "Usage: migrate.sh stylesheet xmlfile [xmlfile ...]"
  echo
  exit
fi

xsl=$1
shift

echo Stylesheet: $xsl

for f in $@; do
  tmp=$f.tmp
  cp -v $f $tmp
  saxon -xsl:$xsl -s:$tmp \
    | sed -E 's/(--|\?)><(TEI|teiCorpus|!--|\?)/\1>\n<\2/g' \
    | sed -E 's/<\/(TEI|teiCorpus)>$/<\/\1>\n/' \
    > $f
  rm $tmp
done
