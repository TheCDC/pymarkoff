#!/bin/sh
pyreverse -S -A -o png ../pymarkoff
pylint ../pymarkoff -f html > linting-report.html
