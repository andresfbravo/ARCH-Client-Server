#!/bin/bash
rm o.o
#g++ -std=c++11 -ggdb -o o.o kmeans2.cpp
g++ -std=c++11 -ggdb -o o.o kmeans2.cc
#$k="\n"
#ejecutable datos dimensiones k numero_corridas centroides iniciales

for i in {1..1}
do
	./o.o datos.csv 3 8 10 centroides.csv #>> salida.csv
	#echo $k
done
