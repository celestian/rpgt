#!/usr/bin/env bash

NAME=""
EMAIL=""
GPG_KEY=""

git config user.name ${NAME}
git config user.email ${EMAIL}
git config user.signingkey ${GPG_KEY}
git config core.editor "vim"
git config commit.template .git-commit-template
git config commit.verbose true
git config pull.ff only
git config fetch.prune true
git config diff.colorMoved zebra
git config -l
