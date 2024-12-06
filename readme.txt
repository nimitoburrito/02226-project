The archive contains two test cases.
One of the test cases is the case used for manual calculations. The files used are:
	- test-streams.csv
	- test-topology.csv
The test case for the omnet++ simulations used the files:
	- streams.csv
	- topology.csv
The outputs of these files are also included as:
	- test-output.csv for test-streams.csv and test-topology.csv
	- output.csv for streams.csv and topology.csv
	
The maple file which was used for manually calculate the first test case is called nescalc.mw

The tool itself consists of two python files:
	- switch.py
	- network_creator.py
The main file that is run when running the tool is network_creator.py. This file has two variables in the top, where the topology and streams files are stored. These can be changed to use other networks. There is a problem with the tool, in that it expects the switches and end systems names to start in a specific way. This can be changed in the code, and in the version that is handed in, it expects the names in the form SWx or ESx, where x can be any string. 



