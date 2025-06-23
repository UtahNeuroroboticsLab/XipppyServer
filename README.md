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

