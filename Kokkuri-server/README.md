# Kokkuri Server
The Kokkuri Server.

## Support Service
- OpenSSH (working)
- FTP   (TODO)
- WEB   (TODO)
- MySQL (TODO)
- Redis (TODO)
- More

## Rsyslog Server's Config
1. Edit the `/etc/rsyslog.conf`, change the below line.
    ```
    # provides UDP syslog reception
    module(load="imudp")
    input(type="imudp" port="10514")
    
    # provides TCP syslog reception
    module(load="imtcp")
    input(type="imtcp" port="10514")
    ```
    In my project, the port is set to 10514 and you can replace it with your own lucky number.
2. Add a new file `/etc/rsyslog.d/kokkuri-server.conf`
    ```
    local6.* /path/to/rsyslog/received/log.log
    ```
    The `local6` must be same with the agent's facility name. Change the path to the real path on your disk. The agent's
    log will save to this log file.