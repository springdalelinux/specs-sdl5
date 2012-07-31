%define tivversion 5.4.0
%define tivrelease 0
Summary: Tivoli Storage Manager startup scripts
Name: TIVsm
Version: %{tivversion}
Release: %{tivrelease}.0%{?dist}
Group: Applications/Internet
Source0: tsmscheduler.init
License: GPL
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-root
# we require coreutils in hopes of fixing installation of
# TIVsm-API and TIVsm-BA, to see if it helps
Requires: TIVsm-API = %{tivversion}-%{tivrelease}, TIVsm-BA = %{tivversion}-%{tivrelease}
Requires: coreutils procps findutils
Requires: /sbin/chkconfig /sbin/service
BuildArch: noarch

%description
This rpm contains a simple startup script for IBM's
Tivoli Storage Manager backup scheduler client.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_initrddir}/tsmscheduler

%post
/sbin/chkconfig --add tsmscheduler
/sbin/service tsmscheduler condrestart >> /dev/null

%preun
if [ $1 = 0 ]; then
 /sbin/chkconfig --del tsmscheduler
 /sbin/service tsmscheduler stop >> /dev/null
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_initrddir}/tsmscheduler

%changelog
* Thu Apr 19 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
