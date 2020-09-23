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
while getopts ':i:n:p:k:' arg
do
	case $arg in
		i)	
			leng=`echo $OPTARG|wc -c`	
			if [ ${leng} -gt 4 ];
			then 
		  		hostip="$OPTARG"		
			else
	   	 		hostip="$hostip$OPTARG"
			fi 
		;;
		n)
			username=$OPTARG
		;;
		p)
			passwd=$OPTARG
		;;
		k)
			location=$OPTARG			
		;;	
		?)
			echo "未知参数"
		;;
	esac
done
fi

case $location in
	"trans")
		location=""		
	;;
	"act")
		location=""
	;;
	"op")
		location=""
	;;
	?)
	echo "未知参数"
	exit 22;;
esac

echo  $hostip $username $passwd $location 

expect $PWD/login.exp $hostip $username $passwd $location
