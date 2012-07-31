Name: 		rlog
Summary: 	Runtime Logging for C++
Version: 	1.3.7
Release: 	3%{?dist}
License: 	LGPL
Group: 		Development/Libraries
Url: 		http://arg0.net/wiki/rlog
Source0: 	http://arg0.net/users/vgough/download/%{name}-%{version}.tgz
Source1:	http://arg0.net/users/vgough/download/%{name}-%{version}.tgz.asc
%ifarch i386
BuildRequires:	valgrind
%endif
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
RLog provides a flexible message logging facility for C++ programs and
libraries.  It is meant to be fast enough to leave in production code.

%package devel
Summary:	Runtime Logging for C++ - development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
BuildRequires:	doxygen tetex-latex

%description devel
Files needed for developing apps using rlog

%prep
%setup -q

%build
%configure \
	--disable-static \
%ifarch i386
	--enable-valgrind
%else
	--disable-valgrind
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}/%{_libdir}/*.la
%{__rm} -rf %{buildroot}/%{_docdir}/rlog

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/librlog.so.*
%doc README AUTHORS COPYING 

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/librlog.so
%doc docs/html docs/latex/refman.pdf

%changelog

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 1.3.7-3%{?dist}
- Rebuild for FC6

* Wed Mar 29 2006 Peter Lemenkov <lemenkov@newmail.ru> 1.3.7-2
- rebuild

* Sun Nov 13 2005 Peter Lemenkov <lemenkov@newmail.ru> 1.3.7-1
- Initial build for FC-Extras
- Release v1.3.7

* Mon Nov 8 2004 Valient Gough <vgough@pobox.com>
- Release v1.3.5
- Add initial attempt at Win32 support (due to help from Vadim Zeitlin)
- Fixes to build on Suse 9.2 (replaced old KDE based autoconf scripts)
- Add "info" channel, and rInfo() macro.
* Mon May 31 2004 Valient Gough <vgough@pobox.com>
- Release v1.3.4
- Portibility changes to allow rlog to build with older C++ compilers and on
  non-x86 computers.
- Add extra ERROR_FMT() macro which allows format string to be passed on Error
  construction.
- Add valgrind support to allow valgrind trace from any assert when running
  under valgrind.
- Update admin dir.
* Sat Mar 13 2004 Valient Gough <vgough@pobox.com>
- Release v1.3.1
- added pkg-config file librlog.pc
- changed license to LGPL
- added rAssertSilent macro
- fixes for special case checks of printf attribute
* Sat Feb 8 2004 Valient Gough <vgough@pobox.com>
- Release v1.3
