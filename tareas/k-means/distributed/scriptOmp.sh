#!/bin/bash
rm o.o
g++ -std=c++11 -o o.o -fopenmp kmeansOmp.cc

#$k="\n"

for i in {1..10}
do
	./o.o datos.csv 3 $i #10 centroides.csv #>> salida.csv
	#echo $k
done
