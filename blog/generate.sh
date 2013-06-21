#!/bin/bash

if [ ! -d ./themes ]; then mkdir ./themes; fi;

DEFAULT_THEME="flat"

OTHER_THEMES="modern5
minimal5
responsive
dark
"

CURRENT_THEME=$DEFAULT_THEME

# build blog for each theme and move build result to /themes/$THEME directory
for THEME in $OTHER_THEMES
do
  sed -i 's/'$CURRENT_THEME'/'$THEME'/g' conf.py
  CURRENT_THEME=$THEME
  echo "current theme: $CURRENT_THEME"
  tinker -b
  mv blog/html themes/$THEME
done

# build default theme
sed -i 's/'$CURRENT_THEME'/'$DEFAULT_THEME'/g' conf.py
tinker -b

# for each other theme, copy over the index.html file and static assets
for THEME in $OTHER_THEMES
do
    mv themes/$THEME/index.html blog/html/index_$THEME.html
    mv themes/$THEME/_static blog/html/_static_$THEME

    # patch references to _static so they point to _static_$THEME
    sed -i 's/_static/_static_'$THEME'/g' blog/html/index_$THEME.html
done

rm -r themes
