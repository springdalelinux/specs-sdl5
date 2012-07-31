Name:               ganglia
Version:            3.0.7
Release:            3%{?dist}
Summary:            Ganglia Distributed Monitoring System

Group:              Applications/Internet
License:            BSD
URL:                http://ganglia.sourceforge.net/
Source0:            http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch1:		    ganglia-security.patch
Buildroot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      rrdtool-devel

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

%package web
Summary:            Ganglia Web Frontend
Group:              Applications/Internet
Requires:           rrdtool, php, php-gd
Requires:           %{name}-gmetad = %{version}-%{release}

%description web
This package provides a web frontend to display the XML tree published by
ganglia, and to provide historical graphs of collected metrics. This website is
written in the PHP4 language.

%package gmetad
Summary:            Ganglia Metadata collection daemon
Group:              Applications/Internet
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service

%description gmetad
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmetad daemon aggregates monitoring data from several clusters
to form a monitoring grid. It also keeps metric history using rrdtool.

%package gmond
Summary:            Ganglia Monitoring daemon
Group:              Applications/Internet
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service

%description gmond
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond daemon provides the ganglia service within a single cluster or
Multicast domain.

%package devel
Summary:            Ganglia Library
Group:              Applications/Internet

%description devel
The Ganglia Monitoring Core library provides a set of functions that
programmers can use to build scalable cluster or grid applications

%prep 
%setup -q
%patch1 -p0 -b .security
## Hey, those shouldn't be executable...
chmod -x lib/{net,rdwr,hash,llist}.h \
    libmetrics/error.c \
    libmetrics/debug_msg.h

%build
%configure \
    --with-gmetad \
    --with-shared
## Build currently fails if enabled
    #--disable-static \

## Default to run as user ganglia instead of nobody
%{__perl} -pi.orig -e 's|nobody|ganglia|g' \
    lib/libgmond.c gmetad/conf.c gmond/g25_config.c \
    gmetad/gmetad.conf gmond/gmond.conf.html ganglia.html \
    gmond/conf.pod ganglia.pod README

## Don't have initscripts turn daemons on by default
%{__perl} -pi.orig -e 's|2345|-|g' \
    gmond/gmond.init gmetad/gmetad.init

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

## Put web files in place
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -rp %{_builddir}/%{name}-%{version}/web/* $RPM_BUILD_ROOT%{_datadir}/%{name}/
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/conf.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
ln -s ../../..%{_sysconfdir}/%{name}/conf.php \
    $RPM_BUILD_ROOT%{_datadir}/%{name}/conf.php
cat << __EOF__ > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf
  #
  # Ganglia monitoring system php web frontend
  #
  
  Alias /%{name} %{_datadir}/%{name}
__EOF__

## Create directory structures
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/rrds
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
## Put files in place
cp -p %{_builddir}/%{name}-%{version}/gmond/gmond.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gmond
cp -p %{_builddir}/%{name}-%{version}/gmetad/gmetad.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gmetad
cp -p %{_builddir}/%{name}-%{version}/gmond/gmond.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/gmond.conf.5
cp -p %{_builddir}/%{name}-%{version}/gmetad/gmetad.conf $RPM_BUILD_ROOT/etc/gmetad.conf
cp -p %{_builddir}/%{name}-%{version}/mans/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
## Build default gmond.conf from gmond using the '-t' flag
%{_builddir}/%{name}-%{version}/gmond/gmond -t > $RPM_BUILD_ROOT/etc/gmond.conf
## Install binaries
make install DESTDIR=$RPM_BUILD_ROOT
## House cleaning
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/{Makefile.am,version.php.in}

%clean
rm -rf $RPM_BUILD_ROOT

### Both gmetad and gmond require user ganglia, but monitored
### nodes only need gmond, servers only need gmetad... So have
### both packages try to add the user (second one should just
### fail silently).
%pre gmetad
## Add the "ganglia" user
/usr/sbin/useradd -c "Ganglia Monitoring System" \
        -s /sbin/nologin -r -d %{_localstatedir}/lib/%{name} ganglia 2> /dev/null || :

%post gmond
/sbin/chkconfig --add gmond

%post gmetad
/sbin/chkconfig --add gmetad

%preun gmetad
if [ "$1" = 0 ]
then
  /sbin/service gmetad stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del gmetad
fi

%preun gmond
if [ "$1" = 0 ]
then
  /sbin/service gmond stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del gmond
fi

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files gmetad
%defattr(-,root,root,-)
%dir %{_localstatedir}/lib/%{name}
%attr(0755,ganglia,ganglia) %{_localstatedir}/lib/%{name}/rrds
%{_sbindir}/gmetad
%{_mandir}/man1/gmetad.1*
%{_sysconfdir}/rc.d/init.d/gmetad
%config(noreplace) %{_sysconfdir}/gmetad.conf

%files gmond
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README ChangeLog
%{_bindir}/gmetric
%{_bindir}/gstat
%{_sbindir}/gmond
%{_sysconfdir}/rc.d/init.d/gmond
%{_mandir}/man5/gmond.conf.5*
%{_mandir}/man1/gmond.1*
%{_mandir}/man1/gstat.1*
%{_mandir}/man1/gmetric.1*
%config(noreplace) %{_sysconfdir}/gmond.conf

%files devel
%defattr(-,root,root,-)
%{_includedir}/ganglia.h
%{_libdir}/libganglia*.so*
%{_bindir}/ganglia-config
%exclude %{_libdir}/libganglia.a

%files web
%defattr(-,root,root,-)
%doc web/AUTHORS web/COPYING web/ChangeLog
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/conf.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}

%changelog
* Fri May 18 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-3
- Add missing Req: php-gd so people will see nifty pie charts

* Sat Mar 24 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-2
- Own created directories (#233790)

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-1
- New upstream release

* Thu Nov 09 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-11
- gmond also needs ganglia user (#214762)

* Tue Sep 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-10
- Rebuild for new glibc

* Fri Jul 28 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-9
- Add missing Reqs on chkconfig and service
- Make %%preun sections match Fedora Extras standards
- Minor %%configure tweak

* Tue Jul 11 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-8
- Add missing php req for ganglia-web
- Misc tiny spec cleanups

* Tue Jun 13 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-7
- Clean up documentation

* Mon Jun 12 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-6
- Remove misplaced execute perms on source files

* Thu Jun 08 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-5
- Whack Obsoletes/Provides, since its never been in FE before
- Use mandir macro
- Check if service is running before issuing a stop in postun
- Remove shadow-utils Prereq, its on the FE exception list

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-4
- Run things as user ganglia instead of nobody
- Don't turn on daemons by default

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-3
- Kill off static libs
- Add URL for Source0

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-2
- Move web-frontend from /var/www/html/ to /usr/share/
- Make everything arch-specific

* Thu Jun 01 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-1
- Initial build for Fedora Extras, converting existing spec to
  (attempt to) conform with Fedora packaging guidelines
