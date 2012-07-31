Summary: C++ Template Library providing array objects for Scientific Computing
Name: blitz++
Version: 0.9
Release: 1%{?dist}
URL: http://www.oonumerics.org/blitz/
Source: blitz-%{version}.tar.gz
License: GPL 
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
#Prereq: /sbin/install-info
Obsoletes: Blitz++
BuildRequires: gcc-c++

%description
Blitz++ is a C++ class library for scientific computing which provides performance on par with Fortran 77/90. It uses template techniques to achieve high performance. The current versions provide dense arrays and vectors, random number generators, and small vectors and matrices.

%prep
%setup -q -n blitz-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" %configure --with-cxx=g++
make lib

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
%makeinstall
gzip doc/blitz.ps
rm -rf $RPM_BUILD_ROOT/usr/share/doc/blitz*

# remove unpackaged files from the buildroot
##rm -f $RPM_BUILD_ROOT%{_infodir}/dir
##rm -rf $RPM_BUILD_ROOT%{_mandir}
##rm -rf $RPM_BUILD_ROOT%{_sysconfdir}
##rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#/sbin/install-info %{_infodir}/blitz.info.gz %{_infodir}/dir
#
#%preun
#if [ "$1" = 0 ]; then
#	/sbin/install-info --delete %{_infodir}/blitz.info.gz %{_infodir}/dir
#fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL README NEWS 
%doc TODO doc/blitz.ps.gz examples
%{_libdir}/*.a
%{_libdir}/*.la
%{_infodir}/blitz.info.gz
%dir %{_includedir}/blitz
%{_includedir}/blitz/*
%dir %{_includedir}/random
%{_includedir}/random/*
%{_libdir}/pkgconfig/bli*
%exclude %{_infodir}/dir

%changelog
* Tue Feb 22 2005 Josko Plazonic <plazonic@math.princeton.edu>
- new version, new os

* Mon Oct 20 2003 Josko Plazonic <plazonic@math.princeton.edu>
- first build
