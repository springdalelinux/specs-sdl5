Name:           glibmm24
Version:        2.12.10
Release:        1%{?dist}
Summary:        C++ interface for GTK2 (a GUI library for X)

Group:          System Environment/Libraries
License:        LGPL
URL:            http://gtkmm.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.12/glibmm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libsigc++20-devel >= 2.0.0
BuildRequires:  glib2-devel >= 2.9.0

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance
and a comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.

%package devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel
Requires:       libsigc++20-devel

%description devel
This package contains the static libraries and header files needed for
developing gtkmm applications.


%prep
%setup -q -n glibmm-%{version}


%build
%configure %{!?_with_static: --disable-static}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

# Fix documentation installation, put everything under gtk-doc
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/glibmm-2.4
%{__mv} ${RPM_BUILD_ROOT}%{_docdir}/glibmm-2.4/* $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/glibmm-2.4/


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README CHANGES
%{_libdir}/*.so.*


%files devel
%defattr(-, root, root, -)
%{_includedir}/glibmm-2.4
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_libdir}/glibmm-2.4
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%doc %{_datadir}/gtk-doc/html/glibmm-2.4


%changelog
* Tue Jul 10 2007 Denis Leroy <denis@poolshark.org> - 2.12.10-1
- Update to 2.12.10
- Put documentation under datadir/gtk-doc/html

* Mon Apr 30 2007 Denis Leroy <denis@poolshark.org> - 2.12.8-1
- Update to 2.12.8

* Sun Jan 28 2007 Denis Leroy <denis@poolshark.org> - 2.12.5-1
- Update to 2.12.5, added dist tag

* Wed Dec  6 2006 Denis Leroy <denis@poolshark.org> - 2.12.3-1
- Update to 2.12.3

* Mon Oct  2 2006 Denis Leroy <denis@poolshark.org> - 2.12.2-1
- Update to 2.12.2

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.12.0-2
- FE6 Rebuild

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.12.0-1
- Update to 2.12.0

* Sun Jun 25 2006 Denis Leroy <denis@poolshark.org> - 2.10.4-1
- Update to 2.10.4

* Sun May  7 2006 Denis Leroy <denis@poolshark.org> - 2.10.1-1
- Update to 2.10.1

* Mon Mar 20 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-1
- Update to 2.10.0, requires newer glib

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.8.4-1
- Update to 2.8.4
- Added optional macro to enable static libs

* Sat Dec 17 2005 Denis Leroy <denis@poolshark.org> - 2.8.3-1
- Update to 2.8.3

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.8.2-1
- Update to 2.8.2
- Disabled static libraries

* Mon Sep 19 2005 Denis Leroy <denis@poolshark.org> - 2.8.0-1
- Upgrade to 2.8.0
- Updated glib2 version dependency

* Fri Sep  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.6.1-2
- rebuild for gcc-c++-4.0.1-12
  result for GLIBMM_CXX_ALLOWS_STATIC_INLINE_NPOS check changed

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.6.1-1
- Update to version 2.6.1

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 17 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.5-1
- Upgrade to glibmm 2.4.5

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.4-0.fdr.1
- Upgrade to 2.4.4
- Moved docs to regular directory

* Fri Dec 6 2002 Gary Peck <gbpeck@sbcglobal.net> - 2.0.2-1
- Removed "--without docs" option and simplified the spec file since the
  documentation is included in the tarball now

* Thu Dec 5 2002 Walter H. van Holst <rpm-maintainer@fossiel.xs4all.nl> - 1.0.2
- Removed reference to patch
- Added the documentation files in %files

* Thu Oct 31 2002 Gary Peck <gbpeck@sbcglobal.net> - 2.0.0-gp1
- Update to 2.0.0

* Wed Oct 30 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.26-gp3
- Added "--without docs" option to disable DocBook generation

* Sat Oct 26 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.26-gp2
- Update to 1.3.26
- Spec file cleanups
- Removed examples from devel package
- Build html documentation (including a Makefile patch)

* Mon Oct 14 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.24-gp1
- Initial release of gtkmm2, using gtkmm spec file as base

