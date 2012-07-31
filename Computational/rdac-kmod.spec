###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2006 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################
Source10: kmodtool
%define kmodtool bash %{SOURCE10}
%{!?kversion: %define kversion 2.6.18-194.el5}
# hint: this can he overridden with "--define kversion foo" on the rpmbuild command line, e.g.
# --define "kversion 2.6.16-1.2096_FC5"

%define kmod_name rdac
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""
%ifarch ppc
%define smpvar smp
%endif
%ifarch i686 x86_64 ia64
%define xenvar xen
#define kdumpvar kdump
%endif
%ifarch i686
%define PAEvar PAE
%endif
%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?kdumpvar} %{?PAEvar}}
# hint: this can he overridden with "--define kvariant foo bar" on the rpmbuild command line, e.g.
# --define 'kvariant "" smp' 

# hacks to work around kernel_read issue
%define my_requires %{_builddir}/my_requires
%define _use_internal_dependency_generator 0


Name:           %{kmod_name}-kmod
Version:        09.03.0C05.0331
Release:        0.4%{?dist}
Summary:        %{kmod_name} kernel modules

Group:          System Environment/Kernel
License:        Unknown
URL:            http://www.lsi.com/rdac/ds4000.html
Source0:        rdac-LINUX-%{version}-source.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  i686 x86_64

%description
rdac driver

# magic hidden here:
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}


%prep
# to understand the magic better or to debug it, uncomment this:
#{kmodtool} rpmtemplate %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null
#sleep 5
%setup -q -c -T -a 0
%{__cat} <<EOF >%{my_requires}
#!/bin/sh
%{__find_requires} | grep -v '^ksym(kernel_read)'
exit 0
EOF
chmod +x %{my_requires}
#define __find_requires %{my_requires}
for kvariant in %{kvariants} ; do
    cp -a linuxrdac-%{version} _kmod_build_${kvariant}
done


%build
for kvariant in %{kvariants}
do
    ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}
    pushd _kmod_build_$kvariant
    make -C "${ksrc}" V=0 M=${PWD} SUBDIRS=${PWD} modules %{?_smp_mflags}
    #make DIST=REDHAT OS_VER=%{kversion} KERNEL_OBJ=$ksrc IS_SMP=1 HOST_TYPE=%{arch}
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kvariant in %{kvariants}
do
    pushd _kmod_build_$kvariant
    mkdir -p $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}
    install -m 644 *.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}
    popd
done
# Temporarily executable for stripping, fixed later in %%files.
chmod u+x $RPM_BUILD_ROOT/lib/modules/*/extra/%{kmod_name}/*

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Mon Feb 09 2009 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
