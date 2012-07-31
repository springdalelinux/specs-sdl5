
# comment out snap if building a real release
%define name torque
%define version 3.0.5

%define release 6.PU_IAS.5


%define torquehomedir %{_localstatedir}/spool/PBS
%define server_name head

#define _libdir /usr/local/lib
#define _mandir /usr/local/man
#define _bindir /usr/local/bin
#define _sbindir /usr/local/sbin
#define _includedir /usr/local/include
%define drmaadocdir /usr/share/doc/torque-drmaa

%define use_tcl 1
%define build_server yes
%define build_mom yes
%define build_clients yes
%define build_gui yes
%define build_pbs_rcp no
%define build_drmaa yes
%define build_drmaa_docs yes
%define pammoddir disabled
%define modulefiles_dir no

%define configure_args  --prefix=%{_prefix} --sbindir=%{_sbindir} --bindir=%{_bindir} \\\
 --includedir=%{_includedir} --mandir=%{_mandir} --libdir=%{_libdir} \\\
 --with-rcp=scp --with-server-home=%{torquehomedir} --with-default-server=%{server_name} \\\
 --enable-drmaa


############################################
## no user serviceable parts below this line

%if "%build_gui" == "yes"
%if "%use_tcl" == "0"
%error GUI cannot be built without TCL support
%endif
%endif

%define shared_description %(echo -e "TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource \\nmanager providing control over batch jobs and distributed compute nodes.  \\nTorque is based on OpenPBS version 2.3.12 and incorporates scalability, \\nfault tolerance, and feature extension patches provided by USC, NCSA, OSC, \\nthe U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many \\nother leading edge HPC organizations.\\n\\nThis build was configured with:\\n   %{?configure_args}\\n  \\n")


Summary: Tera-scale Open-source Resource and QUEue manager
Name: %{name}
Version: %{version}
Release: %{?snap:snap.%snap.}%{release}
Source: torque-%{version}%{?snap:-snap.%snap}.tar.gz
Source1: torque-2.1.9.tar.gz
Patch1: torque-billchanges.patch
Patch11: torque-condrestartfixes.patch
Patch12: torque-2.1-silence-get_proc_stat-errors.patch
Patch13: torque-tclxfixes.patch
Patch14: torque-2.3.10-logpreempt.patch
Patch20: torque-buffer-overrun-2.3.13.patch
License: OpenPBS
Group: System Environment/Daemons
URL: http://www.clusterresources.com/products/torque/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Provides: pbs
BuildRequires: ed
BuildRequires: tcl-devel, tclx-devel, tk-devel, openssh-clients, sendmail
BuildRequires: pam-devel, xauth, flex, bison, groff, readline-devel
BuildRequires: doxygen, gperf, tetex-latex, tetex-dvips, ncurses-devel
Requires: openssh-clients
Conflicts: pbspro, openpbs, openpbs-oscar
Obsoletes: scatorquea
Requires: %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}


%if "%build_gui" == "no"
Obsoletes: %{name}-gui
%endif

%description
%shared_description
This package holds just a few shared files and directories.



%prep
%setup -n torque-%{version}%{?snap:-snap.%snap} -n torque-%{version}%{?snap:-snap.%snap} -c -a 1
cd torque-%{version}%{?snap:-snap.%snap}
%patch1 -p1 -b .billchanges
#patch14 -p1 -b .logpreempt
#patch20 -p1 -b .bufferoverflow
cd ..
cd torque-2.1.9
%patch11 -p1 -b .condrestartfixes
%patch12 -p0 -b .silencetorque
%patch13 -p1 -b .tclxfixes
echo '#define PBS_VERSION "%{version}-%{release}"' > src/include/pbs_version.h

%build
export TCLX_LIBS="-L%{_libdir}/tclx8.4 -rpath %{_libdir}/tclx8.4 -L%{_libdir}/tclx8.4 -ltclx8.4"
#export TCLX_LIBS="-L%{_libdir}/tclx8.4 -Wl,-rpath,%{_libdir}/tclx8.4 -L%{_libdir}/tclx8.4 -ltclx8.4"
cd torque-%{version}%{?snap:-snap.%snap}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
CFLAGS="${RPM_OPT_FLAGS}" ; export CFLAGS ;
./configure %{?configure_args}

%{__make} %{?_smp_mflags}
cd ..

