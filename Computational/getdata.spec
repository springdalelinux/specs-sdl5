%define __python /usr/bin/python26

Name:           getdata
Version:        0.7.3
Release:        1%{?dist}
Summary:        Library for reading and writing dirfile data

Group:          Development/Libraries
License:        GPLv2+
URL:            http://getdata.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

BuildRequires:     gcc-gfortran python26-devel numpy26 libtool-ltdl-devel
BuildRequires:     bzip2-devel zlib-devel xz-devel
%ifarch %{ix86} x86_64
#slim is only available on ix86 and x86_64
BuildRequires:     slimdata-devel
%endif

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description
The GetData Project is the reference implementation of the Dirfile Standards, a
filesystem-based database format for time-ordered binary data. The Dirfile
database format is designed to provide a fast, simple format for storing and
reading data. 

%package devel
Group:  Development/Libraries
Summary: Headers required when building programs against getdata
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gcc-gfortran%{_isa}

%description devel
Headers required when building a program against the GetData library.
Includes C++ and FORTRAN (77 & 95) bindings. 

%package fortran
Group:  Development/Libraries
Summary: getdata bindings for fortran
Requires: %{name} = %{version}-%{release}

%description fortran
The GetData library for fortran programs.  

%package python
Group: Development/Libraries
Summary: getdata bindings for the python language
Requires: %{name} = %{version}-%{release}
Requires: numpy26

%description python
Bindings to the getdata library for the python lanuguage.
Uses (and requires) the numpy python library for large numeric arrays. 

%package gzip
Group:  Development/Libraries
Summary: Enables getdata read ability of gzip compressed dirfiles
Requires: %{name} = %{version}-%{release}

%description gzip
Enables getdata to read dirfiles that are encoded (compressed) with gzip.
Fields must be fully compressed with gzip, not actively being written to.
Does not yet allow writing of gzip encoded dirfiles.  

%package bzip2
Group:  Development/Libraries
Summary: Enables getdata read ability of bzip2 compressed dirfiles
Requires: %{name} = %{version}-%{release}

%description bzip2
Enables getdata to read dirfiles that are encoded (compressed) with bzip2.
Fields must be fully compressed with bzip2, not actively being written to.
Does not yet allow writing of bzip2 encoded dirfiles.

%ifarch %{ix86} x86_64 #slim is only available on for these.
%package slim
Group:  Development/Libraries
Summary: Enables getdata read ability of slim compressed dirfiles
Requires: %{name} = %{version}-%{release}

%description slim
Enables getdata to read dirfiles that are encoded (compressed) with slimdata.
%endif

%package lzma
Group:  Development/Libraries
Summary: Enables getdata read ability of lzma compressed dirfiles
Requires: %{name} = %{version}-%{release}

%description lzma
Enables getdata to read dirfiles that are encoded (compressed) with lzma.

%prep
%setup -q

