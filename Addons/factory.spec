
Summary: C++ class library for multivariate polynomial data
Name:    factory
Version: 2.0.5
Release: 10%{?dist}

License: GPL
URL:	 http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Factory/
Source:  http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Factory/factory-2-0-5.tar.gz
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: factory-2.0.5-gcc34.patch
Patch2: factory-64bit.patch
# See http://bugzilla.redhat.com/bugzilla/183258
Patch3: factory-2.0.5-gcc41.patch

BuildRequires: gmp-devel

%description
Factory is a C++ class library that implements a recursive representation
of multivariate polynomial data.


%package devel
Summary: C++ class library for multivariate polynomial data 
Group:   Development/Libraries
Requires: gmp-devel
%description devel
Factory is a C++ class library that implements a recursive representation
of multivariate polynomial data.


%prep
%setup -q -n %{name}

%patch1 -p1 -b .gcc34
%patch2 -p1 -b .64bit
%patch3 -p1 -b .gcc41


%build
# Macaulay2's build instructions say to use --disable-streamio
# *not* using --disable-streamio requires patching for gcc3+ anyway.
%configure --disable-streamio

# smp broken?
make


%install
rm -rf $RPM_BUILD_ROOT

# make install DESTDIR fails
%makeinstall


%clean
rm -rf $RPM_BUILD_ROOT


%files devel
%defattr(-,root,root)
%doc ChangeLog COPYING NEWS README NEWS
%{_libdir}/lib*.a
%{_includedir}/*


%changelog
* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-10
- respin

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-9
- fc6 respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-8
- fc6 respin

* Tue Mar 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-7
- factory-2.0.5-gcc41.patch (#183258)

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 2.0.5-6
- fix build on 64bit arches

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.0.5-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Oct 06 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-3
- (2nd try at) gcc34 patch

* Wed Oct 06 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-0.fdr.2
- gcc34 patch

* Fri Oct 1 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-0.fdr.1
- factory-2.0.5

* Mon Nov 17 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.4.b
- update macros

* Fri Nov 14 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.3.b
- document use of --disable-streamio

* Mon Oct 06 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.2.b
- remove smp build.

* Mon Oct 06 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.1.b
- -devel: Requires: gmp-devel
- remove extraneous cvs tags
- update macros for Fedora Core support

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.0.b
- first try.
- no shared libs, but make (only) -devel package to signify it's purpose

