#!/bin/bash
git add .
echo "Enter a comment for commit:"
read comment
git commit -m "$comment"
git push