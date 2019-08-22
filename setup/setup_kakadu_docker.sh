#!/bin/bash

curl \
https://kakadusoftware.com/wp-content/uploads/2014/06/\
KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827.zip \
--output \
/app/KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827.zip

unzip /app/KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827.zip \
-d /app/

rm /app/KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827.zip
