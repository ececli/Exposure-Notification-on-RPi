#!/bin/bash

getTXPower(){
    Input=$1
    Var=${Input##'<'*'>'}
    if [ "${Var:12:4}" = '0x0e' ] && [ "${Var:${#Var}-6:2}" = '00' ];
    then 
        echo ${Var:${#Var}-3:2}
    else
        echo 'NaN'
    fi
}

checkResult(){
    Input=$1
    # echo $Input
    Var=${Input##'<'*'>'}
    [ "${Var:12:4}" = '0x0e' ] && [ "${Var:${#Var}-3:2}" = '00' ]
}