cd torque-2.1.9
CFLAGS="-fPIC -O0 -g -pipe -Wall -Wno-unused -std=gnu99 -pedantic -D_GNU_SOURCE -DTCLX"
export CFLAGS

for i in $(find . -name config.guess -o -name config.sub) ; do
   if [ -f /usr/lib/rpm/%{_host_vendor}/$(basename $i) ] ; then
       %{__rm} -f $i && %{__cp} -fv /usr/lib/rpm/%{_host_vendor}/$(basename $i) $i
   elif [ -f /usr/lib/rpm/$(basename $i) ] ; then
        %{__rm} -f $i && %{__cp} -fv /usr/lib/rpm/$(basename $i) $i
   fi
done

# autoconf and friends don't work with torque, so we can't use the
# various configure macros
./configure --prefix=%{_prefix} --sbindir=%{_sbindir} --bindir=%{_bindir} \
 --includedir=%{_includedir} --mandir=%{_mandir} --libdir=%{_libdir} \
 --enable-server --enable-clients --enable-mom --enable-docs \
 --enable-gui --with-server-home=/var/spool/PBS --with-default-server=head --disable-filesync --enable-syslog --with-tcl --with-tclx --enable-rpp --with-scp

%{__make} clean
%{__make} %{_smp_mflags} all

cd ..

%install
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf "$RPM_BUILD_ROOT"

cd torque-%{version}%{?snap:-snap.%snap}
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

env DESTDIR=$RPM_BUILD_ROOT sh ./buildutils/pbs_mkdirs common

if [ -f /etc/SuSE-release ];then
  initpre="suse."
else
  initpre=""
fi

# install initscripts
serverinit="`test "%build_server" == "yes" && echo pbs_sched pbs_server || echo`"
mominit="`test "%build_mom" == "yes" && echo pbs_mom || echo`"
%{__mkdir_p} $RPM_BUILD_ROOT%{_initrddir}
for initscript in $serverinit $mominit; do
  %__sed -e 's|^PBS_HOME=.*|PBS_HOME=%{torquehomedir}|' \
         -e 's|^PBS_DAEMON=.*|PBS_DAEMON=%{_sbindir}/'$initscript'|' \
        < contrib/init.d/$initpre$initscript > $RPM_BUILD_ROOT%{_initrddir}/$initscript
  %__chmod 755 $RPM_BUILD_ROOT%{_initrddir}/$initscript
done

# remove libtool droppings
%{__rm} -vf $RPM_BUILD_ROOT/%pammoddir/pam_pbssimpleauth.{a,la} $RPM_BUILD_ROOT/%{_libdir}/*.la

# we want pbstop and qpeek
install -m 755 contrib/pbstop contrib/qpeek $RPM_BUILD_ROOT%{_bindir}

cd ..
cd torque-2.1.9
install -m 755 src/lib/Libpbs/.libs/libtorque.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libtorque.so.0.0.0
pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libtorque.so.0.0.0 libtorque.so.0
popd
cd ..

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT


%post
if %__grep -q "PBS services" /etc/services;then
   : PBS services already installed
else
   cat<<-__EOF__>>/etc/services
	# Standard PBS services
	pbs           15001/tcp           # pbs server (pbs_server)
	pbs           15001/udp           # pbs server (pbs_server)
	pbs_mom       15002/tcp           # mom to/from server
	pbs_mom       15002/udp           # mom to/from server
	pbs_resmom    15003/tcp           # mom resource management requests
	pbs_resmom    15003/udp           # mom resource management requests
	pbs_sched     15004/tcp           # scheduler
	pbs_sched     15004/udp           # scheduler
	__EOF__
fi


%files
%defattr(-, root, root)
%doc torque-%{version}%{?snap:-snap.%snap}/INSTALL torque-%{version}%{?snap:-snap.%snap}/README.torque 
%doc torque-%{version}%{?snap:-snap.%snap}/torque.setup torque-%{version}%{?snap:-snap.%snap}/Release_Notes
%doc torque-%{version}%{?snap:-snap.%snap}/CHANGELOG
%config(noreplace) %{torquehomedir}/server_name
%config(noreplace) %{torquehomedir}/pbs_environment
%{torquehomedir}/spool
%{torquehomedir}/aux
%if "%modulefiles_dir" != "no"
%modulefiles_dir/%{name}
%endif


%package libs
Group: System Environment/Libraries
Summary: Torque libraries
Obsoletes: torque21-libs
%description libs
%shared_description
This package holds torque libraries.

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(-, root, root)
%{_libdir}/libtorque*.so.*


%package docs
Group: Documentation
Summary: docs for Torque
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: pbs-docs
%description docs
%shared_description
This package holds the documentation files.

%files docs
%defattr(-, root, root)
%doc torque-%{version}%{?snap:-snap.%snap}/doc/admin_guide.ps
%{_mandir}/man*/*


