#!/bin/sh
if ps -ef | grep -v grep | grep qualify.py ; then
	exit 0
else
	. /root/Thesis/meditation/meditations/bin/activate
	python /root/Thesis/meditation/2-25/qualify.py
	echo "started qualifying tweets"
	exit 0
fi
