#!/bin/bash

cd /home/hail/
git clone https://github.com/liameabbott/hail.git
git config --global user.email "liam.e.abbott@gmail.com"
git config --global user.name "Liam"
chmod 777 -R /home/hail/hail

sed -i -e 's/spark.files=\/home\/hail\/.*jar/spark.files=\/home\/hail\/hail\/build\/libs\/hail-all-spark.jar/' /etc/spark/conf/spark-defaults.conf
sed -i -e 's/spark.submit.pyFiles=\/home\/hail\/.*zip/spark.submit.pyFiles=\/home\/hail\/hail\/build\/distributions\/hail-python.zip/' /etc/spark/conf/spark-defaults.conf
sed -i -e 's/spark.driver.extraClassPath=\.\/.*jar:\/home\/hail\/.*jar/spark.driver.extraClassPath=\.\/hail-all-spark.jar:\/home\/hail\/hail\/build\/libs\/hail-all-spark.jar/' /etc/spark/conf/spark-defaults.conf
sed -i -e 's/spark.executor.extraClassPath=\.\/.*jar:\/home\/hail\/.*jar/spark.executor.extraClassPath\.\/hail-all-spark.jar:\/home\/hail\/hail\/build\/libs\/hail-all-spark.jar/' /etc/spark/conf/spark-defaults.conf

apt-get -y install cmake
