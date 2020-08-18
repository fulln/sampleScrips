#!/bin/bash

hostip="" 
username=""
passwd=""
location=""

## 计数器
index=1
## 未输入参数
if [ -z "$1" ];
then                           
   echo "Usage: will be used default params"
   hostip="${hostip}24"
else
   echo "listing args with \$*:"
   for arg in  $*
   do 
	   echo arg: $index = $arg
	   if [ $index  == 1 ];
	   then		   
	   	  len=$arg|wc -L
                  if [ ${len} >3 ];
                  then
                    hostip="$arg"
                  else
                    hostip="$hostip$arg"
                  fi 
	   elif [ $index == 2 ];
	   then
		username=$arg
	   elif [ $index == 3 ];
	   then
	   	passwd=$arg
	   else [ $index == 4 ];
   		location=$arg	
     	   fi
           let index += 1	   
   done    
   echo   
      	   
fi

echo  $hostip $username $passwd $location

expect login.exp $hostip $username $passwd $location

