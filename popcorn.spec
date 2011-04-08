Name:          popcorn
Version:       0.1
Release:       0
Url:           http://en.opensuse.org/Popcorn
License:       X11/MIT
Group:         System/Packages
Summary:       Popularity Contest (for RPM)
Source:        %{name}.tar.bz2
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
Requires:      rpm-python cron

%description
Popularity Contest (for RPM)

%package server
Group:         System/Packages
Summary:       Popularity Contest (for RPM) - server

%description server
Popularity Contest (for RPM) - server

%prep
%setup -q -n %{name}

%build

%install
# client
install -D -m 0755 popcorn-client $RPM_BUILD_ROOT%{_bindir}/popcorn
install -D -m 0644 popcorn.conf   $RPM_BUILD_ROOT%{_sysconfdir}/popcorn.conf
install -D -m 0755 popcorn.cron   $RPM_BUILD_ROOT%{_sysconfdir}/cron.weekly/popcorn
# server

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/popcorn
%config(noreplace) %{_sysconfdir}/popcorn.conf
%{_sysconfdir}/cron.weekly/popcorn

%files server
%defattr(-,root,root)

%changelog
