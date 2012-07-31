Summary: Allow su to root using a secure net key
Name: snksu
Version: 2.1
Release: 1%{?dist}
License: Distributable
Group: System Environment/Daemons
Source: snksu-2.1.tar.gz
BuildRequires: fwtk-lib

BuildRoot: /var/tmp/%{name}-root

%description
The snk program allows you to switch to root or to some other user
without typing passwords.  Instead, a challenge/response scheme base
on a Secure Net Key is used.

%prep
%setup -q -n snksu-2.1

%build
make
strip su

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
mkdir -p $RPM_BUILD_ROOT/usr/local/etc
cp su $RPM_BUILD_ROOT/usr/local/bin/snksu
cp netperm-table $RPM_BUILD_ROOT/usr/local/etc/netperm-table

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(4511,root,root) /usr/local/bin/snksu
%config /usr/local/etc/netperm-table

%changelog
