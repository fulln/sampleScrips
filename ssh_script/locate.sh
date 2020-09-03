#!/bin/bash

hostip="" 
username=""
passwd=""
location=""

## 未输入参数
if [ -z "$1" ];
then                           
   echo "Usage: will be used default params"
   hostip="${hostip}24"
else   
while getopts ":ip:name:pass:pack:" arg
do 
	case $arg in
		ip)
		len=$arg|wc -c      
		if [ ${len} >4 ];
		then 
		  hostip="$arg"		
		else
	   	  hostip="$hostip$arg"
		fi 
		;;
		name)
		username=$arg
		;;
		pass)
		passwd=$arg
		;;
		pack)
		location=$arg			
		;;	
		?)
			echo "未知参数"
		;;
	esac
done
fi

case $location in
	"trans")
		location="es-cabinet-transfer"		
	;;
	"act")
		location="fcbox-activity-core"
	;;
	"op")
		location="fcbox-oplatform-admin"
	;;
	?)
	echo "未知参数"
	exit 22;;
esac

echo  $hostip $username $passwd $location 

expect $PWD/login.exp $hostip $username $passwd $location

