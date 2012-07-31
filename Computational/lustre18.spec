Source10: kmodtool
Source11: find-requires
Source12: find-requires.ksyms
%define kmodtool bash %{SOURCE10}
%{!?kversion: %define kversion 2.6.18-128.1.16.el5}
# hint: this can he overridden with "--define kversion foo" on the rpmbuild command line, e.g.
# --define "kversion 2.6.16-1.2096_FC5"

%define kmod_name lustre18
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""
%ifarch ppc
%define smpvar smp
%endif
%ifarch i686 x86_64 ia64
#define xenvar xen
#define kdumpvar kdump
%endif
%ifarch i686
%define PAEvar PAE
%endif
%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?kdumpvar} %{?PAEvar}}
%{!?mykvariants: %define mykvariants %{?xenvar} %{?kdumpvar} %{?PAEvar} %{?upvar} %{?smpvar} }
# hint: this can he overridden with "--define kvariant foo bar" on the rpmbuild command line, e.g.
# --define 'kvariant "" smp' 

# we need this
%define mrelease 0.5%{?dist}

Name:		lustre18
Summary:	Lustre File System
Version:	1.8.0.1
Release:        %{mrelease}
License:	GPL
Group:		Utilities/System
URL: 		http://www.sun.com/software/products/lustre/index.xml
Source0:	lustre-%{version}.tar.gz
Patch1:		lustre-buildfixes.patch
Buildroot:	%{_tmppath}/%{name}-buildroot
ExclusiveArch:  i686 x86_64
BuildRequires:	libibverbs-devel, opensm-devel, librdmacm-devel, zlib-devel, net-snmp-devel, readline-devel, openssl-devel, lm_sensors-devel

# Override find_provides to use a script that provides "kernel(symbol) = hash".
# Pass path of the RPM temp dir containing kabideps to find-provides script.
%global _use_internal_dependency_generator 0
%define __find_requires %_sourcedir/find-requires %{name}

%description
Userspace tools and files for the Lustre file system.

%package devel
Summary:	Lustre File System development files
Group:		Development/Kernel
Requires:	%{name} = %{version}-%{mrelease}

%description devel
Lustre development include files and libraries.

# magic hidden here:
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%prep
%setup -n lustre-%{version} -c
#patch1 -p0 -b .buildfixes
for kvariant in %{kvariants} ; do
    cp -ar lustre-%{version} _kmod_build_${kvariant}
        perl -pi -e "s|^KERNEL_HEADER_DIR =.*|KERNEL_HEADER_DIR = %{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}/include|" _kmod_build_${kvariant}/src/config/site.mcr
        perl -pi -e "s|^KERNEL_BUILD_DIR =.*|KERNEL_BUILD_DIR = %{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}|" _kmod_build_${kvariant}/src/config/site.mcr
done

%build
for kvariant in %{kvariants}
do
	pushd _kmod_build_$kvariant
	./configure --with-linux=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu} --with-sockets --with-lustre-hack --sysconfdir=%{_sysconfdir} \
        --mandir=%{_mandir} --libdir=%{_libdir} --with-o2ib
	make
	popd
done

%install
# install all - we use mykvariants to make the default one last to be installed
for kvariant in %{mykvariants}
do
	pushd _kmod_build_$kvariant
	mkdir 		 -p $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/{fs,net}
        make install DESTDIR=$RPM_BUILD_ROOT
	mv $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/kernel/fs/lustre $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/fs/%{kmod_name}
	mv $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/kernel/net/lustre $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/net/%{kmod_name}
	popd
	rm -rf $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/kernel
done

# Temporarily executable for stripping, fixed later in %%files.
chmod u+x $RPM_BUILD_ROOT/lib/modules/*/extra/*/%{kmod_name}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/sbin/mount.lustre
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/liblustre.so
%dir %{_libdir}/lustre
%dir %{_libdir}/lustre/snmp
%dir %{_libdir}/lustre/liblustre
%{_libdir}/lustre/snmp/lustresnmp.so
%{_libdir}/lustre/lc_common
%{_mandir}/man*/*
%dir %{_datadir}/lustre
%dir %{_datadir}/lustre/snmp
%dir %{_datadir}/lustre/snmp/mibs
%{_datadir}/lustre/snmp/mibs/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lustre
%{_includedir}/linux/lustre*
%{_libdir}/lib*a
%{_datadir}/lustre/mpich-1.2.6-lustre.patch
%{_libdir}/lustre/tests
%{_libdir}/lustre/liblustre/tests

%changelog
* Tue Jul 07 2009 Josko Plazonic <plazonic@math.princeton.edu>
- weak updates bugfix

* Tue Jun 23 2009 Josko Plazonic <plazonic@math.princeton.edu>
- version 1.8.0.1 and weak updates test

* Wed Apr 29 2009 Josko Plazonic <plazonic@math.princeton.edu>
- build with openib

* Mon Mar 30 2009 Josko Plazonic <plazonic@math.princeton.edu>
- initial build for rhel5
