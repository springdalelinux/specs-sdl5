Name:		libmcrypt
Version:	2.5.7
Release:	5%{?dist}
License:	LGPL
Group:		System Environment/Libraries
Summary:	Encryption algorithms library
URL:		http://mcrypt.sourceforge.net/
Source0:	http://download.sourceforge.net/mcrypt/libmcrypt-%{version}.tar.gz
Patch0:		libmcrypt-2.5.7-nolibltdl.patch
Patch1:		libmcrypt-2.5.7-aclocal_underquoted.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool-ltdl-devel

%description
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

%package devel
Group:		Development/Libraries
Summary:	Development libraries and headers for libmcrypt
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries and headers for use in building applications that
use libmcrypt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --enable-static=yes
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB ChangeLog KNOWN-BUGS README NEWS THANKS TODO
%{_libdir}/*.so.*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root,-)
%doc doc/README.key doc/README.xtea doc/example.c
%{_bindir}/libmcrypt-config
%{_includedir}/mcrypt.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/aclocal/libmcrypt.m4

%changelog
* Sun Oct  8 2006 Ed Hill <ed@eh3.com> 2.5.7-5
- bz 209913 : libmcrypt.m4 in -devel and properly quote it

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-4
- bump for FC-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-3
- bump for FC-5

* Wed Sep 28 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-2
- fix for FC-3

* Thu Sep 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-1
- initial package for Fedora Extras
