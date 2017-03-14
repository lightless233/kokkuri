# Kokkuri Agent
The agent in the server.

## Support Service
- OpenSSH (working)
- FTP   (TODO)
- WEB   (TODO)
- MySQL (TODO)
- Redis (TODO)
- More

## Agent's rsyslog Config
### 1. OpenSSH
1.1 Edit `/etc/ssh/sshd_config`, and change the below line.
    ```
    SyslogFacility [Facility_name]
    ```
    e.g.
    ```
    SyslogFacility ssh-agent
    ```

1.2 Add a new file `/etc/rsyslog.d/ssh-auth.conf` to send ssh log to rsyslog's server.
    ```
    [Facility_name].* @@rsync_server:port
    ```
    e.g.
    ```
    ssh-agent.* @@192.168.198.128:10514
    ```
