# XipppyServer
 Software for take-home trial with advanced neuromyoelectric prosthesis


### Nommad Login info

Refer to `NomadHelp.txt` and `HowToSSH_into_Ripple.txt` for help.

Username and Password to Ripple Nomad (or Summit) are `root` and `root`


##### SSH into the Nomad

Below is a log of working commands to connect to the Ripple Neuro Bio-Amplifier (tested on a specific Ripple Summit*)
- MUST BE USING LINUX (Ubuntu/WSL) OR GIT BASH
*Yes, we are aware that it is called Nomad instead of summit on the machine, this itself is not a breaking issue

- This was tested using Git BASH on windows. You need linux command line features for this to work properly. In theory, wsl
would also work great: https://learn.microsoft.com/en-us/windows/wsl/install

Enter the following command when on the same network or connected to the Ripple Neuro Device:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa root@192.168.42.1
```

You will then be prompted with "Are you sure you want to continue connecting (yes/no/[fingerprint])?" 

Type "**yes**" and hit `Enter`

```bash
$ ssh -oHostKeyAlgorithms=+ssh-rsa root@192.168.42.1
The authenticity of host '192.168.42.1 (192.168.42.1)' can't be established.
RSA key fingerprint is SHA256:nYTKUObqiJffmVPkgbmeg//4rjXCLI5YDoQJrGsJ85I.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

Finally you will be prompted for a password. Enter `root`

```bash
root@192.168.42.1's password: root
```

## Check if Xippy is running:


1. Check Service Status (Recommended)
The repository uses systemd to manage background processes. You can query the status of your specific service to see if it is active, running, or failed.

Run this command over your SSH connection:

```bash
systemctl status XipppyServer.service
```

- Active (running): The service is currently executing.
- Inactive (dead): The service is not running.
- Failed: The service attempted to start but crashed due to a configuration error or hardware communication issue.

2. View Real-time Logs
If the service is running but you aren't sure if it is successfully streaming data, you can view the live output (stdout/stderr) of the service:

```bash
journalctl -u XipppyServer.service -f
```
The -f flag keeps the terminal open and updates in real-time. If the XipppyServer.py script is printing connection status or streaming heartbeats, they will appear here.

3. Check for the Process Directly
If you suspect the service is not managed by systemd or you just want to verify the Python process is alive in the OS process table:

```bash
ps aux | grep python
```
This will list all running Python processes. You should see a command line that includes python followed by the path to XipppyServer.py.

Troubleshooting Note: If the service is in a "failed" state, the logs from journalctl usually indicate a permission issue with the hardware interface or a missing dependency in the local Python environment (e.g., if the xipppy wheel was not correctly installed in the system's dist-packages).