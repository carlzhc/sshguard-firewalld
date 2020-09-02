Name:           sshguard-firewalld
Version:        1.7.1
Release:        1%{?dist}
Summary:        Protect hosts from brute-force attacks
License:        ISC and BSD and Public Domain
URL:            http://www.sshguard.net/
Source0:        http://downloads.sourceforge.net/project/sshguard/sshguard/%{version}/sshguard-%{version}.tar.gz
Source1:        sshguard.service
Source2:        sshguard.sshg-fwd
Source3:        sshguard.sysconfig
Source4:        sshguard.whitelist

BuildRequires:  systemd
Requires:       firewalld
Conflicts:      sshguard
%{?systemd_requires}


%description
sshguard protects hosts from brute-force attacks against SSH and other
services.  It aggregates system logs and blocks repeat offenders using
iptables.

sshguard can read log messages from standard input (suitable for piping from
syslog) or monitor one or more log files.  Log messages are parsed,
line-by-line, for recognized patterns.  If an attack, such as several login
failures within a few seconds, is detected, the offending IP is blocked.
Offenders are unblocked after a set interval, but can be semi-permanently
banned using the blacklist option.


%prep
%setup -q -n sshguard-%{version}

%build
# glibc headers need POSIX_C_SOURCE:
#export CFLAGS="$CFLAGS -D_POSIX_C_SOURCE=200112L"
%configure --with-firewall=iptables
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
%make_install

mkdir -p $RPM_BUILD_ROOT%{_unitdir}/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/
install -m 755 -D %{SOURCE2} $RPM_BUILD_ROOT%{_libexecdir}/sshg-fwd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 -D %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sshguard
install -m 644 -D %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sshguard/whitelist

%post
if [ $1 -eq 1 ]; then
    %{_libexecdir}/sshg-fwd add
fi

%systemd_post sshguard.service


%preun
%systemd_preun sshguard.service

if [ $1 -eq 0 ]; then
    %{_libexecdir}/sshg-fwd remove
fi


%postun
%systemd_postun_with_restart sshguard.service


%files
%doc README.rst COPYING examples
%doc %{_mandir}/man8/sshguard.8*
%{_sbindir}/sshguard
%{_unitdir}/sshguard.service
%{_libexecdir}/sshg-fwd
%{_libexecdir}/sshg-fw
%{_libexecdir}/sshg-logtail
%{_libexecdir}/sshg-parser
%config(noreplace) %{_sysconfdir}/sshguard
%config(noreplace) %{_sysconfdir}/sysconfig/sshguard


%changelog
* Sun Aug 30 2020 Carl <356878@gmail.com> - 1.7.1-1
- Initial package
