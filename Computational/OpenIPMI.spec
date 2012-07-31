%define ipmitoolver 1.8.9
%define pythonver %(%{__python} -c "import sys; print sys.version[:3]")
Summary: OpenIPMI (Intelligent Platform Management Interface) library and tools
Name: OpenIPMI
Version: 2.0.6
Release: 5%{?dist}.4.DELL.13
License: GPL
Group: System Environment/Base
URL: http://sourceforge.net/projects/openipmi/
Source: http://prdownloads.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
Source2: http://prdownloads.sourceforge.net/ipmitool/ipmitool-%{ipmitoolver}.tar.gz
Source3: openipmi.sysconf
Source4: openipmi.initscript
Patch200: ipmitool-dell-baseline-common.patch
Patch201: ipmitool-dell-baseline-rhel5fixes.patch
Patch202: ipmitool-dell-baseline-rhel5autoconf.patch
Patch203: ipmitool-dell-rhel5manpages.patch
Patch204: ipmitool-dell9.patch
Patch205: ipmitool-dell10.patch
Patch206: ipmitool-dell11.patch
Patch207: ipmitool-dell12.patch
Patch208: ipmitool-dell13.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
PreReq: chkconfig
BuildPrereq: gdbm-devel swig glib2-devel net-snmp-devel ncurses-devel
BuildPrereq: openssl-devel python-devel readline-devel

%description
The Open IPMI project aims to develop an open code base to allow access to
platform information using Intelligent Platform Management Interface (IPMI).
This package contains the tools of the OpenIPMI project.

%package libs
Group: Development/Libraries
Summary: The OpenIPMI runtime libraries

%description libs
The OpenIPMI-libs package contains the runtime libraries for shared binaries
and applications.

%package tools
Group: Applications/System
Summary: OpenIPMI utilities and scripts from ipmitool

%description tools
The OpenIPMI-tools package contains the addon utilities and script from the
ipmitool project.

%package perl
Group: Development/Libraries
Summary: OpenIPMI Perl language bindings

%description perl
The OpenIPMI-perl package contains the Perl language bindings for OpenIPMI.

%package python
Group: Development/Libraries
Summary: OpenIPMI Python language bindings

%description python
The OpenIPMI-perl package contains the Python language bindings for OpenIPMI.

%package devel
Group: Development/Libraries
Summary: The development environment for the OpenIPMI project.
Requires: %{name} = %{version}

%description devel
The OpenIPMI-devel package contains the development libraries and header files
of the OpenIPMI project.

%prep
%setup -q -a 2

pushd ipmitool-%{ipmitoolver}
%patch200 -p1
%patch201 -p1 -b .dell.rhel5fixes
#patch202 -p1
%patch203 -p1 -b .dell.rhel5manpages
%patch204 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
popd

