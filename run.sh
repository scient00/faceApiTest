#!/bin/sh

host="http://120.79.151.3:8011"
AppId="f6f96cec55e5a9823c6115ddcad6ff80"
AppSecret="cc4c90231dd9e6b970fdd8d385e7a782b2bd9f59"
multiNum=10
vSampleList="/mnt/00_TestSample/samplePath/Testface2220.ly"

if [ $# -lt 1]
then
	type=1
else
	type=$1

fi

nohup python Test.py $host $AppId $AppSecret $multiNum $vSampleList $type & .

