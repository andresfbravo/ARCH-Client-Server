#!/bin/bash
rm o.o
g++ -std=c++11 -o o.o -fopenmp kmeansOmp.cpp

#$k="\n"

for i in {1..10}
do
	./o.o datos.csv 4 50 centroides.csv #>> salida.csv
	#echo $k
done
