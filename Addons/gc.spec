
Summary: C++ Garbage Collector	
Name:    gc	
Version: 6.8

Release: 3%{?dist}
Group:   System Environment/Libraries
License: BSD
Url:     http://www.hpl.hp.com/personal/Hans_Boehm/gc/	
Source:  http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# force no undefined symbols (#166344)
Patch1: gc-6.7-no-undefined.patch

BuildRequires: libtool
BuildRequires: automake 

Obsoletes: libgc < %{version}-%{release}
Provides:  libgc = %{version}-%{release}


%description
The Boehm-Demers-Weiser conservative garbage collector can be used as a garbage 
collecting replacement for C malloc or C++ new.

%package devel
Summary: Libraries and header files for %{name} development 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: libgc-devel < %{version}-%{release}
Provides:  libgc-devel = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q -n %{name}%{version}

%patch1 -p1 -b .no-undefined

cp -f %{_datadir}/aclocal/libtool.m4 .
libtoolize --copy --force
%if 1
autoreconf
%else
aclocal
automake
autoconf
#autoheader
%endif


%build

%configure \
  --disable-dependency-tracking \
  --disable-static \
  --enable-cplusplus \
  --enable-threads=posix \
%ifarch %{ix86}
  --enable-parallel-mark
%endif

make %{?_smp_mflags}


%check || :
make check


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT 

install -p -D -m644 doc/gc.man	$RPM_BUILD_ROOT%{_mandir}/man3/gc.3

## Unpackaged files
rm -rf $RPM_BUILD_ROOT%{_datadir}/gc
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc doc/README doc/README.changes doc/README.contributors 
%doc doc/README.environment doc/README.linux
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.html
%{_includedir}/*
%{_libdir}/lib*.so
%{_mandir}/man?/*


%changelog
* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-3
- Obsoletes/Provides: libgc(-devel) (rpmforge compatibility)

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-2
- fc6 respin

* Thu Jul 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-1
- 6.8

* Fri Mar 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.7-1
- 6.7

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-5
- gcc(4.1) patch 

* Thu Dec 01 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-4
- Provides: libgc(-devel)

* Wed Sep 14 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-3
- no-undefined patch, libtool madness (#166344)

* Mon Sep 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-2
- drop opendl patch (doesn't appear to be needed anymore)

* Fri Sep 09 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-1
- 6.6

* Wed May 25 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.5-1
- 6.5

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:6.4-2
- --enable-threads unconditionally
- --enable-parallel-mark only on %%ix86 (#144681)

* Mon Jan 10 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:6.4-1
- 6.4
- update opendl patch

* Fri Jul 09 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.1
- 6.3(final)

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.4.alpha6
- dlopen patch

* Wed May 26 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.3.alpha6
- explictly --enable-threads ('n friends)

* Tue May 25 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.2.alpha6
- 6.3alpha6
- --disable-static
- --enable-parallel-mark

* Wed Dec 17 2003 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.1.alpha2
- 6.3alpha2

* Thu Oct 02 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.3
- OK, put manpage in man3.

* Thu Oct 02 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.2
- drop manpage pending feedback from developer. 

* Tue Sep 30 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.1
- fix manpage location 
- remove .la file (it appears unnecessary after all, thanks to opendl patch)
- remove cvs tag from description
- touchup -devel desc/summary.
- macro update to support Fedora Core

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.0 
- 6.2 release.
- update license (BSD)
- Consider building with: --enable-parallel-mark
  (for now, no).

