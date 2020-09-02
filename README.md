# sshguard-firewalld

This is to make sshguard running with firewalld firewall.
It can be installed for rhel, centos, or fedora.

This was created from compiling sshguard 1.7.1 from source from sshguard.sourceforge.net
and I program a script to add/remove chain in firewalld for sshguard.

No guarantees for running it may mess up your system, but it seems to work well.

To build from source:
```
make -f Makefile
```

To install:
```
yum install https://github.com/carlzhc/sshguard-firewalld/raw/master/RPMS/x86_64/sshguard-firewalld-1.7.1-1.el7.x86_64.rpm
```
