Summary: POSIX regexp functions
Name: librx
Version: 1.5
Release: 8%{?dist}
License: GPL
URL: http://www.gnu.org/software/rx/rx.html
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/rx/rx-%{version}.tar.bz2
Patch0: rx-1.5-shared.patch
Patch1: rx-1.5-texinfo.patch
Patch2: librx-1.5-libdir64.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: texinfo, libtool

%description
Rx is, among other things, an implementation of the interface
specified by POSIX for programming with regular expressions.  Some
other implementations are GNU regex.c and Henry Spencer's regex
library.

%package devel
Summary: POSIX regexp functions, developers library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Rx is, among other things, an implementation of the interface
specified by POSIX for programming with regular expressions.  Some
other implementations are GNU regex.c and Henry Spencer's regex
library.

This package contains files needed for development with librx.

%prep
%setup -q -n rx-%{version}
%patch0 -p1
%patch1 -p1 -b .texipatch
%ifarch x86_64 ppc64 sparc64
%patch2 -p1 -b .64bit
%endif

%build
%configure
make %{?_smp_mflags}
make doc/rx.info

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
make install DESTDIR=${RPM_BUILD_ROOT}
install -m 644 doc/rx.info ${RPM_BUILD_ROOT}%{_infodir}
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/librx.la
chmod -x ${RPM_BUILD_ROOT}%{_includedir}/rxposix.h

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/rx.info \ 
    %{_infodir}/dir 2>/dev/null || :

%postun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/rx.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc ANNOUNCE BUILDING COOKOFF rx/ChangeLog
%{_includedir}/*
%{_infodir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-8
- fix bz 200090

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-7
- fix bz 197717
- bump for FC-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-6
- bump for FC-5

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-5
- remove hardcoded dist tags

* Sun May  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-4
- Fix 64 bit arches to install to the right libdir

* Thu May  5 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-3
- add BuildRequires: texinfo

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-2
- use dist tag

* Sat Apr 23 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-1
- new package, based on Alexey Voinov's package from AltLinux
