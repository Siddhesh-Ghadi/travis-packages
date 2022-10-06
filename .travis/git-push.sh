#!/bin/bash

set -e

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

# [skip travis] ensures that the commits made via CI will not trigger travis job
commit_files() {
  git add .
  git commit --message "[skip travis] Data from travis job $TRAVIS_JOB_WEB_URL"
}

push_files() {
  git remote add https_push https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/Siddhesh-Ghadi/travis-packages.git > /dev/null 2>&1
  git pull origin $TRAVIS_BRANCH
  git push https_push HEAD:$TRAVIS_BRANCH
}

setup_git
commit_files
push_files