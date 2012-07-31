Name:           glpk
Version:        4.20
Release:        2%{?dist}
Summary:        GNU Linear Programming Kit

Group:          System Environment/Libraries
License:        GPL
URL:            http://www.gnu.org/software/glpk/glpk.html
Source0:        ftp://ftp.gnu.org/gnu/glpk/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The GLPK (GNU Linear Programming Kit) package is intended for solving
large-scale linear programming (LP), mixed integer programming (MIP),
and other related problems. It is a set of routines written in ANSI C
and organized in the form of a callable library.

GLPK supports the GNU MathProg language, which is a subset of the AMPL
language.

The GLPK package includes the following main components:

 * Revised simplex method.
 * Primal-dual interior point method.
 * Branch-and-bound method.
 * Translator for GNU MathProg.
 * Application program interface (API).
 * Stand-alone LP/MIP solver. 


%package devel
Summary:        Development headers and files for GLPK
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The glpk-devel package contains libraries and headers for developing
applications which use GLPK (GNU Linear Programming Kit).


%package utils
Summary:        GLPK-related utilities and examples
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description utils
The glpk-utils package contains the standalone solver programs glpksol
and tspsol that use GLPK (GNU Linear Programming Kit).


%package static
Summary:        Static version of GLPK libraries
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
The glpk-static package contains the statically linkable version of
the GLPK (GNU Linear Programming Kit) libraries.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} libdir=$RPM_BUILD_ROOT%{_libdir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}/%name
## Clean up directories that are included in docs
make clean
rm -Rf examples/.deps examples/Makefile* doc/*.dvi doc/*.latex

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README doc
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README doc
%{_includedir}/glpk

%files utils
%defattr(-,root,root)
%doc COPYING examples
%{_bindir}/*

%files static
%defattr(-,root,root)
%{_libdir}/*.a
%exclude %{_libdir}/*.la


%changelog
* Thu Aug  9 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-2
- Add pre and postun scripts to run ldconfig.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-1
- New release.
- Split static libs into separate package.

* Thu Jun 28 2007 Quentin Spencer <qspencer@users.sf.net> 4.18-1
- New release.

* Wed Mar 28 2007 Quentin Spencer <qspencer@users.sf.net> 4.15-1
- New release. Shared libraries are now supported.

* Tue Dec 12 2006 Quentin Spencer <qspencer@users.sf.net> 4.13-1
- New release.

* Tue Aug 29 2006 Quentin Spencer <qspencer@users.sf.net> 4.11-2
- Rebuild for FC6.

* Tue Jul 25 2006 Quentin Spencer <qspencer@users.sf.net> 4.11-1
- New release.

* Fri May 12 2006 Quentin Spencer <qspencer@users.sf.net> 4.10-1
- New release.

* Tue Feb 14 2006 Quentin Spencer <qspencer@users.sf.net> 4.9-2
- Add dist tag

* Tue Feb 14 2006 Quentin Spencer <qspencer@users.sf.net> 4.9-1
- New release.

* Tue Aug 09 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-3
- Remove utils dependency on base package, since it doesn't exist until
  shared libraries are enabled.

* Tue Aug 09 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-2
- Add -fPIC to compile flags.

* Fri Jul 22 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-1
- First version.
