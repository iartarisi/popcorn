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

%prep
%setup -q -n %{name}

%build

%install
install -D -m 0755 popcorn-client %{buildroot}%{_bindir}/popcorn
install -D -m 0644 popcorn.conf   %{buildroot}%{_sysconfdir}/popcorn.conf
install -D -m 0755 popcorn.cron   %{buildroot}%{_sysconfdir}/cron.weekly/popcorn

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/popcorn
%config(noreplace) %{_sysconfdir}/popcorn.conf
%{_sysconfdir}/cron.weekly/popcorn

%changelog
