#!/bin/bash

uri=http://test.yxyy.top/kindle-monitor.png
fbink=/mnt/us/FBInk/bin/fbink
path=/mnt/us/kindle-monitor.png
font="regular=/mnt/us/LXGWWenKai-Regular.ttf"
flashFlag=0

#initctl stop powerd
lipc-set-prop com.lab126.powerd preventScreenSaver 1
initctl stop lab126_gui
initctl stop framework
initctl stop x

while true
do
    /usr/bin/curl -o $path $uri
    $fbink -i $path
    battery=$(powerd_test -s | grep 'Battery Level' | sed 's/Battery Level: //g' | sed 's/%//g')
    flashFlag=$(expr $flashFlag + 1)
    if [ $battery -lt 25 ]
    then 
        $fbink -m -t $font,size=20,top=900,bottom=0,left=0,right=0 'Low battery!'
    fi
    if [ $flashFlag -ge 144 ]
    then
        $fbink -f -i $path
        flashFlag=0
    fi
    sleep 300
done