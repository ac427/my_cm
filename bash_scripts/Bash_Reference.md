# How to pin a process to a cpu on multicore cpu

Examples:
taskset <COREMASK> <EXECUTABLE>

```
taskset 1 vlc
```

[taskset2]

Pin a Running Process ( below example 9030 is pid)  to Particular CPU Core(s)

```
taskset -cp 0,4 9030 
```

[taskset1]


# top command
 
- top -u uid . To display only process of uid
- top -b -n 1. To display top in batch mode for 1 time 
- Press 'shift+O' to Sort. (Uppercase Letter 'O') . example press ‘a‘ letter to sort process with PID (Process ID).
- Press '1' to display all cpu information
- Press 'c' to display absolute path of the command
- Press 'z' to hightlight running process
- Press 'd' to set screen refresh intervel
- Press 'k' to kill a process
- Press 'h' for help
- Press 'r' to renice a process
- Press 'shift+W' to save top info

# Screen command

 Below command will start screen session with name one
```
 screen -s one.
```

Below command is used to detach screen one
```
screen -d one
```

To list all screen sessions
```
screen -ls
```
To reattach to screen session
```
screen -r
```
Below will Reattach a session and if necessary detach it first.
```
screen -dr
```

[taskset1]: http://veithen.github.io/2013/11/18/iowait-linux.html
[taskset2]: http://xmodulo.com/run-program-process-specific-cpu-cores-linux.html
