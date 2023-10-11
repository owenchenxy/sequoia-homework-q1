# User Manual
This tools parses key information from **user specified log file** and send to **user specified server**

# Configuration
The default configuration file `config.yaml` is located in the repo's root directory. There're several customizable configs:
- **log_server.url**: The url the analysis result will be sent to, default is `foo.com/bar`
- **log_server.protocol**: The protocal (http/https) the tool use to send data to the log server, default is `https`
- **log_server.verify**: Set it `true` if https is used, else set it `false`
- **log_server.cert_file**: The `.pem` file path you use for SSL/TLS verification

# Command Line Options
You can run as below using the default configuration file:

```bash
python3 main.py -f syslog.log
```

If your configuration file is located somewhere else, run:
```bash
python3 main.py -c <config_file_path> -f syslog.log
```