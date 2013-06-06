#!/bin/bash

if [ ! -d ./themes ]; then mkdir ./themes; fi;

DEFAULT_THEME="modern5"

OTHER_THEMES="flat
boilerplate
responsive
dark
minimal5
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


# view all themes
xdg-open blog/html/index.html
sleep 5 # Firefox is already running, but is not responding.
for THEME in $OTHER_THEMES
do
  xdg-open blog/html/themes/$THEME/index.html
done
