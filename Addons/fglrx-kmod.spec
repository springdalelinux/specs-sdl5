# stuff to be implemented externally:
Source10: kmodtool
%define   kmodtool bash %{SOURCE10}
# end stuff to be ...

# hardcode for now:
%{!?kversion: %define kversion 2.6.18-164.el5}

%define kmod_name fglrx
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""
%ifarch ppc
%define smpvar smp
%endif
%ifarch i686
%define PAEvar PAE
%endif
%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?kdumpvar} %{?PAEvar}}
# hint: this can he overridden with "--define kvariant foo bar" on the rpmbuild command line, e.g.
# --define 'kvariant "" smp'

Name:           fglrx-kmod
Version:        8.455.2
Release:        2%{?dist}
# Taken over by kmodtool anyways
Summary:        ATI display driver kernel module

Group:          System Environment/Kernel
License:        Distributable
URL:            http://www.ati.com/support/drivers/linux/radeon-linux.html

Source0:        http://www.diffingo.com/downloads/livna/kmod-data/fglrx-kmod-data-%{version}.tar.bz2
Patch1:         fglrx-makefile.diff
Patch2:         fglrx-makesh.diff
Patch10:        fglrx-via_int_agpgart.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch:  i586 i686 x86_64

%description
This package provides the driver ATI driver for accelerated
OpenGL support with ATI hardware supporting from the Radeon
9500 series to the Radeon X1900 series among others such
as mobility and integrated products.
This package is built for the %{_target_cpu}, kernel version %{kernel}

