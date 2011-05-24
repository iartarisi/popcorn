#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           popcorn
Version:        0.1
Release:        0
License:        X11/MIT
Summary:        Popularity Contest (for RPM)
Url:            https://gitorious.org/opensuse/popcorn
Group:          System/Packages
Source:         %{name}.tar.bz2
Requires:       cron
Requires:       rpm-python
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Popularity Contest (for RPM).

%package server
Summary:        Server for Popularity Contest (for RPM)
Requires:       python-redis
Requires:       python-tornado

%description server
Server for Popularity Contest (for RPM).

%prep
%setup -q -c -n %{name}

%build
# not needed

%install
# client files
install -D -m 0755 popcorn-client %{buildroot}%{_bindir}/popcorn
install -D -m 0644 popcorn.conf   %{buildroot}%{_sysconfdir}/popcorn.conf
install -D -m 0755 popcorn.cron   %{buildroot}%{_sysconfdir}/cron.weekly/popcorn
# server files
install -D -m 0755 server/popcorn-server      %{buildroot}%{_sbindir}/popcorn-server
install -D -m 0644 server/index.html          %{buildroot}%{_datadir}/popcorn/index.html
install -D -m 0644 server/server.conf         %{buildroot}%{_sysconfdir}/popcorn-server.conf
install -D -m 0755 server/popcorn-server.init %{buildroot}%{_initddir}/popcorn-server
ln -s %{_initddir}/popcorn-server %{buildroot}%{_sbindir}/rcpopcorn-server
# use absolute paths
sed -i "s:^CONFIG_FILE = .*$:CONFIG_FILE = '%{_sysconfdir}/popcorn-server.conf':" %{buildroot}%{_sbindir}/popcorn-server
sed -i "s:^INDEX_FILE  = .*$:INDEX_FILE  = '%{_datadir}/popcorn/index.html':"     %{buildroot}%{_sbindir}/popcorn-server

%clean
rm -rf %{buildroot}

%pre server
/usr/sbin/groupadd -r popcorn &>/dev/null || :
/usr/sbin/useradd -o -g popcorn -s /bin/false -r -c "User for Popcorn server" -d /var/lib/empty popcorn-server &>/dev/null || :

%post server
%fillup_and_insserv -y popcorn-server

%preun
%stop_on_removal popcorn-server

%postun
%restart_on_update popcorn-server
%insserv_cleanup

%files
%defattr(-,root,root)
%doc README
%{_bindir}/popcorn
%config(noreplace) %{_sysconfdir}/popcorn.conf
%{_sysconfdir}/cron.weekly/popcorn

%files server
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/popcorn-server.conf
%dir %{_datadir}/popcorn
%{_datadir}/popcorn/index.html
%{_sbindir}/popcorn-server
%{_sbindir}/rcpopcorn-server
%{_initddir}/popcorn-server

%changelog
