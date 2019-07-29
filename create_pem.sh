#!/bin/bash
# openssl enc -aes-256-cbc -in $2 -k $1 -out $3;
# openssl enc -aes-256-cbc -in $2 -k $1 -d;
# openssl rsautl -encrypt -pubin -inkey %s -in %s -out %s;
# openssl rsautl -decrypt -inkey %s -in %s;

openssl genrsa -out priv.pem $1;
openssl rsa -in priv.pem -pubout -out pub.pem;