# magic hidden here:
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%prep
# to understand the magic better or to debug it, uncomment this:
%{kmodtool} rpmtemplate %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null
#sleep 5
%setup -q -c -T -a 0
mkdir fglrxpkg
%ifarch %{ix86}
cp -r fglrx/common/* fglrx/arch/x86/* fglrxpkg/
%endif

%ifarch x86_64
cp -r fglrx/common/* fglrx/arch/x86_64/* fglrxpkg/
%endif

for kvariant in %{kvariants} ; do
    cp -a fglrxpkg/ _kmod_build_$kvariant
    pushd _kmod_build_$kvariant
    find lib/modules/fglrx/build_mod/ usr/share/doc  -type d -print0 | xargs -0 chmod 0755
    find lib/modules/fglrx/build_mod/ -type f -print0 | xargs -0 chmod 0644
    pushd lib/modules/fglrx/build_mod/
kversion=%{kversion}
#sed -i 's!#include <linux/config.h>!!' $(grep -r '#include <linux/config.h>' . | sed 's!:#include <linux/config.h>!!')
%patch1 -b .patch1
%patch2 -b .patch2
#patch10 -p1 -b .patch10
    popd
    popd
done


%build
for kvariant in %{kvariants}
do
    ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}
    pushd _kmod_build_$kvariant/lib/modules/fglrx/build_mod/
    export AS_USER=y
    export KERNEL_PATH="${ksrc}"
    export FEDORA_UNAME_R="%{kverrel}${kvariant:+-$kvariant}"
    export FEDORA_UNAME_M="%{_target_cpu}"
    export CC="gcc"
    bash make.sh verbose
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kvariant in %{kvariants}
do
    install -D -m 0644 _kmod_build_$kvariant/lib/modules/fglrx/build_mod/2.6.x/fglrx.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}/fglrx.ko
done
chmod u+x $RPM_BUILD_ROOT/lib/modules/*/extra/%{kmod_name}/*


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Sep 03 2009 Josko Plazonic <plazonic@math.princeton.edu>
- convert to weak updates kmod

* Sun Feb 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-1
- Update to 8.34.8
- Move paths and names to plain fglrx, not ati-fglrx, the driver's name's
  long changed!
- Product support in %%description...
- Conditional patch for 2.6.20

* Sat Feb 17 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-2
- Change descriptions to more informative, easy-to-understand ones

* Fri Jan 12 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-1
- Update to 8.33.6

* Fri Nov 17 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-1
- Update to 8.31.5, patch from Edgan in #livna

* Sat Oct 14 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.29.6-1
- Update to 8.29.6 (needed for 2.6.18 suppport/FC6)

* Fri Aug 18 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.28.8-1
- Update to 8.28.8
- refactored %%prep now that ATi's installer has merged arches

* Thu Aug 10 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-3
- update for kernel 2.6.17-1.2174_FC5

* Sat Aug 05 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-2
- no i586 on fc5

* Sun Jul 30 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-1
- Update to 8.27.10
- removal of random tabs

* Tue Jun 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.26.18-1
- Update to 8.26.18

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.25.18-2
- Invoke kmodtool with bash instead of sh.

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.25.18-1
- Update to 8.25.18
- drop patch25

* Thu May 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.24.8-3
- Require version >= of fglrx-kmod-common.
- Provide fglrx-kmod instead of kmod-fglrx to fix upgrade woes (#970).

* Thu Apr 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.24.8-2
- Provide "kernel-modules" instead of "kernel-module" to match yum's config.

* Sat Apr 15 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.24.8-1
- Update to 8.24.8
- Remove old patches, x86_64 patch still needed

* Thu Mar 23 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.23.7.1-4
- apply patches that might fix x86_64 at least for some people

* Thu Mar 23 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.23.7.1-3
- disable xen0, too

* Wed Mar 22 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.23.7.1-2
- allow to pass kversion and kvariants via command line
- disable x86_64 (build problem)

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7.1-1
- drop 0.lvn
- drop ati-fglrx-get_page.patch patch
- update to 8.23.7
- hardcode kversion and kvariants

* Wed Feb 08 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.2
- add ati-fglrx-accessok.patch

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- split into packages for userland and kmod
- rename to fglrx-kmod

* Mon Dec 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.3
- Add patch for kernel 2.6.15

* Tue Dec 13 2005 Dams <anvil[AT]livna.org> - 8.20.8.1-0.lvn.2
- Really dropped Epoch

* Sat Dec 10 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- Update to 8.20.8-1
- Drop Epoch

* Sun Nov 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.19.10.1-0.lvn.2
- Patch for 2.6.14 still needed on x86_64 (thx Ryo Dairiki for noticing)

* Sat Nov 12 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.19.10.1-0.lvn.1
- Update to 8.19.10-1
- Remove patches for 2.6.14
- Add fresh translation to desktop-file

* Wed Nov 09 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.18.6.1-0.lvn.2
- Patch kernel-module source to compile with 2.6.14

* Thu Oct 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.18.6.1-0.lvn.1
- Update to 8.18.6-1
- Conflict with nvidia-glx{,-legacy) (#627)
- Fix moduleline.split in ati-fglrx-config-display (#582)
- Unload drm in ati-fglrx-config-display, too
- Only ship self compiled fireglcontrolpanel

* Fri Aug 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.16.20.1-0.lvn.1
- Update to 8.16.20-1
- Update patch1, fireglcontrol.desktop
- Don't strip kernel-module for now

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.5
- Update fglrx-2.6.12-inter_module_get.patch (thx to Mike Duigou)

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.4
- Add patches from http://ati.cchtml.com/show_bug.cgi?id=136 and some tricks
  to built with 2.6.12 -- fixes building for FC4

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.3
- Missed one thing during reword of kernel-module-build-stuff
- Both x86_64 and x86 in the same package now

* Sun Jun 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.2
- Fix thinko

* Sun Jun 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.1
- Rework kernel-module-build-stuff for FC3 kmd and FC4 and new livna scheme
- Simplify the install; Lowers risk to miss files and is easier to maintain
- Remove dep on fedora-rpmdevtools
- Use modules and userland rpmbuild parameter to not build kernel- or driver-package

* Wed May 04 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.12.10.1-0.lvn.2
- Add fix for kernel 2.6.11

* Fri Apr 08 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.12.10.1-0.lvn.1
- Update to 8.12.10-1
- mod 0755 dri.so to let rpm detect require libstdc++.so.5

* Thu Mar 06 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.10.19.1-0.lvn.2
- Add patch for via agpgart (#355)

* Thu Feb 17 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.10.19.1-0.lvn.1
- Update to 8.10.19-1
- Remove patch for 2.6.10 kernel
- require libstdc++.so.5

* Wed Jan 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.4
- fix x86-64 in spec-file and in ati-fglrx-config-display
- Fix by Ville Skyttä: ldconfig on upgrades

* Wed Jan 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.3
- Package library links

* Wed Jan 19 2005 Dams <anvil[AT]livna.org> - 0:8.8.25.1-0.lvn.2
- Urlized ati rpm source

* Sat Jan 15 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.1
- Update to 8.8.25
- Remove workaround from last version
- Remove special drm includes
- Prepare package for 64-bit version; But untested ATM
- Update patches

* Tue Jan 11 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.3
- add patch10 -- allows building on 2.6.10; Found:
  http://www.rage3d.com/board/showthread.php?t=33798874&highlight=2.6.10
- update drm-includes
- temporary for kernel-module:  Requires: ati-fglrx >= %%{epoch}:%%{version}-0.lvn.2
  so we don't have to rebuild the driver package

* Sun Nov 21 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.2
- Use kernelp and driverp rpmbuild parameter to not build kernel- or
  driver-package
- Trim doc in header

* Fri Nov 04 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.1
- Update to 3.14.6

* Fri Nov 04 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.7
- Build per default without kmoddev
- Rename --without tools to --without dirverp
- Update dri-headers to 2.6.9 version
- update building documentation in header

* Fri Oct 22 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.6
- Some small cleanups to various parts of the package as suggested by Dams

* Fri Oct 22 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.5
- Enhance makefile patch so building with different uname should work correctly
- Build verbose

* Thu Oct 21 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.4
- Update fedora-unrpm usage to work with newer version
- Update one para in README and ati-fglrx-config-display output

* Fri Oct 15 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.3
- Change the enabling/disabling methode again -- driver is changed now
  directly. DRI is enabled when fglrx is enabled, but try to unload/warn if
  radeon kernel-module is loaded. DRI will be disabled and reenabled on the
  when next restart when disableing fglrx driver.
- Update README.fglrx.Fedora

* Mon Oct 11 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.2
- Let new version of ati-flrx-config-display change default depth to 24
- Updated Spec-File bits: fedora-kmodhelper usage and building description

* Thu Sep 30 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.1
- Update to 3.14.1
- In expectation of missing kernel-sourcecode package in FC3 remove the BR
  on it and include the neccessary header-files in the package. Will
  integrate more packages if there are API changes. But for now I
  think this is the easiest methode.
- Let ati-flrx-config-display handle /etc/ld.so.conf.d/ati-fglrx.conf
- Update ati-flrx-config-display; it adds a VideoOverlay Option now
  so xv works out of the box
- Don't (de)activate driver if DRI-Kernel-Modules are loaded; Let the
  init script to that during restart
- Update README.fglrx.Fedora

* Wed Sep 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.12.0-0.lvn.2
- Allow rpm to strip the kernel module.
- Fix shared library permissions.
- Split Requires(post,postun) to two to work around a bug in rpm.
- Fix -devel dependencies and kernel module package provisions.
- Improve summary and description, remove misleading comments.

* Sat Sep 11 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.12.0-0.lvn.1
- Update to 3.12.0
- Fix some fedora-kmodhelper/kernel-module related bits in spec
- Clean up install part a bit more

* Sun Sep 05 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.6
- Add stupid ati-fglrx.profile.d workaround for systems that had the
  original fglrx drivers installed before
- Conflict with fglrx -- the package should be removed so it can clean up
  the mess it did itself.
- Clean up desktop file

* Tue Aug 24 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.5
- Add ifdefs so building tools and kernel-module can be separated
- BuildRequire kernel-sourcecode kverrel, not kernel

* Wed Aug 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.4
- Fixed double release in Requires of devel-package
- Building against custom kernels now should work using rhkernel-macro
- Updated fedora-kmodhelper to 0.9.10
- Add 'include ld.so.conf.d/*.conf' before /usr/lib/X11 in /etc/ld.so.conf if
  it does not exists

* Wed Aug 10 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.3
- small fixes for dump issues

* Thu Aug 09 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.2
- BuildRequire fedora-rpmdevtools
- Use KERNEL_PATH correctly, needs updated patch1

* Sat Aug 07 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.1
- Update to 3.11.1
- Minor fixes

* Fri Aug  6 2004 Dams <anvil[AT]livna.org> 0:3.9.0-0.lvn.4
- .a files are 0644 moded. tgz files too.
- Added missing BuildReq: desktop-file-utils, qt-devel, fedora-rpmdevtools

* Mon Jul 19 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.3
- Update Patches to a working solution
- Modify start-script-- fglrx can also work without kernel-module (no DRI then)

* Sun Jul 18 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.2
- intergrate Readme, init-script and ati-fglrx-config-display (stolen from
  nvidia package)

* Sat Jul 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.1
- Initial RPM release.
