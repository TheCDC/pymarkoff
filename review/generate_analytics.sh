#!/bin/sh
pyreverse -o png ../pymarkoff
pylint ../pymarkoff -f html > linting-repot.html
