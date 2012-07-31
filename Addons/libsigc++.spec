Name:           libsigc++20
Version:        2.0.18
Release:        1%{?dist}

Summary:        Typesafe signal framework for C++
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://libsigc.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.0/libsigc++-%version.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  m4

%description
This library implements a full callback system for use in widget libraries,
abstract interfaces, and general programming. Originally part of the Gtk--
widget set, %name is now a separate library to provide for more general
use. It is the most complete library of its kind with the ability to connect
an abstract callback to a class method, function, or function object. It
contains adapter classes for connection of dissimilar callbacks and has an
ease of use unmatched by other C++ callback libraries.

Package GTK-- (gtkmm), which is a C++ binding to the GTK+ library,
starting with version 1.1.2, uses %name.


%package devel
Summary:        Development tools for the typesafe signal framework for C++
Group:          Development/Libraries
Requires:       %name = %{version}-%{release}
Requires:       pkgconfig


%description devel
The %name-devel package contains the static libraries and header files
needed for development with %name.


%prep
%setup -q -n libsigc++-%{version}


%build
%configure %{!?_with_static: --disable-static}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT docs-to-include
make DESTDIR=${RPM_BUILD_ROOT} install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
%{__mkdir} docs-to-include
%{__mv} ${RPM_BUILD_ROOT}%{_docdir}/libsigc-2.0/* docs-to-include/


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS ChangeLog TODO
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%doc docs-to-include/*
%{_includedir}/*
%{_libdir}/sigc++-2.0
%{_libdir}/pkgconfig/*.pc
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so


%changelog
* Thu Dec 13 2007 Denis Leroy <denis@poolshark.org> - 2.0.18-1
- Update to 2.0.18
- Spec cleanup

* Tue Jul 10 2007 Denis Leroy <denis@poolshark.org> - 2.0.17-3
- Added dist tag

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.0.17-2
- FE6 Rebuild

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.0.17-1
- Upgrade to version 2.0.17
- Added optional macro to compile static libs (use '--with static')

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.0.16-2
- Disabled static libraries
- Was missing copy of GPL licence

* Sun Sep 18 2005 Denis Leroy <denis@poolshark.org> - 2.0.16-1
- Upgrade to version 2.0.16

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.0.11-1
- Upgrade to version 2.0.11

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jan 15 2005 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0:2.0.6-1
- Update to 2.0.6

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.0.3-0.fdr.1
- Update to 2.0.3
- Merged deps from FC2 sigc++ 1.2.5 spec
- Moved docs to regular directory

* Sat Apr 15 2000 Dmitry V. Levin <ldv@fandra.org>
- updated Url and Source fileds
- 1.0.0 stable release

* Sat Jan 22 2000 Dmitry V. Levin <ldv@fandra.org>
- filtering out -fno-rtti and -fno-exceptions options from $RPM_OPT_FLAGS
- minor install section cleanup

* Wed Jan 19 2000 Allan Rae <rae@lyx.org>
- autogen just creates configure, not runs it, so cleaned that up too.

* Wed Jan 19 2000 Dmitry V. Levin <ldv@fandra.org>
- minor attr fix
- removed unnecessary curly braces
- fixed Herbert's adjustement

* Sat Jan 15 2000 Dmitry V. Levin <ldv@fandra.org>
- minor package dependence fix

* Sat Dec 25 1999 Herbert Valerio Riedel <hvr@gnu.org>
- fixed typo of mine
- added traditional CUSTOM_RELEASE stuff
- added SMP support

* Thu Dec 23 1999 Herbert Valerio Riedel <hvr@gnu.org>
- adjusted spec file to get tests.Makefile and examples.Makefile from scripts/

* Fri Oct 22 1999 Dmitry V. Levin <ldv@fandra.org>
- split into three packages: %name, %name-devel and %name-examples

* Thu Aug 12 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- updated source field and merged conflicts between revisions.

* Tue Aug 10 1999 Dmitry V. Levin <ldv@fandra.org>
- updated Prefix and BuildRoot fields

* Thu Aug  5 1999 Herbert Valerio Riedel <hvr@hvrlab.dhs.org>
- made sure configure works on all alphas

* Wed Jul  7 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- Added autoconf macro for sigc.

* Fri Jun 11 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- Made into a .in to keep version field up to date
- Still need to do release by hand

* Mon Jun  7 1999 Dmitry V. Levin <ldv@fandra.org>
- added Vendor and Packager fields

* Sat Jun  5 1999 Dmitry V. Levin <ldv@fandra.org>
- updated to 0.8.0

* Tue Jun  1 1999 Dmitry V. Levin <ldv@fandra.org>
- initial revision
