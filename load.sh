#!/bin/bash

for i in \
  array_search.sql \
  pgmapcss_types.sql \
  pgmapcss_parse_string.sql \
  pgmapcss_condition.sql \
  pgmapcss_parse_selector.sql \
  pgmapcss_parse_selectors.sql \
  pgmapcss_parse_properties.sql \
  pgmapcss_build_statement.sql \
  pgmapcss_compile_content.sql \
  pgmapcss_parse_eval.sql \
  pgmapcss_compile_eval.sql \
  eval.sql \
  pgmapcss_compile.sql \
  pgmapcss_install.sql
do
  echo "* $i"
  psql $@ -f $i
done

echo "=== Resulting function ===" > test.output
FILE=`cat test.mapcss`
psql $@ -P format=unaligned -c "select pgmapcss_install('test', \$\$$FILE\$\$);" | tail -n+2 | head -n-2 >> test.output

less test.output