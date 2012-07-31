Name:           gtkmm24
Version:        2.10.10
Release:        1%{?dist}

Summary:        C++ interface for GTK2 (a GUI library for X)

Group:          System Environment/Libraries
License:        LGPL
URL:            http://gtkmm.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gtkmm/2.10/gtkmm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glibmm24-devel >= 2.12.8
BuildRequires:  atk-devel >= 1.9.0
BuildRequires:  pango-devel >= 1.5.2
BuildRequires:  gtk2-devel >= 2.10.0
BuildRequires:  glib2-devel >= 2.8.0
BuildRequires:  cairomm-devel >= 1.1.12


%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance
and a comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.


%package        devel
Summary:        Headers for developing programs that will use %{name}.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel
Requires:       glib2-devel
Requires:       glibmm24-devel
Requires:       atk-devel
Requires:       pango-devel
Requires:       cairomm-devel


%description devel
This package contains the static libraries and header files needed for
developing gtkmm applications.


%package        docs
Summary:        Documentation for %{name}, includes full API docs
Group:          Documentation
Requires:       %{name}-devel = %{version}-%{release}


%description    docs
This package contains the full API documentation for %{name}.


%prep
%setup -q -n gtkmm-%{version}


%build
%configure %{!?_with_static: --disable-static} --enable-shared --disable-examples --disable-demos
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

# Fix documentation installation, put everything under gtk-doc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/gtk-doc/html/gtkmm-2.4
mv ${RPM_BUILD_ROOT}%{_docdir}/gtkmm-2.4/* ${RPM_BUILD_ROOT}%{_datadir}/gtk-doc/html/gtkmm-2.4/
mv ${RPM_BUILD_ROOT}%{_datadir}/devhelp/books/gtkmm-2.4/*.devhelp ${RPM_BUILD_ROOT}%{_datadir}/gtk-doc/html/gtkmm-2.4
sed -i 's:../../../doc/gtkmm-2.4/docs/:docs/:' ${RPM_BUILD_ROOT}%{_datadir}/gtk-doc/html/gtkmm-2.4/*.devhelp
rm -r ${RPM_BUILD_ROOT}%{_docdir}/gtkmm-2.4


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*


%files devel
%defattr(-, root, root, -)
%doc CHANGES PORTING
%{_includedir}/gtkmm-2.4
%{_includedir}/atkmm-1.6
%{_includedir}/gdkmm-2.4
%{_includedir}/pangomm-1.4
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_libdir}/gtkmm-2.4
%{_libdir}/gdkmm-2.4
%{_libdir}/pkgconfig/*.pc


%files docs
%defattr(-, root, root, -)
%doc %{_datadir}/gtk-doc/html/gtkmm-2.4


%changelog
* Tue Jul 10 2007 Denis Leroy <denis@poolshark.org> - 2.10.10-1
- Update to 2.10.10, memory leak fix
- Fixed documentation devhelp support

* Mon Apr 30 2007 Denis Leroy <denis@poolshark.org> - 2.10.9-1
- Update to 2.10.9

* Sun Jan 28 2007 Denis Leroy <denis@poolshark.org> - 2.10.7-1
- Update to 2.10.7, fixed Source url path

* Wed Dec  6 2006 Denis Leroy <denis@poolshark.org> - 2.10.5-1
- Update to 2.10.5, addresses bug 218564

* Tue Oct  3 2006 Denis Leroy <denis@poolshark.org> - 2.10.2-1
- Update to 2.10.2

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-3
- FE6 Rebuild

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-2
- Added cairomm Require in devel 

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-1
- Update to 2.10.0. Now depends on cairomm

* Sun Jun 25 2006 Denis Leroy <denis@poolshark.org> - 2.8.8-2
- Added dist postfix to release version

* Sun Jun 25 2006 Denis Leroy <denisleroy@yahoo.com> - 2.8.8-1
- Update to 2.8.8

* Sun May  7 2006 Denis Leroy <denis@poolshark.org> - 2.8.5-1
- Update to 2.8.5

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.8.3-1
- Update to version 2.8.3
- Added optional macro to compile static libs

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.8.1-1
- Update to gtkmm 2.8.1
- Disabled static libraries build

* Mon Sep 19 2005 Denis Leroy <denis@poolshark.org> - 2.8.0-1
- Update to gtkmm 2.8.0
- Incorporated dependency updates from Rick Vinyard

* Fri Apr 29 2005 Denis Leroy <denis@poolshark.org> - 2.6.2-2
- Disabled building of demo and examples

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.6.2-1
- Update to gtkmm 2.6.2
- Added demo binary to devel package

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jan 15 2005 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0:2.4.8-1
- Update for gtkmm 2.4.8

* Wed Nov 17 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.7-1
- Update for gtkmm 2.4.7

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.5-0.fdr.1
- Upgrade to 2.4.5

* Thu Oct 8 2003 Michael Koziarski <michael@koziarski.org> - 0:2.2.8-0.fdr.3
- Incorporated more of Michael Schwendt's Comments in fedora bug 727
- Seperate -docs package with devhelp support disabled.

* Tue Oct 7 2003 Michael Koziarski <michael@koziarski.org> - 0:2.2.8-0.fdr.2
- Split the documentation into a separate -docs package
- Included devhelp

* Sat Oct 4 2003 Michael Koziarski <michael@koziarski.org> - 0:2.2.8-0.fdr.1
- Incorporated Michael Schwendt's Comments in fedora bug 727
- Updated to 2.2.8

* Tue Sep 16 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.2.7-0.fdr.1
- Initial Fedora Release.
- Updated to 2.2.7.

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