%build
# FIXME: FFLAGS/FCFLAGS are not being honored; looking into it with upstream.
%configure --disable-static --enable-modules --with-python=%{__python}
make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} SUID_ROOT="" install
# Remove .la files.  
rm -f %{buildroot}/%{_libdir}/lib*.la
rm -f %{buildroot}/%{_libdir}/getdata/lib*.la
rm -f %{buildroot}/%{python_sitearch}/*.la
# Remove simple docs, as we install them ourselves (along with others)
rm -f %{buildroot}/%{_datadir}/doc/%{name}/*
# Place fortran module in the correct location
#mkdir -p %{buildroot}/%{_fmoddir}
#mv %{buildroot}/%{_includedir}/getdata.mod  %{buildroot}/%{_fmoddir}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING AUTHORS TODO ChangeLog
%{_bindir}/dirfile2ascii
%{_bindir}/checkdirfile
%{_libdir}/libgetdata*.so.*
%dir %{_libdir}/getdata
%{_mandir}/man5/*
%{_mandir}/man1/*

%files python
%defattr(-,root,root,-)
%{python_sitearch}/*.so

%files fortran
%defattr(-,root,root,-)
%{_libdir}/libf*getdata.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/README.cxx doc/README.f77 doc/unclean_database_recovery.txt doc/README.python
%{_libdir}/libgetdata.so
%{_libdir}/libf*getdata.so
%{_libdir}/libgetdata++.so
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/getdata.pc
#{_fmoddir}/getdata.mod

%files gzip
%defattr(-,root,root,-)
%{_libdir}/getdata/libgetdatagzip*.so

%files bzip2
%defattr(-,root,root,-)
%{_libdir}/getdata/libgetdatabzip2*.so

%ifarch %{ix86} x86_64
%files slim
%defattr(-,root,root,-)
%{_libdir}/getdata/libgetdataslim*.so
%endif

%files lzma
%defattr(-,root,root,-)
%{_libdir}/getdata/libgetdatalzma*.so

%changelog
* Thu Apr 7 2011 Matthew Truch <matt at truch.net> - 0.7.3-0
- Upstream 0.7.3.  Several bugfixes.  

* Thu Feb 17 2011 Matthew Truch <matt at truch.net> - 0.7.1-0
- Upstream 0.7.1 release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 5 2010 Matthew Truch <matt at truch.net> - 0.6.3-1
- Upstream 0.6.3.

* Tue Feb 16 2010 Matthew Truch <matt at truch.net> - 0.6.2-1
- Upstream 0.6.2.  Fixes serious memory corruption bug in legacy API.

* Fri Feb 12 2010 Matthew Truch <matt at truch.net> - 0.6.1-2
- Bump for no reason.

* Fri Feb 12 2010 Matthew Truch <matt at truch.net> - 0.6.1-1
- Upstream 0.6.1.

* Wed Feb 10 2010 Matthew Truch <matt at truch.net> - 0.6.1-0rc2.1
- Upstream -rc2 which includes upstreamed patches to fix build and test issues.

* Sun Feb 7 2010 Matthew Truch <matt at truch.net> - 0.6.1-0rc1.2
- Include missing files in buildsys.

* Wed Feb 3 2010 Matthew Truch <matt at truch.net> - 0.6.1-0rc1
- Upstream 0.6.1rc1
-  Fixes minor bugs.
-  Fixes build issues with recent gcc discovered with Fedora buildsystem.

* Sat Jan 30 2010 Matthew Truch <matt at truch.net> - 0.6.0-2
- Use proper URL for Source0 at sourceforge.

* Tue Nov 3 2009 Matthew Truch <matt at truch.net> - 0.6.0-1
- Upstream 0.6.0 release.
- Split fortran dependancy into a sub-package.

* Mon Nov 2 2009 Matthew Truch <matt at truch.net> - 0.6.0-0rc4
- Upstream 0.6.0 release candidate 4.
- Include new numpy support in python bindings.
- Put python bindings in their own sub-package.

* Mon Oct 19 2009 Matthew Truch <matt at truch.net> - 0.6.0-0rc3
- Upstream 0.6.0 release candidate 3.
- Properly deal with slim's limited arch availability.

* Wed Oct 14 2009 Matthew Truch <matt at truch.net> - 0.6.0-0rc2
- Upstream 0.6.0 release candidate 2.
- Remove patch which is included in upstream release.
- Activate python bindings.
- Enable slimdata and lzma encoded dirfile read ability.

* Mon Sep 21 2009 Matthew Truch <matt at truch.net> - 0.5.0-5
- Include bugfix from upstream.
- Put fortran module in correct place. BZ 523539

* Mon Jul 27 2009 Matthew Truch <matt at truch.net> - 0.5.0-4
- Disable verbose debugging output.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Matthew Truch <matt at truch.net> - 0.5.0-2
- Bump for mass rebuild.

* Fri Jan 16 2009 Matthew Truch <matt at truch.net> - 0.5.0-1
- Upstream 0.5.0
-   Includes bugfixes.
-   New gzip and bzip2 encoded dirfile read ability.
-   Uses ltdl dynamic module loading for gzip and bzip2 modules.

* Tue Nov 18 2008 Matthew Truch <matt at truch.net> - 0.4.2-1
- Upstream 0.4.2.
-   Includes several bugfixes, especially to the legacy interface.

* Sat Nov 1 2008 Matthew Truch <matt at truch.net> - 0.4.0-1
- Upstream 0.4.0.

* Thu Oct 16 2008 Matthew Truch <matt at truch.net> - 0.3.1-2
- Remove mention of static libs in description
- Include TODO in doc.  
- Cleanup man-pages file glob.
- Include signature.

* Wed Sep 24 2008 Matthew Truch <matt at truch.net> - 0.3.1-1
- Upstream 0.3.1.
-   Includes former c++ compile fix patch
-   Includes bug fixes to legacy API.

* Fri Sep 19 2008 Matthew Truch <matt at truch.net> - 0.3.0-1
- Initial Fedora build.

