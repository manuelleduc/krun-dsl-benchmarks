#!/usr/bin/env python

import os
import subprocess

MODEL = '''import org.openjdk.jmh.results.format.ResultFormatType;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.ChainedOptionsBuilder;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;
import org.openjdk.jmh.annotations.*;

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
        .param("modelPath", new String[] {{ "{program_name}" }})
		    .jvmArgs("-Xms4G", "-Xmx4G")
        .mode(Mode.SingleShotTime)
        .build();
    try
    {{
      new Runner(opt).run();
    }}
    catch (Exception e)
    {{
      e.printStackTrace();
    }}
  }}
}}'''

patterns=['interpreter','modularrevisitor','monolithicrevisitor','visitor','switch']
programs=['p1', 'p2', 'p3']

real_names = {
	'p1': 'testperformance_variant1',
	'p2': 'testperformance_variant2',
	'p3': 'testperformance_variant3',
}

for program in programs:
	for pattern in patterns:
		krunName = program+'_'+pattern
		KRUN_ENTRY_DIR = "./benchmarks/"+krunName+"/java/"
		
		if not os.path.exists(KRUN_ENTRY_DIR):
			os.makedirs(KRUN_ENTRY_DIR)
			
		f= open(KRUN_ENTRY_DIR+"KrunEntry.java","w+",0)
		tmp = MODEL.format(name=krunName, program_name=real_names[program])
		f.write(tmp)
		f.close