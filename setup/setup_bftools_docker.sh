#!/bin/bash

curl \
https://downloads.openmicroscopy.org/bioformats/6.2.1/artifacts/bftools.zip \
--output \
/app/bftools.zip

unzip /app/bftools.zip

rm /app/bftools.zip