%package scheduler
Group: System Environment/Daemons
Summary: scheduler part of Torque
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: pbs-scheduler
%description scheduler
%shared_description
This package holds the fifo C scheduler.

%if "%build_server" == "yes"
%files scheduler
%defattr(-, root, root)
%{_sbindir}/pbs_sched
%{_sbindir}/qschedd
%{_initrddir}/pbs_sched
%dir %{torquehomedir}/sched_priv
%config(noreplace) %{torquehomedir}/sched_priv/*
%{torquehomedir}/sched_logs
%endif

%post scheduler
/sbin/chkconfig --add pbs_sched

%preun scheduler
[ $1 = 0 ] || exit 0
/sbin/service pbs_sched stop >/dev/null 2>&1 || :
/sbin/chkconfig --del pbs_sched


%package server
Group: System Environment/Daemons
Summary: server part of Torque
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: pbs-server
%description server
%shared_description
This package holds the server.

%if "%build_server" == "yes"
%files server
%defattr(-, root, root)
%{_sbindir}/pbs_server
%{_sbindir}/qserverd
%{_initrddir}/pbs_server
%{torquehomedir}/server_logs
%dir %{torquehomedir}/server_priv
%dir %{torquehomedir}/server_priv/accounting
%dir %{torquehomedir}/server_priv/acl_groups
%dir %{torquehomedir}/server_priv/acl_hosts
%dir %{torquehomedir}/server_priv/acl_svr
%dir %{torquehomedir}/server_priv/acl_users
%dir %{torquehomedir}/server_priv/arrays
%dir %{torquehomedir}/server_priv/credentials
%dir %{torquehomedir}/server_priv/disallowed_types
%dir %{torquehomedir}/server_priv/hostlist
%dir %{torquehomedir}/server_priv/jobs
%dir %{torquehomedir}/server_priv/queues
%config(noreplace) %{torquehomedir}/server_priv/nodes
%endif

%post server
/sbin/chkconfig --add pbs_server

%preun server
[ $1 = 0 ] || exit 0
/sbin/service pbs_server stop >/dev/null 2>&1 || :
/sbin/chkconfig --del pbs_server


%package mom
Group: System Environment/Daemons
Summary: execution part of Torque
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: pbs-mom
%description mom
%shared_description
This package holds the execute daemon required on every node.

%if "%build_mom" == "yes"
%files mom
%defattr(-, root, root)
%{_sbindir}/pbs_mom
%{_sbindir}/qnoded
%{_sbindir}/pbs_demux
%{_bindir}/pbs_track
%{_initrddir}/pbs_mom
%if "%build_pbs_rcp" == "yes"
%attr(4755 root root) %{_sbindir}/pbs_rcp
%endif
%dir %{torquehomedir}/mom_priv
%dir %{torquehomedir}/mom_priv/jobs
%{torquehomedir}/mom_logs
%{torquehomedir}/checkpoint
%{torquehomedir}/undelivered
%endif

%post mom
/sbin/chkconfig --add pbs_mom

%preun mom
[ $1 = 0 ] || exit 0
/sbin/service pbs_mom stop >/dev/null 2>&1 || :
/sbin/chkconfig --del pbs_mom


%package client
Group: Applications/System
Summary: client part of Torque
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: pbs-client
%description client
%shared_description
This package holds the command-line client programs.

%if "%build_clients" == "yes"
%files client
%defattr(-, root, root)
%{_bindir}/q*
%{_bindir}/chk_tree
%{_bindir}/hostn
%{_bindir}/nqs2pbs
%{_bindir}/pbsdsh
%{_bindir}/pbsnodes
%{_bindir}/printjob
%{_bindir}/printtracking
%{_bindir}/printserverdb
%{_bindir}/tracejob
%{_bindir}/pbstop
%{_sbindir}/momctl
%attr(4755 root root) %{_sbindir}/pbs_iff
%if "%use_tcl" == "1"
%{_bindir}/pbs_tclsh
%endif
%endif


%package gui
Group: Applications/System
Summary: graphical client part of Torque
Requires: %{name}-client = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: xpbs xpbsmon
%description gui
%shared_description
This package holds the graphical clients.

%if "%build_gui" == "yes"
%files gui
%defattr(-, root, root)
%{_bindir}/pbs_wish
%{_bindir}/xpbs
%{_bindir}/xpbsmon
%{_libdir}/xpbs
%{_libdir}/xpbsmon
%endif


%package localhost
Group: Applications/System
Summary: installs and configures a minimal localhost-only batch queue system
PreReq: pbs-mom pbs-server pbs-client pbs-scheduler
%description localhost
%shared_description
This package installs and configures a minimal localhost-only batch queue system.

%files localhost
%defattr(-, root, root)
%post localhost
/sbin/chkconfig pbs_mom on
/sbin/chkconfig pbs_server on
/sbin/chkconfig pbs_sched on
/bin/hostname --long > %{torquehomedir}/server_priv/nodes
/bin/hostname --long > %{torquehomedir}/server_name
/bin/hostname --long > %{torquehomedir}/mom_priv/config
pbs_server -t create
qmgr -c "s s scheduling=true"
qmgr -c "c q batch queue_type=execution"
qmgr -c "s q batch started=true"
qmgr -c "s q batch enabled=true"
qmgr -c "s q batch resources_default.nodes=1"
qmgr -c "s q batch resources_default.walltime=3600"
qmgr -c "s s default_queue=batch"
%{_initrddir}/pbs_mom restart
%{_initrddir}/pbs_sched restart
%{_initrddir}/pbs_server restart
qmgr -c "s n `/bin/hostname --long` state=free" -e


%package devel
Summary: Development tools for programs which will use the %{name} library
Group: Development/Libraries
Provides: lib%{name}-devel
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description devel
%shared_description
This package includes the header files and static libraries
necessary for developing programs which will use %{name}.

%files devel
%defattr(-, root, root)
%{_libdir}/libtorque*.a
%{_libdir}/libtorque*.so
%{_includedir}/pbs_error.h
%{_includedir}/pbs_error_db.h
%{_includedir}/pbs_ifl.h
%{_includedir}/rm.h
%{_includedir}/rpp.h
%{_includedir}/tm_.h
%{_includedir}/tm.h
%{_bindir}/pbs-config



%package pam
Summary: PAM module for PBS MOM nodes
Group: System Environment/Base
%description pam
%shared_description
A simple PAM module to authorize users on PBS MOM nodes with a running job.

%if "%pammoddir" != "disabled"
%files pam
%defattr(-, root, root)
%doc torque-%{version}%{?snap:-snap.%snap}/src/pam/README.pam
%pammoddir/pam_pbssimpleauth.so
%endif


%package drmaa
Summary: DRMAA 1.0 implementation for PBS/TORQUE
Group: System Environment/Base
%description drmaa
%shared_description
An API specification for the submission and control of jobs to one or more
Distributed Resource Management (DRM) systems.

%if "%build_drmaa" == "yes"
%files drmaa
%defattr(-, root, root)
%{_libdir}/libdrmaa.*
%{_includedir}/drmaa.h
%endif

%package drmaa-docs
Summary: DRMAA 1.0 implementation for PBS/TORQUE
Group: System Environment/Base
%description drmaa-docs
%shared_description
An API specification for the submission and control of jobs to one or more
Distributed Resource Management (DRM) systems.

%if "%build_drmaa_docs" == "yes"
%files drmaa-docs
%defattr(-, root, root)
%{drmaadocdir}
%endif

%changelog
* Fri Feb 17 2012 Josko Plazonic <plazonic@math.princeton.edu>
- previously updated to 3.0.4, now added also %config for nodes

* Thu Jun 9 2011 Josko Plazonic <plazonic@math.princeton.edu>
- add torque-buffer-overrun.patch , rhbz#711463

* Fri Apr 23 2010 Josko Plazonic <plazonic@math.princeton.edu>
- log pre-empted jobs too

* Tue Mar 02 2009 Josko Plazonic <plazonic@math.princeton.edu>
- specified with %dir config dirs for mom_priv and server_priv to attempt
  to prevent overwriting of config files
