Source10: kmodtool
%define kmodtool bash %{SOURCE10}
%{!?kversion: %define kversion 2.6.18-308.8.1.el5}
# as our release is 128 or higher we stop at 99 below:
%define gpfskernelversion 2061899
# hint: this can he overridden with "--define kversion foo" on the rpmbuild command line, e.g.
# --define "kversion 2.6.16-1.2096_FC5"

%define kmod_name gpfs
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""
%ifarch ppc
%define smpvar smp
%endif
%ifarch i686 x86_64 ia64
# we do not build xen variant any more - why bother
#define xenvar xen
#define kdumpvar kdump
%endif
%ifarch i686
%define PAEvar PAE
%endif
%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?kdumpvar} %{?PAEvar}}
# hint: this can he overridden with "--define kvariant foo bar" on the rpmbuild command line, e.g.
# --define 'kvariant "" smp' 

# hacks to work around ksym dependency issues
%define my_requires %{_builddir}/my_requires
%define _use_internal_dependency_generator 0

# minor gpfs version
%define subversion 23
# we need this
%define mrelease %{subversion}.11%{?dist}

Name:		gpfs-princeton
Summary:	The kernel module for GPFS
Version:	3.3.0
Release:        %{mrelease}
License:	LGPL/GPL
Group: 		System Environment/Base
URL: 		http://www.pvfs.org/pvfs2/
#Source0:	gpfs.gpl-%{version}-%{subversion}.noarch.rpm
#Source1:	gpfs.base-%{version}-%{subversion}.i386.rpm
#Source2:	gpfs.base-%{version}-%{subversion}.x86_64.rpm
Source100:	gpfs-kernel-setup.init
Buildroot:	%{_tmppath}/%{name}-buildroot
ExclusiveArch:  x86_64
BuildRequires:	imake ksh 
BuildRequires:	gpfs.base = %{version}-%{subversion}
BuildRequires:	gpfs.gpl = %{version}-%{subversion}
Requires:	gpfs.base = %{version}-%{subversion}

%description
The kernel module for GPFS

# magic hidden here:
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%prep
%setup -n %{name}-%{version}-%{subversion} -c -T
%{__cat} <<EOF >%{my_requires}
#!/bin/sh
%{__find_requires} | egrep -v '^ksym\((__setlease|relay_subbufs_consumed|vfs_write)\)'
exit 0
EOF
chmod +x %{my_requires}
%define __find_requires %{my_requires}
mkdir kernel
cd kernel
mkdir usr
cp -ar /usr/lpp usr/ || :
#rpm2cpio %{SOURCE0} | cpio -i -d
#rpm2cpio %{SOURCE2} | cpio -i -d
pushd usr/lpp/mmfs/
# begin with local configs
cp ./src/config/env.mcr.sample ./src/config/env.mcr
%ifarch x86_64
        perl -pi -e 's|^#define GPFS_ARCH_.*|#define GPFS_ARCH_X86_64|' src/config/env.mcr
%endif
        perl -pi -e 's|^LINUX_DISTRIBUTION = .*|LINUX_DISTRIBUTION = REDHAT_AS_LINUX|' src/config/env.mcr
        perl -pi -e 's|^#define LINUX_KERNEL_VERSION .*|#define LINUX_KERNEL_VERSION %{gpfskernelversion}|' src/config/env.mcr
popd
cd ..
for kvariant in %{kvariants} ; do
    cp -a kernel _kmod_build_${kvariant}
        perl -pi -e "s|^KERNEL_BUILD_DIR =.*|KERNEL_BUILD_DIR = %{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}|" _kmod_build_${kvariant}/usr/lpp/mmfs/src/config/env.mcr
done

%build
for kvariant in %{kvariants}
do
    pushd _kmod_build_$kvariant/usr/lpp/mmfs/src
    make World
    popd
done

%install
# install modules
for kvariant in %{kvariants}
do
	pushd _kmod_build_$kvariant/usr/lpp/mmfs/src
	mkdir 		 -p $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/
	for i in tracedev.ko mmfslinux.ko mmfs26.ko; do
                install -m 644 gpl-linux/$i $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/
        done
	mkdir 		 -p $RPM_BUILD_ROOT/usr/lpp/mmfs/bin
	install -m 755 bin/lxtrace-2.6* bin/kdump-2.6* $RPM_BUILD_ROOT/usr/lpp/mmfs/bin/
	popd
done
# install the rest
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE100} $RPM_BUILD_ROOT%{_initrddir}/gpfs-kernel-setup

# Temporarily executable for stripping, fixed later in %%files.
chmod u+x $RPM_BUILD_ROOT/lib/modules/*/extra/*

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/chkconfig --add gpfs-kernel-setup

%postun -p /sbin/ldconfig

%preun
if [ "$1" -eq 0 ]; then
	/sbin/chkconfig --del gpfs-kernel-setup
fi

%files
%defattr(-,root,root,-)
%{_initrddir}/gpfs-kernel-setup
#/usr/lpp/mmfs/bin/lxtrace
#/usr/lpp/mmfs/bin/dumpconv

%changelog
* Fri Aug 14 2009 Josko Plazonic <plazonic@math.princeton.edu>
- new gpfs version

* Mon Mar 30 2009 Josko Plazonic <plazonic@math.princeton.edu>
- initial build for rhel5
