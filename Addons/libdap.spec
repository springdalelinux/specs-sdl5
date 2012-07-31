Name: libdap
Summary: The C++ DAP2 library from OPeNDAP
Version: 3.11.0
Release: 1%{?dist}

License: LGPLv2+
Group: Development/Libraries
URL: http://www.opendap.org/
Source0: http://www.opendap.org/pub/source/libdap-%{version}.tar.gz
#Don't run HTTP tests - builders don't have network connections
Patch2:  libdap-3.10.2-offline.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cppunit-devel
BuildRequires: curl-devel
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: e2fsprogs-devel
BuildRequires: libxml2-devel
BuildRequires: pkgconfig

# This package could be relocatable. In that case uncomment the following
# line
#Prefix: %{_prefix}


%description
The libdap++ library contains an implementation of DAP2. This package
contains the library, dap-config, and getdap. The script dap-config
simplifies using the library in other projects. The getdap utility is a
simple command-line tool to read from DAP2 servers. It is built using the
library and demonstrates simple uses of it.


%package devel
Summary: Development and header files from libdap
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: curl-devel
Requires: libxml2-devel
Requires: pkgconfig
# for the /usr/share/aclocal directory ownership
Requires: automake

%description devel
This package contains all the files needed to develop applications that
will use libdap.


%package doc
Summary: Documentation of the libdap library
Group: Documentation

%description doc
Documentation of the libdap library.


%prep
%setup -q
%patch2 -p1 -b .offline
iconv -f latin1 -t utf8 < COPYRIGHT_W3C > COPYRIGHT_W3C.utf8
touch -r COPYRIGHT_W3C COPYRIGHT_W3C.utf8
mv COPYRIGHT_W3C.utf8 COPYRIGHT_W3C


%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

make docs


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mv $RPM_BUILD_ROOT%{_bindir}/dap-config-pkgconfig $RPM_BUILD_ROOT%{_bindir}/dap-config

rm -rf __dist_docs
cp -pr docs __dist_docs
# those .map and .md5 are of dubious use, remove them
rm -f __dist_docs/html/*.map __dist_docs/html/*.md5
# use the ChangeLog timestamp to have the same timestamps for the doc files 
# for all arches
touch -r ChangeLog __dist_docs/html/*


%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/getdap
%{_libdir}/libdap.so.*
%{_libdir}/libdapclient.so.*
%{_libdir}/libdapserver.so.*
%doc README NEWS COPYING COPYRIGHT_URI README.dodsrc
%doc COPYRIGHT_W3C

%files devel
%defattr(-,root,root,-)
%{_libdir}/libdap.so
%{_libdir}/libdapclient.so
%{_libdir}/libdapserver.so
%{_libdir}/pkgconfig/libdap*.pc
%{_bindir}/dap-config
%{_includedir}/libdap/
%{_datadir}/aclocal/*

%files doc
%defattr(-,root,root,-)
%doc COPYING COPYRIGHT_URI COPYRIGHT_W3C
%doc __dist_docs/html/


%changelog
* Fri Dec 10 2010 Orion Poplawski <orion@cora.nwra.com> - 3.11.0-1
- Update to 3.11.0
- Drop libuuid patch fixed upstream
- Drop soname patch

* Thu Jul 15 2010 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-3
- Add patch to bump soname as this dropped the AIS* functions
- Add BR cppunit-devel and %%check section
- Add patch to not run HTTP network tests

* Wed Jul 14 2010 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-2
- Add patch to remove -luuid from pkg-config libs

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com> - 3.10.2-1
- Update to 3.10.2
- Deflate is no longer shipped
- Drop includes patch fixed upstream
- Add license to doc sub-package

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.9.3-1
- Update to 3.9.3

* Tue Mar  2 2009 Caolán McNamara <caolanm@redhat.com> - 3.8.2-3
- include cstdio for std::sprintf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Patrice Dumas <pertusus@free.fr> 3.8.2-1
- update to 3.8.2

* Sun Mar 16 2008 Patrice Dumas <pertusus@free.fr> 3.8.0-1
- update to 3.8.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.7.10-3
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Patrice Dumas <pertusus@free.fr> 3.7.10-2
- use pkg-config in dap-config

* Mon Dec 17 2007 Patrice Dumas <pertusus@free.fr> 3.7.10-1
- update to 3.7.10

* Sun Oct 21 2007 Patrice Dumas <pertusus@free.fr> 3.7.8-3
- remove reference to libdir in dap-config

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.7.8-2
- Rebuild for selinux ppc32 issue.

* Thu Jul  5 2007 Patrice Dumas <pertusus@free.fr> 3.7.8-1.1
- update to 3.7.8

* Thu May 31 2007 Patrice Dumas <pertusus@free.fr> 3.7.7-1.1
- update to 3.7.7

* Sat May 12 2007 Patrice Dumas <pertusus@free.fr> 3.7.6-4
- remove static libs
- set the same doc file timestamps for all arches

* Mon Apr 30 2007 Patrice Dumas <pertusus@free.fr> 3.7.6-3
- correct the library install order
- keep timestamps
- add documentation in a subpackage

* Mon Apr 30 2007 Patrice Dumas <pertusus@free.fr> 3.7.6-2
- update to 3.7.6

* Tue Oct 31 2006 Patrice Dumas <pertusus@free.fr> 3.7.2-3
- rebuild for new libcurl soname

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.7.2-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Patrice Dumas <pertusus@free.fr> 3.7.2-1
- update to 3.7.2

* Wed Sep  6 2006 Patrice Dumas <pertusus@free.fr> 3.7.1-1
- update to 3.7.1
- set licence to LGPL instead of W3C/LGPL, since only deflate is W3C, so
  the whole is under the LGPL

* Fri Jul 21 2006 Patrice Dumas <pertusus@free.fr> 3.7.0-1
- update to 3.7.0

* Mon Feb 27 2006 James Gallagher <jgallagher@opendap.org> - 3.6.0-1
- update to 3.6.0

* Mon Nov 21 2005 Patrice Dumas <pertusus@free.fr> - 3.5.3-2
- fix Source0

* Tue Aug 30 2005 Patrice Dumas <pertusus@free.fr> - 3.5.2-3
- Add missing Requires

* Sat Jul  2 2005 Patrice Dumas <pertusus@free.fr> - 3.5.1-2
- Support for shared libraries
- Add COPYING
- Update with fedora template

* Thu May 12 2005 James Gallagher <jimg@comet.opendap.org> - 3.5.0-1
- Changed: Requires xml2 to libxml2

* Wed May 11 2005 James Gallagher <jimg@zoey.opendap.org> 3.5.0-1
- Removed version numbers from .a and includes directory.

* Tue May 10 2005 James Gallagher <jimg@zoey.opendap.org> 
- Mostly works. Problems: Not sure if the %%post script stuff works.
- Must also address the RHEL3 package deps issue (curl 7.12.0 isn't available;
  not sure about xml2 2.5.7). At least the deps fail when they are not present!

* Fri May  6 2005 James Gallagher <jimg@zoey.opendap.org> 
- Initial build.
