#!/bin/bash
rm o.o
g++ -std=c++11 -o o.o -fopenmp kmeans2Omp.cc

#$k="\n"

for i in {1..1}
do
	./o.o datos.csv 3 5 10 centroides.csv #>> salida.csv
	#echo $k
done
