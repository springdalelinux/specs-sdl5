Summary: Compile-time libraries for the firewall toolkit
Name: fwtk-lib
Version: 2.0
Release: 1%{?dist}
License: TIS copyright
Group: System Environment/Daemons
Source: ftp://ftp.tis.com/pub/fwtk-2.0.tar.gz
BuildRoot: /var/tmp/fwtklib.root

%description
The Libraries and header files from the firewall toolkit.  Only needed on
the system where you compile things like snksu.

%prep
%setup -c fwtklib

cd fwtk
cp Makefile.config.linux Makefile.config

%build

cd fwtk
( cd lib; make )
( cd auth; make ../libauth.a )


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install fwtk/libfwall.a $RPM_BUILD_ROOT%{_libdir}/libfwall.a
# avoid conflicts w/ Sun's libauth
install fwtk/libauth.a  $RPM_BUILD_ROOT%{_libdir}/libfwauth.a
install fwtk/firewall.h $RPM_BUILD_ROOT%{_includedir}/firewall.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/lib*
%{_includedir}/firewall.h
