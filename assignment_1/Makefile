default: main

main: main.o average.o
	gcc -o main main.o average.o

average.o: average.c average.h
	gcc -c average.c

main.o: main.c
	gcc -c main.c
