Name: maui
Version: 3.2.6p21
Release: 7.SL30X_ratio01.cses.5
Source0: http://www.clusterresources.com/downloads/maui/maui-%{version}.tar.gz
Source1: maui-init.d.sh
Source2: maui.cfg
Source3: maui.sysconfig
# Increase the number of queues we can cope with.
#Patch1: maui_max_mclass_patch
# Increase the number of queued jobs we can cope with.
#Patch2: maui_max_mjobs_patch
#Patch3: scale-fscalc.patch
Patch10: maui-preemptfix.patch
Summary: The Maui supercluster scheduler
License: unknown
Group: System/Daemons
Packager: Steve Traylen <s.traylen@rl.ac.uk>
BuildRoot: %{_var}/tmp/maui-%{version}-root
BuildRequires: torque-devel >= 2.1.6
Requires: net-tools

# The following option is ssupported:
#   --with prefix=directory

# This is the CSES default prefix
%define _prefix	/usr

%if %{?_with_prefix:1}%{!?_with_prefix:0}
%define _prefix %(set -- %{_with_prefix}; echo $1 | grep -v with | sed 's/=//')
%endif

%package client
Requires: maui = %{version}-%{release}
Summary: Client for the MAUI schedular from SuperCluster.org
Group: System/Tools

%package server
Requires: maui = %{version}-%{release}
Summary: Server for the MAUI schedular from SuperCluster.org
Group: System/Tools

%package devel
Summary: Libary and header files for maui.
Group: System/Tools

%description
MAUI is the scheduler from SuperCluster.org

%description client
MAUI is the scheduler from SuperCluster.org

%description server
MAUI is the scheduler from SuperCluster.org

%description devel
MAUI is the scheduler from SuperCluster.org



%prep
%setup -q 
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch10 -p1 -b .preemptfix

%build
# Kill the stack protection and fortify source stuff...
# and maui sees to be buggy with it turned on
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
CFLAGS="${RPM_OPT_FLAGS}" ; export CFLAGS ; 
CXXFLAGS="${RPM_OPT_FLAGS}" ; export CXXFLAGS ; 
FFLAGS="${RPM_OPT_FLAGS}" ; export FFLAGS ; 
%configure --with-spooldir=%{_var}/spool/maui \
           --with-pbs=%{_prefix}
make 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir} ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig

make install \
       INST_DIR=${RPM_BUILD_ROOT}%{_prefix} \
       MSCHED_HOME=${RPM_BUILD_ROOT}%{_var}/spool/maui

# remove, we will have one of our own
rm -rf ${RPM_BUILD_ROOT}/etc/init.d

# edit and copy maui boot script for current _prefix
%__sed -e 's|/usr/bin/|%{_prefix}/bin/|' \
       -e 's|/usr/sbin/|%{_prefix}/sbin/|' \
	< %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/maui

install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_var}/spool/maui/maui.cfg

cp %{SOURCE3} ${RPM_BUILD_ROOT}/etc/sysconfig/maui

%ifarch x86_64
mv $RPM_BUILD_ROOT%{_prefix}/lib/* ${RPM_BUILD_ROOT}%{_libdir}
%endif

%post
# edit maui.cfg script for install hostname (short form)
# if set, leave it, else try to get it with hostname command
HOSTNAME=${HOSTNAME:-`hostname -s`}
# if still empty set it to localhost
HOSTNAME=${HOSTNAME:-localhost}
# if localhost try checking /etc/sysconfig/network
if [ -e /etc/sysconfig/network -a "$HOSTNAME" = "localhost" ]; then
	. /etc/sysconfig/network
	HOSTNAME=${HOSTNAME%%%%.*}
fi
%__sed -i -e "s|localhost|$HOSTNAME|" %{_var}/spool/maui/maui.cfg

%post server
/sbin/chkconfig --add maui
if [ "$1" -ge "1" ]; then
    service maui condrestart > /dev/null 2>&1 || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%config(noreplace) %{_var}/spool/maui/maui.cfg
%config(noreplace) %{_var}/spool/maui/maui-private.cfg

%files client
%attr(0755,root,root) %{_bindir}/*

%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/maui
%attr(0755,root,root) %{_sbindir}/maui
%dir %{_var}/spool/maui/stats
%dir %{_var}/spool/maui/traces
%dir %{_var}/spool/maui/tools
%dir %{_var}/spool/maui/spool
%config(noreplace) /etc/sysconfig/maui

%files devel
%attr(0644,root,root) %{_includedir}/moab.h
%attr(0644,root,root) %{_libdir}/libmcom.a
%attr(0644,root,root) %{_libdir}/libmoab.a

%changelog
* Mon Apr 26 2010 Josko Plazonic <plazonic@math.princeton.edu>
- add Bill's patch to fix preemption in cases where jobs are not
  rerunnable

* Thu Dec 12 2006 Josko Plazonic <plazonic@math.princeton.edu>
- added condrestart option to init script
- fixed up spec file not to use things like %{_prefix}/bin - use
  directly %{_bindir} as we set Prefix:
- moved back to /usr and corrected for torque libs now being in
  /usr/lib/torque (similar for includes)
