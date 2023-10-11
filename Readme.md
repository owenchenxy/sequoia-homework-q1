# User Manual
This tools parses key information from **user specified log file** and send to **user specified server**

# Configuration
The default configuration file `config.yaml` is located in the repo's root directory. There're several customizable configs:
- **log_server.url**: The url the analysis result will be sent to, default is `foo.com/bar`
- **log_server.protocol**: The protocal (http/https) the tool use to send data to the log server, default is `https`
- **log_server.verify**: Set it `true` if https is used, else set it `false`
- **log_server.cert_file**: The `.pem` file path you use for SSL/TLS verification

# Command Line Options
## Use Default Configuration Path
You can run as below using the default configuration file:
```bash
python3 main.py -f syslog.log
```

## Use Custom Configuration File Path
If your configuration file is located somewhere else, run:
```bash
python3 main.py -c <config_file_path> -f syslog.log
```

## Show Response From Server
To show response from server, specify option `-s` or `--show-response`
```bash
python3 main.py -f syslog.log --show-response
```
# Test
With the configs below, we can send data to the `httpbin` server.
```yaml
log_server:
  # log server address
  url: "httpbin.org/post"
  # http or https
  protocal: "https"
  # whether we verify the server's TLS certificate
  verify: true
  # path to ssl client cert file (.pem)
  cert_file: ""
```

Run the command below:
```bash
python3 main.py -f syslog.log
```

By specifying `-s` or `--show-response` we can see the response and find the post data in it.
```bash
python3 main.py -f syslog.log --show-response
```