%build
%configure --with-pythoninstall=%{_libdir}/python%{pythonver}/site-packages
make
pushd ipmitool-%{ipmitoolver}
%configure
make 
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
# Remove python cruft in 32bit libdir on 64bit archs...
%ifarch ppc64 s390x x86_64
rm -rf $RPM_BUILD_ROOT/usr/lib
%endif
pushd ipmitool-%{ipmitoolver}
make install DESTDIR=${RPM_BUILD_ROOT}
install -d ${RPM_BUILD_ROOT}%{_datadir}/ipmitool/
cp -a contrib/* ${RPM_BUILD_ROOT}%{_datadir}/ipmitool/
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/ipmitool/Makefile*
popd

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/ipmi
install -d ${RPM_BUILD_ROOT}%{_initrddir}
install -m 755 %SOURCE4 ${RPM_BUILD_ROOT}%{_initrddir}/ipmi

%post
/sbin/chkconfig --add ipmi

%preun
if [ $1 = 0 ]; then
   service ipmi stop >/dev/null 2>&1
   /sbin/chkconfig --del ipmi
fi

%postun
if [ "$1" -ge "1" ]; then
    service ipmi condrestart >/dev/null 2>&1 || :
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%config %{_initrddir}/ipmi
%{_bindir}/ipmicmd
%{_bindir}/ipmilan
%{_bindir}/ipmish
%{_bindir}/ipmi_ui
%{_bindir}/openipmicmd
%{_bindir}/openipmish
%{_bindir}/rmcp_ping
%{_bindir}/solterm
%{_mandir}/man1/ipmi_ui*
%{_mandir}/man1/openipmicmd*
%{_mandir}/man1/openipmigui*
%{_mandir}/man1/openipmish*
%{_mandir}/man1/rmcp_ping*
%{_mandir}/man1/solterm*
%{_mandir}/man7/ipmi_cmdlang*
%{_mandir}/man7/openipmi_conparms*
%{_mandir}/man8/ipmilan*

%files perl
%{_libdir}/perl5/site_perl/*/*-linux-thread-multi/OpenIPMI.pm
%dir %{_libdir}/perl5/site_perl/*/*-linux-thread-multi/auto/OpenIPMI
%{_libdir}/perl5/site_perl/*/*-linux-thread-multi/auto/OpenIPMI/*

%files python
%{_libdir}/python*/site-packages/*

%files tools
%defattr(-,root,root)
%{_datadir}/doc/ipmitool/
%{_datadir}/ipmitool/
%{_bindir}/ipmitool
%{_mandir}/man1/ipmitool*
%{_mandir}/man8/ipmievd*
/usr/sbin/ipmievd

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*

%files devel
%defattr(-,root,root)
%{_mandir}/man7/*
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Fri Mar 21 2008 Josko Plazonic <plazonic@math.princeton.edu>
- add dell patches

* Thu Jun 21 2007 Phil Knirsch <pknirsch@redhat.com> 2.0.6-5.el5.4
- Update ipmitool to 1.8.9 (#228114)

* Wed Dec 13 2006 Phil Knirsch <pknirsch@redhat.com> 2.0.6-5.el5.3
- Fixed ipmitool fru print displays error for physical fru devices (#217676)

* Tue Nov 21 2006 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-5.el5.2
- Added patch to fix sensors problems on Woodcrest (#214309)

* Wed Oct 25 2006 Phil Knirsch <pknirsch@redhat.com>
- Bump release to trigger build on ia64, too (#211313)

* Tue Jul 18 2006 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-5
- Fixed check for udev in initscript (#197956)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.6-4.1
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com> 2.0.6-4
- don't include <linux/compiler.h>

* Fri Jun 16 2006 Jon Masters <jcm@redhat.com> 2.0.6-3
- Fix a build requires (needs glibc-kernheaders)

* Thu Jun 15 2006 Jesse Keating <jkeating@redhat.com> 2.0.6-2
- Bump for new glib2

* Tue May 16 2006 Phil Knirsch <pknirsch@redhat.com> 2.0.6-1
- Fixed bug with type conversion in ipmitool (#191091)
- Added python bindings 
- Split off perl and python bindings in separate subpackages
- Dropped obsolete patches
- Added missing buildprereq on readline-devel
- Made it install the python bindings properly on 64bit archs

* Mon May 15 2006 Phil Knirsch <pknirsch@redhat.com>
- Updated ipmitool to 1.8.8
- Updated OpenIPMI to 2.0.6

* Fri Feb 17 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-19
- Added missing PreReq for chkconfig

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-18
- Updated ipmitool to latest upstream version.
- Removed 3 patches for already fixed bugs in latest ipmitool.
- Adapted warning message fix for ipmitool for latest version.

* Tue Jan 24 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-17
- Fixed some minor things in initscripts.

* Mon Jan 09 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-16
- Included FRU fix for displaying FRUs with ipmitool
- Included patch for new option to specify a BMC password for IPMI 2.0 sessions

* Tue Jan 03 2006 Radek Vokal <rvokal@redhat.com> 1.4.14-15
- Rebuilt against new libnetsnmp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-14
- Some more initscript and sysconfig updates from Dell.

* Wed Nov 09 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-13
- Rebuilt to link against latest openssl libs.
- Fixed ipmitool not setting session privilege level (#172312)

* Wed Nov 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-11
- Rebuild to link against new net-snmp libs.

* Tue Oct 11 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-10
- Updated initscript to fix missing redhat-lsb bug (#169901)

* Thu Sep 08 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-9
- Another update to latest initscripts from Dell
- Fixed some missing return statements for non-void functions (#164138)

* Thu Sep 01 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-8
- Updated initscript to latest version from Dell

* Fri Aug 12 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-7
- Fixed the unwanted output of failed module loading of the initscript. Behaves
  now like all our other initscripts (#165476)

* Fri Aug 05 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-6
- Fixed build problem on 64bit machines

* Fri Jul 15 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-5
- Fixed missing change to not autostart in the initscript

* Wed Jul 06 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-4
- Made the initscript a replacing configfile

* Mon Jul 04 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-3
- Updated versions of the initscripts and sysconf files
- Fixed typo in preun script and changelog

* Mon Jun 27 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-2
- Updated to OpenIPMI-1.4.14
- Split the main package into normal and libs package for multilib support
- Added ipmitool-1.8.2 to OpenIPMI and put it in tools package
- Added sysconf and initscript (#158270)
- Fixed oob subscripts (#149142)

* Wed Mar 30 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-5
- Correctly put libs in the proper packages

* Thu Mar 17 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-4
- gcc4 rebuild fixes
- Added missing gdbm-devel buildprereq

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-3
- bump release and rebuild with gcc 4

* Tue Feb 08 2005 Karsten Hopp <karsten@redhat.de> 1.4.11-2 
- update

* Tue Oct 26 2004 Phil Knirsch <pknirsch@redhat.com>
- Initial version
