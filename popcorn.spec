#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           popcorn
Version:        0.1
Release:        0
License:        X11/MIT
Summary:        Popularity Contest (for RPM)
Url:            http://en.opensuse.org/Popcorn
Group:          System/Packages
Source:         %{name}.tar.bz2
Requires:       cron
Requires:       rpm-python
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Popularity Contest (for RPM)

%package server
Summary:        Server for Popularity Contest (for RPM)
Requires:       python-redis
Requires:       python-tornado

%description server
Server for Popularity Contest (for RPM)

%prep
%setup -q -n %{name}

%build

%install
# client files
install -D -m 0755 popcorn-client %{buildroot}%{_bindir}/popcorn
install -D -m 0644 popcorn.conf   %{buildroot}%{_sysconfdir}/popcorn.conf
install -D -m 0755 popcorn.cron   %{buildroot}%{_sysconfdir}/cron.weekly/popcorn
# server files
install -D -m 0755 server/popcorn-server %{buildroot}%{_bindir}/popcorn-server
install -D -m 0644 server/index.html     %{buildroot}%{_datadir}/popcorn/index.html
install -D -m 0644 server/server.cfg     %{buildroot}%{_sysconfdir}/popcorn-server.cfg
# use absolute paths
sed -i "s/^CONFIG_FILE = .*$/CONFIG_FILE = '%{_sysconfdir}/popcorn-server.conf'" %{buildroot}%{_bindir}/popcorn-server
sed -i "s/^INDEX_FILE = .*$/INDEX_FILE = '%{_datadir}/popcorn/index.html'" %{buildroot}%{_bindir}/popcorn-server

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/popcorn
%config(noreplace) %{_sysconfdir}/popcorn.conf
%{_sysconfdir}/cron.weekly/popcorn

%files server
%defattr(-,root,root)
%doc README
%{_bindir}/popcorn-server
%config(noreplace) %{_sysconfdir}/popcorn-server.conf
%dir %{_datadir}/popcorn
%{_datadir}/popcorn/index.html

%changelog
