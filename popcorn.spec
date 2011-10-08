%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

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
BuildRequires:  python-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Popularity Contest (for RPM).

%package server
Summary:        Server for Popularity Contest (for RPM)
Requires:       redis
Requires:       python-redis
Requires:       python-Flask
Requires:       python-jinja2
BuildRequires:  python-devel

%description server
Server for Popularity Contest (for RPM).

%prep
%setup -q -c -n %{name}

%build
python setup.py build

%install
# client files
install -D -m 0755 popcorn-client %{buildroot}%{_bindir}/popcorn
install -D -m 0644 popcorn.conf   %{buildroot}%{_sysconfdir}/popcorn.conf
install -D -m 0755 popcorn.cron   %{buildroot}%{_sysconfdir}/cron.weekly/popcorn

# server files
python setup.py install --skip-build --root %{buildroot} --prefix=%{_prefix}
install -D -m 0755 server/popcorn-server      %{buildroot}%{_sbindir}/popcorn-server
install -D -m 0644 server/server.conf         %{buildroot}%{_sysconfdir}/popcorn-server.conf
install -D -m 0755 server/popcorn-server.init %{buildroot}%{_initddir}/popcorn-server
ln -s %{_initddir}/popcorn-server %{buildroot}%{_sbindir}/rcpopcorn-server

%clean
rm -rf %{buildroot}

%pre server
/usr/sbin/groupadd -r popcorn &>/dev/null || :
/usr/sbin/useradd -o -g popcorn -s /bin/false -r -c "User for Popcorn server" -d /var/lib/empty popcorn &>/dev/null || :

%post server
%fillup_and_insserv -y popcorn-server

%preun server
%stop_on_removal popcorn-server

%postun server
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
%{python_sitelib}/popcorn
%{python_sitelib}/%{name}-*.egg-info
%{_sbindir}/popcorn-server
%{_sbindir}/rcpopcorn-server
%{_initddir}/popcorn-server

%changelog
