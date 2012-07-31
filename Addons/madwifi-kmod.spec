Source10: kmodtool
%define kmodtool bash %{SOURCE10}
%{!?kversion: %define kversion 2.6.18-164.el5}

%define kmod_name madwifi

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

# PU_IAS
%define mversion 0.9.4.5.2
%define svnversion madwifi-ng-r3695-20080602
# /PU_IAS
Name:           %{kmod_name}-kmod
Release:        6%{?dist}
Version: %{mversion}
License: Other
#Source: %{kmod_name}-%{version}.tar.bz2
Source: madwifi-ng-current.tar.bz2
Patch2: %{kmod_name}-svnversion.patch
BuildRoot: %{_tmppath}/%{name}-root
ExclusiveArch: i686 x86_64
Group: System Environment
Summary: Madwifi drivers for atheros based wireless cards
BuildRequires: kernel-devel, sharutils

%description
** BUILT FOR PRIVATE PU_IAS USE, REDISTRIBUTION NOT ALLOWED **
        ** PU_IAS NOT RESPONSIBLE FOR REDISTRIBUTION **

Atheros wireless network driver

# magic hidden here: - this is rh
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%prep
%setup -q -c -n %{kmod_name}-kmod
pushd %{svnversion}
%patch2 -p1 -b .pu_ias
popd
for kvariant in %{kvariants}
do
	cp -a %{svnversion} _kmod_build_${kvariant}
done

%build
echo starting build
for kvariant in %{kvariants}
do
    ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}
    pushd _kmod_build_$kvariant
    #./configure --kernel_src=${ksrc} --libdir=%{_libdir} --incdir=%{_includedir}
    KERNELPATH=${ksrc} make -C "${ksrc}" SUBDIRS=${PWD} modules %{?_smp_mflags}
    popd
done
echo done build

%install
for kvariant in %{kvariants}
do
	pushd _kmod_build_$kvariant
	test -d $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/madwifi    || mkdir -p $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/madwifi
	install -m 644 net80211/*.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/madwifi
	install -m 644 ath/*.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/madwifi
	install -m 644 ath_rate/sample/*.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/madwifi
	install -m 644 ath_hal/ath_hal.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/madwifi
	popd
done

%post
/sbin/depmod -ae

%clean
rm -rf $RPM_BUILD_ROOT

#%files -n kernel-%{name}
#%defattr(-,root,root)
#%doc README COPYRIGHT
#/lib/modules/%{kversion}/kernel/drivers/net/wireless/madwifi/*

%changelog
* Fri Feb 25 2005 Thomas Uphill <uphill@ias.edu>
- updated to 0.9.4.12

* Sun Sep 05 2004 Josko Plazonic <plazonic@math.princeton.edu>
- upgraded to 0.9.3.1

* Tue Jul 13 2004 Thomas Uphill <uphill@math.ias.edu>
- updated to version 0.8.6.1

* Mon May 03 2004 Josko Plazonic <plazonic@math.princeton.edu>
- updated to version 0.8.5.4

* Tue Jul 08 2003 Thomas Uphill <uphill@ias.edu>
- Initial version
