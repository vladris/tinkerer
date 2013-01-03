#!/bin/bash

if [ ! -d ./themes ]; then mkdir ./themes; fi;

DEFAULT_THEME="modern5"

OTHER_THEMES="minimal
responsive
dark
"

CURRENT_THEME=$DEFAULT_THEME

# disable disqus comments
sed -i "s/, 'tinkerer.ext.disqus'//g" conf.py

for THEME in $OTHER_THEMES
do
  sed -i 's/'$CURRENT_THEME'/'$THEME'/g' conf.py
  CURRENT_THEME=$THEME
  echo "current theme: $CURRENT_THEME"
  tinker -b
  mv blog/html themes/$THEME
done

# enable disqus comments again
sed -i "s/'tinkerer.ext.blog'/'tinkerer.ext.blog', 'tinkerer.ext.disqus'/g" conf.py

sed -i 's/'$CURRENT_THEME'/'$DEFAULT_THEME'/g' conf.py
tinker -b
mv themes blog/html/
