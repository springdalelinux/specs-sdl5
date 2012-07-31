%define	snap	20060603

Name:           libedit
Version:        2.9
Release:        4.%{snap}cvs%{?dist}
Summary:        The NetBSD Editline library (libedit)

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.thrysoee.dk/editline/
Source0:        http://www.thrysoee.dk/editline/%{name}-%{snap}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel 

%description
This is an autotool- and libtoolized port of the NetBSD Editline
library (libedit). This Berkeley-style licensed command line
editor library provides generic line editing, history, and
tokenization functions, similar to those found in GNU Readline.

%package	devel
Summary:	Development files for %{name}
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ncurses-devel

%description	devel
This is an autotool- and libtoolized port of the NetBSD Editline
library (libedit). This Berkeley-style licensed command line
editor library provides generic line editing, history, and
tokenization functions, similar to those found in GNU Readline.

This package contains development files for %{name}.

%prep
%setup -q -n %{name}-%{snap}-%{version}

%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog INSTALL THANKS COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 2.9-3.20060603cvs
- Rebuild for FC6

* Thu Jun 29 2006 Michael J. Knox <michael@knox.net.nz> - 2.9-3.20060603cvs
- updated to current snapshot
- fixed incoherent-version-in-changelog rpmlint messages

* Thu Mar 23 2006 Michael J Knox <michael@knox.net.nz> - 2.9-2.20060213cvs
- removed licence file I supplied, have requested upstream to provide one
- removed unrequire build dep

* Tue Mar 14 2006 Michael J Knox <michael@knox.net.nz> - 2.9-1.20060213cvs
- removed .la
- added post and postun calls.
- fixed package groups and release.
- added %{name}.COPYING to include NetBSD BSD license.

* Tue Feb 14 2006 Michael J Knox <michael@knox.net.nz> - 2.9-20060103cvs
- initial package for NetBSD's editline.
