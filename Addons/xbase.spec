Name:		xbase
Summary: 	XBase compatible database library and tools
Version: 	2.0.0
Release: 	6%{?dist}
License: 	LGPLv2+ and GPLv2+
Group: 		Development/Libraries
URL:		http://linux.techass.com/projects/xdb/
Source0:	http://dl.sourceforge.net/xdb/%{name}-%{version}.tar.gz
Patch0:		xbase-2.0.0-fixconfig.patch
Patch1:		xbase-2.0.0-fixheader.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	doxygen

%description
XBase is an xbase (i.e. dBase, FoxPro, etc.) compatible C++ class library
originally by Gary Kunkel and others (see the AUTHORS file).

XBase is useful for accessing data in legacy dBase 3 and 4 database files as
well as a general light-weight database engine.  It includes support for
DBF (dBase version 3 and 4) data files, NDX and NTX indexes, and DBT
(dBase version 3 and 4).  It supports file and record locking under *nix
OS's.

%package devel
Summary: XBase development libraries and headers
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Headers and libraries for compiling programs that use the XBase library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --enable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc NEWS README TODO AUTHORS COPYING ChangeLog
%{_bindir}/checkndx
%{_bindir}/copydbf
%{_bindir}/dbfxtrct
%{_bindir}/deletall
%{_bindir}/dumphdr
%{_bindir}/dumprecs
%{_bindir}/packdbf
%{_bindir}/reindex
%{_bindir}/undelall
%{_bindir}/zap
%{_bindir}/dbfutil1
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%doc docs/html
%dir %{_includedir}/xbase
%{_includedir}/xbase/*
%{_bindir}/xbase-config
%{_libdir}/libxbase.a
%{_libdir}/libxbase.so

%changelog
* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-6
- rebuild

* Sun Jun  4 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-5
- fix header file

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-4
- bump for FC-5

* Sun Jul 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-3
- fix xbase-config --ld (bugzilla 162845)

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-2
- add BuildRequires: doxygen
- remove latex docs (html is fine)

* Thu Jun 16 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.0-1
- initial package for Fedora Extras
