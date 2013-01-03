#!/bin/bash

if [ ! -d ./themes ]; then mkdir ./themes; fi;

DEFAULT_THEME="modern5"

OTHER_THEMES="minimal
responsive
dark
"

CURRENT_THEME=$DEFAULT_THEME

for THEME in $OTHER_THEMES
do
  sed -i 's/'$CURRENT_THEME'/'$THEME'/g' conf.py
  CURRENT_THEME=$THEME
  echo "current theme: $CURRENT_THEME"
  tinker -b
  mv blog/html themes/$THEME
done

sed -i 's/'$CURRENT_THEME'/'$DEFAULT_THEME'/g' conf.py
tinker -b
mv themes blog/html/
