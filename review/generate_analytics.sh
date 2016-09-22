#!/bin/sh
pyreverse -o png ../pymarkoff
pylint ../pymarkoff -f html > linting-report.html
