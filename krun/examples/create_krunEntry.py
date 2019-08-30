#!/usr/bin/env python

import os
import subprocess

MODEL = '''import org.openjdk.jmh.results.format.ResultFormatType;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.ChainedOptionsBuilder;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

public class KrunEntry
  implements BaseKrunEntry
{{
  public void run_iter(int param)
  {{
    Options opt = new OptionsBuilder()
        .forks(1)
        .warmupIterations(0)
        .measurementIterations(param)
        .resultFormat(ResultFormatType.JSON)
        .result("/home/benchmarks/results/{name}_" + System.getProperty("java.home").split("/")[4] + "_" + System.currentTimeMillis() + ".json")
        .param("program", new String[] {{ "/home/benchmarks/programs/{program_name}.xmi" }})
	.jvmArgs("-Xms4G", "-Xmx4G"{extraParams})
        .build();
    try
    {{
      new Runner(opt).run();
    }}
    catch (RunnerException e)
    {{
      e.printStackTrace();
    }}
  }}
}}'''
TRUFFLE_PARAMS = ', "-Dtruffle.class.path.append=/home/benchmarks/benchmark/{language}/simplelanguage.jar"'
def extractTestName(name):
	parts = name.split(".")
	return parts[0]

patterns = ["truffle"]
#patterns = ["interpreter", "revisitor", "switch", "visitor", "truffle"]

BENCH_FOR_JMH = "/home/benchmarks/benchmark/boa/interpreter/benchmarks.jar"

testNames = map(extractTestName, os.listdir("/home/benchmarks/programs/"))

benchs = []

for testName in testNames:
	testInfos = testName.split("_")
	lang = testInfos[0]
	test = testInfos[1]

	for pattern in patterns:
		krunName = lang+"_"+pattern+"_"+test
		benchs.append(krunName)
		KRUN_ENTRY_DIR = "./benchmarks/"+krunName+"/java/"
		
		xtraParams = ""
		if pattern == "truffle":
		        xtraParams = TRUFFLE_PARAMS.format(language=lang)
	
		if not os.path.exists(KRUN_ENTRY_DIR):
			os.makedirs(KRUN_ENTRY_DIR)
			
		f= open(KRUN_ENTRY_DIR+"KrunEntry.java","w+",0)

                
		tmp = MODEL.format(extraParams=xtraParams, name=krunName, program_name=testName)
		f.write(tmp)
		f.close

		javac = ["javac","-cp",BENCH_FOR_JMH+":../iterations_runners/", KRUN_ENTRY_DIR+"KrunEntry.java"]
		proc = subprocess.Popen(javac)

f = open("bench_list.txt","w+",0)
f.write(";".join(benchs))
f.close()





