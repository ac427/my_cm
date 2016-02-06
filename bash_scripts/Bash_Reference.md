# How to pin a process to a cpu on multicore cpu

Examples:
taskset <COREMASK> <EXECUTABLE>

taskset 1 vlc

[taskset2]

Pin a Running Process to Particular CPU Core(s)

taskset -cp 0,4 9030 

[taskset1]













[taskset1]: http://veithen.github.io/2013/11/18/iowait-linux.html
[taskset2]: http://xmodulo.com/run-program-process-specific-cpu-cores-linux.html
