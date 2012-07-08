# -*- coding: utf-8 -*-
# Copyright (c) 2012 Akshit Khurana <axitkhurana@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

Name:      popcorn
Version:   0.1
Release:   0
Summary:   Client for opensuse popcorn project
License:   MIT
Url:       http://github.com/opensuse/popcorn
Group:     System/Packages
Source:    %{name}.tar.gz
Requires:  cron, python, rpm-python
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch

%description
Popcorn tracks the collection of packages and repositories that users have installed on their systems in a central place.

%prep
%setup -q -c -n %{name}

%build

%install
install -Dm755 popcorn-client %{buildroot}%{_bindir}/popcorn
install -Dm644 popcorn.conf   %{buildroot}%{_sysconfdir}/popcorn.conf
install -Dm755 popcorn.cron   %{buildroot}%{_sysconfdir}/cron.monthly/popcorn
install -Dm644 popcorn.log %{buildroot}%{_localstatedir}/log/popcorn.log

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README LICENSE
%{_bindir}/popcorn
%{_sysconfdir}/popcorn.conf
%config(noreplace) %{_sysconfdir}/cron.monthly/popcorn
%{_localstatedir}/log/popcorn.log

%changelog
