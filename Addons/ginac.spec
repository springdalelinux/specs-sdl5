Name:           ginac
Version:        1.3.6
Release:        1%{?dist}
Summary:        C++ library for symbolic calculations

Group:          System Environment/Libraries
License:        GPL
URL:            http://www.ginac.de/
Source0:        http://www.ginac.de/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires:  cln-devel >= 1.1 gcc-c++ readline-devel
BuildRequires:  tetex-latex tetex-dvips doxygen transfig
Obsoletes:      GiNaC < 1.3.2
Provides:       GiNaC = %{version}-%{release}

%description
GiNaC (which stands for "GiNaC is Not a CAS (Computer Algebra System)") is an
open framework for symbolic computation within the C++ programming language.


%package devel
Summary: GiNaC development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} cln-devel
Obsoletes: GiNaC-devel < 1.3.2
Provides:  GiNaC-devel = %{version}-%{release}

%description devel
GiNaC (which stands for "GiNaC is Not a CAS (Computer Algebra System)") is an
open framework for symbolic computation within the C++ programming language.

This package contains the libraries, include files and other resources you
use to develop GiNaC applications.


%package utils
Summary: GiNaC-related utilities
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: GiNaC-utils < 1.3.2
Provides:  GiNaC-utils = %{version}-%{release}

%description utils
GiNaC (which stands for "GiNaC is Not a CAS (Computer Algebra System)") is an
open framework for symbolic computation within the C++ programming language.

This package includes ginsh ("GiNaC interactive shell") which provides a
simple and easy-to-use CAS-like interface to GiNaC for non-programmers, and
the tool "viewgar" which displays the contents of GiNaC archives.


%prep
%setup -q

%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/ginac.info.gz 2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/ginac.info.gz 2>/dev/null || :
fi


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_infodir}/*.info*
%{_mandir}/man?/ginac-config.1*
%{_libdir}/*.so
%{_libdir}/pkgconfig/ginac.pc
%{_includedir}/ginac
%{_bindir}/ginac-config
%{_datadir}/aclocal/ginac.m4
%exclude %{_libdir}/*.la

%files utils
%defattr(-,root,root)
%{_bindir}/ginsh
%{_bindir}/viewgar
%{_mandir}/man?/ginsh.1*
%{_mandir}/man?/viewgar.1*

%changelog
* Wed Jan 10 2007 Quentin Spencer <qspencer@users.sf.net> 1.3.6-1
- New release.

* Mon Aug 28 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.5-1
- New release.

* Fri Apr 14 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.4-1
- New release. Old patch removed.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.3-4
- Rebuild for Fedora Extras 5.

* Thu Feb  2 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.3-3
- Patch so it builds on gcc 4.1.
- Disable static libs from build and enable parallel build.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 1.3.3-2
- Exclude /usr/share/info/dir from package.
- New URL.
- Exclude static libs.

* Mon Oct 31 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.3-1
- New upstream release.

* Tue Aug  2 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.2-1
- New upstream release. Changed package name to lowercase letters to
  mirror upstream sources.  Added Provides and Obsoletes for upgrade.

* Sat Jun 11 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-5
- Added cln-devel as dependency of GiNaC-devel

* Fri May 27 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-5
- Removed gmp-devel--it should be in cln-devel instead

* Fri May 27 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-4
- Added gmp-devel to BuildRequires

* Thu May 26 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-3
- Added transfig to BuildRequires

* Thu May 26 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-2
- Added dist tag

* Wed May 18 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.1-1
- New upstream release.
- Added missing BuildRequires (readline-devel, tetex-*, doxygen).

* Wed May 11 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.0-2
- Exclude .la lib.
- Remove processing of info files (this is supposed to be automatic).

* Fri Apr 22 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.0-2
- Added release to Requires for devel and utils

* Thu Apr 21 2005 Quentin Spencer <qspencer@users.sf.net> 1.3.0-1
- Adapted spec file for Fedora Extras
- Fixed missing BuildRequires
- Fixed broken install-info command

* Thu Nov 20 2003 Christian Bauer <Christian.Bauer@uni-mainz.de>
- added pkg-config metadata file to devel package

* Thu Nov  1 2001 Christian Bauer <Christian.Bauer@uni-mainz.de>
- moved ginsh and viewgar to "utils" package

* Thu Oct  5 2000 Christian Bauer <Christian.Bauer@uni-mainz.de>
- cleaned up a bit

* Wed Jan 26 2000 Christian Bauer <Christian.Bauer@uni-mainz.de>
- split into user and devel packages

* Wed Dec  1 1999 Christian Bauer <Christian.Bauer@uni-mainz.de>
- aclocal macros get installed
