#!/bin/bash

cd /Users/labbott/Documents/hail
./gradlew shadowJar archiveZip
gsutil cp build/distributions/hail-python.zip gs://annotationdb/test/hail-python.zip
gsutil cp build/libs/hail-all-spark.jar gs://annotationdb/test/hail-all-spark.jar

