#!/bin/bash
rm o.o
g++ -std=c++11 -o o.o kmeans.cpp

#$k="\n"
#ejecutable datos dimensiones k numero_corridas centroides iniciales

for i in {1..10}
do
	./o.o datos.csv 3 4 50 centroides.csv #>> salida.csv
	#echo $k
done
