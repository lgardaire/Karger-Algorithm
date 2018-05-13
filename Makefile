all: algo.ex stat.ex

algo.ex:
	cp source/algo.py algo.ex

stat.ex:
	cp source/algo_stat.py stat.ex
clean:
	rm algo.ex
	rm stat.ex
