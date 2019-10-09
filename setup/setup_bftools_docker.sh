#!/bin/bash

curl \
-o /app/bftools.zip \
https://downloads.openmicroscopy.org/bioformats/6.2.1/artifacts/bftools.zip

unzip /app/bftools.zip -d /app/

rm /app/bftools.zip
