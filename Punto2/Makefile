all: bestmodels.txt

bestmodels.txt: lineal.txt lineal_gaussiano.txt lineal_paso.txt bestmodels.py
	python bestmodels.py

lineal_paso.txt: intervalos.txt lineal_paso.py
	python lineal_paso.py

lineal_gaussiano.txt: intervalos.txt lineal_gaussiano.py
	python lineal_gaussiano.py

lineal.txt: intervalos.txt lineal.py
	python lineal.py

intervalos.txt: leer_timescsv.R
	Rscript leer_timescsv.R

clean:
	rm -f *.pdf *.txt