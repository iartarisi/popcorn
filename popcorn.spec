Name:          popcorn
Version:       0.1
Release:       0
Url:           http://en.opensuse.org/Popcorn
License:       X11/MIT
Group:         System/Packages
Summary:       Popularity Contest (for RPM)
Source0:       popcorn-client
Source1:       popcorn.conf
Source2:       popcorn.cron
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
BuildRequires: python rpm-python
Requires:      python

%description
Popularity Contest (for RPM)

%prep
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} .

%build

%install
install -D -m 0755 popcorn-client $RPM_BUILD_ROOT%{_bindir}/popcorn-client
install -D -m 0644 popcorn.conf   $RPM_BUILD_ROOT%{_sysconfdir}/popcorn.conf
install -D -m 0755 popcorn.cron   $RPM_BUILD_ROOT%{_sysconfdir}/cron.weekly/popcorn

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/popcorn-client
%{_sysconfdir}/popcorn.conf
%{_sysconfdir}/cron.weekly/popcorn
