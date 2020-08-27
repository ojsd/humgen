#!/usr/bin/env bash
# Export the "build" documentation files to glaccios-server
# Documentation can then be seen in http://157.136.74.67:10080/humgen
rsync -r ../docs/build/ ojossoud@157.136.74.67:/var/www/html/humgen/
