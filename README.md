# Measurement Context

## Hardware

- **CPU:** Intel(R) Xeon(R) W-2104 CPU @ 3.20GHz
- **RAM** 15G
- **SSD Drive:** ???


### BIOS

- deactivate turboboots
- decativate hyperthreading

## Operating System

- **Linux distribution:** Debian with running with the particular KRUN kernel

### Managed

- deactivating performance optimizations in the BIOS
- deactivating P-states
- mono-threaded operating system
- deactivating network connectivity, SSH, cron

## Virtual Machines

- **HotspotVM** version 8, 11, 12
- **HotspotVM** version 8, 11, 12
- **GraalVM CE** version 19.1.1
- **GraalVM EE** version 19.1.1

### Managed

- Fixing allocated memory `-Xms4G -Xmx4G`
- Use JMH Benchmarking Framework


# How to reproduce the experiment

On the repository you have a lot of files and the following are really important.

![Important files in the project](/assets/images/Experiment.png)

## Where do i put my files

As you can see, in the `benchmarks` user home you have a folder named `benchmark`. 
In this folder you need to create a folder for each language you want to benchmark.
Inside those folders you will create a folder for each pattern of implementation of
your interpreter. Moreover, if you want to benchmark Truffle languages, you need to
put here the jar file of the truffle project.
Then simply put your benchmarks jar file in the pattern folder.

The next step is choosing the JVM you will use. For that you simply have to unzip your
JVMs in the `jvms` folder.

As you can imagine, the programs you want to use in your benchmarks will be put in the
`programs` folder. This programs need to follow a conventional name made by combining
the language name and the program name. Of course your programs need to be XMI files.

## How do i configure my benchmarks

All the configuration files are in `/home/benchmarks/krun/`.

In the `examples` folder, you can find a script named `create_krunEntry.py`. This script
generate the entry point that Krun will use to call your benchmarks. This script contains
the model of a Java entry point using JMH with the management of Truffle parameters.
You have to put all the pattern you want to benchmark in the pattern list because this
script create a benchmark for a pair <pattern, program>. 

NB : This script also create the `bench_list.txt` file to let the Krun initialisation script 
do the combinatorics between VM an benchmarks without creating invalid pair like 
boa_interpreter_fibonacci run on a minijava interpreter

In the second level `krun` folder you will find the `vm_defs.py` file. It's in this 
file that we define how our JVM will be called.

``` python
def run_exec(self, entry_point, iterations,
             param, heap_lim_k, stack_lim_k, key, key_pexec_idx,
             force_dir=None, sync_disks=True):
    """Running Java experiments is different due to the way that the JVM
    doesn't simply accept the path to a program to run. We have to set
    the CLASSPATH and then provide a class name instead"""
```

This function is used to run the benchmark and use the entry points we just created as parameters.

In the `examples` folder again, you can find two Krun files `benchmarks.krun` and `onlyjava.krun`.
Those files purpose is to configure your experiment process.  

## How do i run the experiment

There is two solution, one to test that your benchmarking process work correctly and the second
is to run from `/etc/rc.local` to do the real experiment.

`/etc/rc.local`
``` sh
#!/bin/sh
/usr/bin/sudo -u benchmarks /home/benchmarks/krun/scripts/run_krun_at_boot /home/benchmarks/krun/examples/benchmarks.krun
exit 0
```

To test your process run directly the following command :
``` sh
sudo ~/krun/krun.py ~/krun/examples/benchmarks.krun
```
**WARNING :** You will probably have to add parameters to this command because it will not restart the hardware

**WARNING 2 :** Do not deactivate the network if you are working with ssh. It will kill the process and never reactivate the network


# References:

## Explored 
- Virtual Machine Warmup Blows Hot and Cold (Barrett et al.) \[[Arxiv](https://arxiv.org/abs/1602.00602)\] \[[DOI](http://dx.doi.org/10.1145/3133876)\]
- Renaissance project: [measurements](https://github.com/renaissance-benchmarks/measurements)

## Unexplored

DaCapo [21], ScalaBench [100], and SPECjvm2008 [1] (from https://renaissance.dev/resources/docs/renaissance-suite.pdf)