Supervisor PID Listener
=======================

*Require: Python 2.7 or greater*

This is a simple event handler for [Supervisord](http://supervisord.org/). Its
purpose is to write files containing PID of the processes that Supervisord
manages when they start, and delete those files when the processes stop.

By default, the files are written to `/var/run/supervisor/{processname}.pid`,
you can change this by passing in the `--location` argument. This argument also
accepts all the keys associated with the Supervisor events (e.g. `processname`,
`groupname`, `from_state`. More info [here](http://supervisord.org/events.html
#process-state-running-event-type)). Make sure the directory containing the PID files exist, and Supervisor has permission to write to that directory.

In order to use this program, add it to your `supervisord.conf` file. It is
advisable to only listen to `PROCESS_STATE_RUNNING` and `PROCESS_STATE_STOPPED`
events. For example:

```
[eventlistener:pidlistener]
command=python /path/to/your/pid.py --location=/path/to/your/pid/{processname}.pid
events=PROCESS_STATE_RUNNING,PROCESS_STATE_STOPPED
```

If the program does not work for some reason, add
`stderr_logfile=/path/to/a/stderr.log` to the `eventlistener` section, all
exception stack traces will be logged to that file.