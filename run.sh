#!/bin/sh

host="http://114.80.100.146:3002"
AppId="b2268f0901893d4f8d5c7f123c602712"
AppSecret="22c5334624496bdec437945d3e43deb10616f430"
multiNum=10
vSampleList="/mnt/00_TestSample/samplePath/Testface2220.ly"

if [ $# -lt 1 ]
then
	type=1
else
	type=$1
fi

nohup python Test.py $host $AppId $AppSecret $multiNum $vSampleList $type & .

