import org.openjdk.jmh.results.format.ResultFormatType;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.ChainedOptionsBuilder;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

public class KrunEntry
  implements BaseKrunEntry
{
  public void run_iter(int param)
  {
    Options opt = new OptionsBuilder()
        .forks(1)
        .warmupIterations(0)
        .measurementIterations(param)
        .resultFormat(ResultFormatType.JSON)
        .result("/home/benchmarks/results/logo_interpreter_fractal_" + System.getProperty("java.home").split("/")[4] + "_" + System.currentTimeMillis() + ".json")
        .param("program", new String[] { "/home/benchmarks/programs/logo_fractal.xmi" })
	.jvmArgs("-Xms4G", "-Xmx4G")
        .build();
    try
    {
      new Runner(opt).run();
    }
    catch (RunnerException e)
    {
      e.printStackTrace();
    }
  }
}