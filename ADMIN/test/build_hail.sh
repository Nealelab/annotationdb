#!/bin/bash

cd /Users/labbott/hail
./gradlew -Dspark.version=2.0.2 shadowJar archiveZip
gsutil cp build/distributions/hail-python.zip gs://annotationdb/test/hail-python.zip
gsutil cp build/libs/hail-all-spark.jar gs://annotationdb/test/hail-all-spark.jar

