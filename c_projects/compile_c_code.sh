#!/usr/bin/env bash


if [[ "$UID" == "0" ]]; then
  echo "ERROR: Script must not be run as root"
  exit 1
fi

if [[ $# > 1 ]]; then
  echo "ERROR: Script only accepts one source code file as an argument"
  exit 2

elif [[ $# < 1 ]]; then
  echo "ERROR: Script must receive one argument of the soruce c file to compile"
  exit 3
fi

echo gcc $1 -o $1.compiled
gcc $1 -o $1.compiled
