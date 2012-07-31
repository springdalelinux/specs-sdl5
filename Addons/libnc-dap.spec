Name: libnc-dap
Summary: The NetCDF interface to DAP-2 from OPeNDAP
Version: 3.7.4
Release: 3%{?dist}

Group: Development/Libraries
# ncdump, netcdf headers, lnetcdf are coverd by a BSD/MIT-like license
# but they are linked statically against libnc-dap
License: LGPLv2+
URL: http://www.opendap.org/
Source0: http://www.opendap.org/pub/source/libnc-dap-%{version}.tar.gz
Patch0:  libnc-dap-3.7.4-AIS.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libdap-devel >= 3.8.0 gcc-gfortran
BuildRequires: pkgconfig


%description
The libnc-dap library is a call-for-call replacement for netcdf. It can 
read and write to and from netcdf files on the local machine and it can 
read from DAP2 compatible data servers running on local or remote 
machines. Data served using DAP2 need not be stored in netcdf files 
to be read using this replacement library.
Also included in this package is the ncdump utility, also bundled with the
original netcdf library, renamed dncdump, relinked with the library and 
thus able to read from DAP2 compatible servers.

%package devel
Summary: Development files and header files from libnc-dap
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libdap-devel >= 3.8.0
Requires: pkgconfig
# for /usr/share/aclocal owning
Requires: automake

%description devel
This package contains all the files needed to develop applications that
will use libnc-dap.

%prep
%setup -q
%patch0 -p1 -b .AIS
rm -rf netcdf/.svn

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
rm $RPM_BUILD_ROOT%{_libdir}/*.la

mv  $RPM_BUILD_ROOT%{_bindir}/ncdap-config-pkgconfig $RPM_BUILD_ROOT%{_bindir}/ncdap-config

mv $RPM_BUILD_ROOT%{_bindir}/ncdump $RPM_BUILD_ROOT%{_bindir}/dncdump

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/dncdump
%{_libdir}/libnc-dap.so.*
%doc README README.translation NEWS COPYRIGHT COPYING netcdf

%files devel
%defattr(-,root,root,-)
%{_libdir}/libnc-dap.so
%{_libdir}/pkgconfig/libnc-dap.pc
%{_bindir}/ncdap-config
%{_includedir}/libnc-dap/
%{_datadir}/aclocal/*


%changelog
* Thu Jul 15 2010 Orion Poplawski <orion@cora.nwra.com> - 3.7.4-3
- Rebuild for libdap 3.10.2
- Add patch to change AISConnect to Connect

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.7.4-1
- Update to 3.7.4
- Drop templates patch applied upstream

* Wed Jul 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.7.3-3
- Rebuild for libdap 3.9.3
- Add patch to support 3.9.3

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  9 2008 Patrice Dumas <pertusus@free.fr> 3.7.3-1
- update to 3.7.3

* Thu Sep  4 2008 Patrice Dumas <pertusus@free.fr> 3.7.0-11
- gcc 4.3 patch for missing include files

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.7.0-10
- Autorebuild for GCC 4.3

* Mon Dec 17 2007 Patrice Dumas <pertusus@free.fr> 3.7.0-9
- rebuild against newer libdap

* Sun Oct 21 2007 Patrice Dumas <pertusus@free.fr> 3.7.0-8
- remove reference to libdir in ncdap-config, should fix multilib conflict
  (#342251)

* Wed Aug 22 2007 Patrice Dumas <pertusus@free.fr> 3.7.0-7
- fix license
- add gawk BuildRequires

* Fri Jun  1 2007 Patrice Dumas <pertusus@free.fr> 3.7.0-4
- remove static libs

* Tue May  1 2007 Patrice Dumas <pertusus@free.fr> 3.7.0-3
- Buildrequires gfortran for the fortran API

* Mon Apr 30 2007 Patrice Dumas <pertusus@free.fr> 3.7.0-2
- update to 3.7.0

* Tue Oct 31 2006 Patrice Dumas <pertusus@free.fr> 3.6.2-5
- licence is LGPL since it cause the BSD code to be distributed as LGPL too

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.6.2-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Patrice Dumas <pertusus@free.fr> 3.6.2-3
- rebuild against libdap 3.7.2

* Wed Sep  6 2006 Patrice Dumas <pertusus@free.fr> 3.6.2-2
- update to 3.6.2

* Sat Jul 22 2006 Patrice Dumas <pertusus@free.fr> 3.6.0-4
- BuildRequires the 3.7.0 libdap library or above

* Sat Jul 22 2006 Patrice Dumas <pertusus@free.fr> 3.6.0-3
- quick and dirty patch to build against newer libdap

* Fri Jul 21 2006 Patrice Dumas <pertusus@free.fr> 3.6.0-2
- rebuild against newer libdap

* Tue Feb 28 2006 James Gallagher <jgallagher@opendap.org> - 3.6.0-1.1
- new release

* Mon Nov 21 2005 Patrice Dumas <pertusus@free.fr> - 3.5.2-5
- fix Source0

* Tue Aug 30 2005 Patrice Dumas <pertusus@free.fr> - 3.5.2-4
- Add missing Requires
- remove the INSTALL file and add the netcdf directory

* Fri Aug 19 2005 James Gallagher <jimg@zoey.opendap.org> 3.5.2-3
- Added README.translation and INSTALL; version to 3.5.2

* Sat Jul  2 2005 Patrice Dumas <pertusus@free.fr> - 3.5.1-2
- Support for shared libraries

* Mon Jun 20 2005 James Gallagher <jimg@otaku.opendap.org> 
- Initial build.
