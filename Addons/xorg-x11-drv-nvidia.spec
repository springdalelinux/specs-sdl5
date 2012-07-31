%define        nvidialibdir      %{_libdir}/nvidia
%define        nvidialibdir32bit %{_prefix}/lib/nvidia

Name:          xorg-x11-drv-nvidia
Version:       195.36.15
Release:       4.1%{?dist}
Summary:       NVIDIA's proprietary display driver for NVIDIA graphic cards

Group:         User Interface/X Hardware Support
License:       Distributable
URL:           http://www.nvidia.com/
Source0:       http://us.download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}-pkg1.run
Source1:       http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-pkg2.run
Source2:       nvidia.sh
Source3:       nvidia.csh
Source4:       nvidia-settings.desktop
Source5:       nvidia-init
Source10:      nvidia-config-display
Source11:      nvidia-README.Fedora
Source12:      nvidia.opts
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: i386 x86_64
Obsoletes:     xorg-x11-drv-nvidia185
Requires:      mesa-libGL

Requires:        nvidia-kmod >= %{version}
Requires(post):  nvidia-kmod >= %{version}

# Needed in all nvidia or fglrx driver packages
BuildRequires:      desktop-file-utils
#Requires:           livna-config-display
#Requires(post):     livna-config-display
#Requires(preun):    livna-config-display
Requires(post):     chkconfig
Requires(post):     ldconfig
Requires(preun):    chkconfig

Provides:      nvidia-kmod-common = %{version}

Conflicts:     xorg-x11-drv-nvidia-legacy
Conflicts:     xorg-x11-drv-nvidia-96xx
Conflicts:     xorg-x11-drv-fglrx

Conflicts:     selinux-policy < 2.2.29-2.fc5

Obsoletes:     nvidia-glx
Obsoletes:     nvidia-kmod < %{version}

%description
This package provides the most recent NVIDIA display driver which allows for
hardware accelerated rendering with NVIDIA chipsets NV30 (FX series) and newer.
NV30 and below (such as GeForce2) are NOT supported by this release.

For the full product support list, please consult the release notes
for driver version %{version}.


%package devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Obsoletes:     xorg-x11-drv-nvidia185-devel

%description devel
This package provides the development files of the %{name} package,
such as OpenGL headers.


%ifarch x86_64
%package libs-32bit
Summary:       32 bit version of %{name}
Group:         User Interface/X Hardware Support
Requires:      %{name} = %{version}-%{release}
Obsoletes:     xorg-x11-drv-nvidia185-libs-32bit

%description libs-32bit
This package provides the 32 bit version of %{name}. Please see description
of package %{name} for more information.
%endif #x86_64


%prep
%setup -q -c -T
sh %{SOURCE0} --extract-only --target nvidiapkg-x86
sh %{SOURCE1} --extract-only --target nvidiapkg-x64
tar -cjf nvidia-kmod-data-%{version}.tar.bz2 nvidiapkg-*/LICENSE nvidiapkg-*/usr/src/

%ifarch %{ix86}
ln -s nvidiapkg-x86 nvidiapkg
%else
ln -s nvidiapkg-x64 nvidiapkg
%endif
mv nvidiapkg/LICENSE nvidiapkg/usr/share/doc/
# More docs
cp %{SOURCE11} nvidiapkg/usr/share/doc/README.Fedora
find nvidiapkg/usr/share/doc/ -type f | xargs chmod 0644

# lots of problems with providing libGL.so.1 and friends so just drop risky provides
find_provides="%{__find_provides}"
echo "#!/bin/sh" > find-provides
echo "$find_provides | grep -v libGL.so.1 | grep -v libGLcore.so.1 | grep -v libglx.so " >> find-provides
echo "exit 0" >> find-provides
chmod +x find-provides
%global _use_internal_dependency_generator 0
%define __find_provides %{_builddir}/%{name}-%{version}/find-provides

# and just in case drop also risky requires
find_requires="%{__find_requires}"
echo "#!/bin/sh" > find-requires
echo "$find_requires | grep -v libGL.so.1 | grep -v libGLcore.so.1 | grep -v libglx.so " >> find-requires
echo "exit 0" >> find-requires
chmod +x find-requires
%define __find_requires %{_builddir}/%{name}-%{version}/find-requires


%install
rm -rf $RPM_BUILD_ROOT

set +x
for file in $(cd nvidiapkg &> /dev/null; find . -type f | grep -v -e 'makeself.sh$' -e 'mkprecompiled$' -e 'tls_test$' -e 'tls_test_dso.so$' -e 'nvidia-settings.desktop$' -e '^./Makefile'  -e '^./nvidia-installer' -e '^./pkg-history.txt' -e '^./.manifest' -e '/usr/share/doc/' -e 'libGL.la$' -e 'drivers/nvidia_drv.o$' -e 'nvidia-installer.1.gz$' -e '^./usr/src/')
do
  if [[ ! "/${file##./usr/lib/}" = "/${file}" ]]
  then
    install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/%{nvidialibdir}/${file##./usr/lib/}
  elif [[ ! "/${file##./usr/X11R6/lib/modules/extensions}" = "/${file}" ]]
  then
    install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/extensions/nvidia/${file##./usr/X11R6/lib/modules/extensions}
  elif [[ ! "/${file##./usr/X11R6/lib/modules}" = "/${file}" ]]
  then
    install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/${file##./usr/X11R6/lib/modules}
  elif [[ ! "/${file##./usr/X11R6/lib/}" = "/${file}" ]]
  then
    install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/%{nvidialibdir}/${file##./usr/X11R6/lib/}
  elif [[ ! "/${file##./usr/include/}" = "/${file}" ]]
  then
    install -D -p -m 0644 nvidiapkg/${file} $RPM_BUILD_ROOT/%{_includedir}/nvidia/${file##./usr/include/}
  elif [[ ! "/${file##./etc/}" = "/${file}" ]]
  then
    install -D -p -m 0644 nvidiapkg/${file} $RPM_BUILD_ROOT/etc/${file##./etc/}
  elif [[ ! "/${file##./usr/bin/}" = "/${file}" ]]
  then
    if [[ ! "/${file##./usr/bin/nvidia-xconfig}" = "/${file}" ]]
    then
      install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/usr/sbin/${file##./usr/bin/}
    elif [[ ! "/${file##./usr/bin/nvidia-bug-report.sh}" = "/${file}" ]]
    then
      install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/usr/bin/${file##./usr/bin/}
    else
      install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/${file}
    fi
  elif [[ ! "/${file##./usr/lib32}" = "/${file}" ]]
  then
    install -D -p -m 0755 nvidiapkg/${file} $RPM_BUILD_ROOT/%{nvidialibdir32bit}/${file##./usr/lib32/}
  elif [[ ! "/${file##./usr/share/man/}" = "/${file}" ]]
  then
    install -D -p -m 0644 nvidiapkg/${file} $RPM_BUILD_ROOT/%{_mandir}/${file##./usr/share/man/}
    gunzip $RPM_BUILD_ROOT/%{_mandir}/${file##./usr/share/man/}
  elif [[ ! "/${file##./usr/share/pixmaps/}" = "/${file}" ]]
  then
    install -D -p -m 0644 nvidiapkg/${file} $RPM_BUILD_ROOT/%{_datadir}/pixmaps/${file##./usr/share/pixmaps/}
  else
    echo ${file} found -- don\'t know how to handle
    exit 1
  fi
done
set -x

# Move the libnvidia-wfb.so lib to the Nvidia xorg extension directory.
mv $RPM_BUILD_ROOT%{_libdir}/xorg/modules/libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.%{version}

# Change perms on static libs. Can't fathom how to do it nicely above.
find $RPM_BUILD_ROOT/%{nvidialibdir} -type f -name "*.a" -exec chmod 0644 '{}' \;

# Fixme: should we do this directly in above for-loop? Yes, we should! No, please don't!
ln -s libGLcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLcore.so
ln -s libGLcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGLcore.so.1
ln -s libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGL.so
ln -s libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libGL.so.1
ln -s libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-tls.so.1
ln -s libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/tls/libnvidia-tls.so.1
ln -s libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libnvidia-cfg.so.1
ln -s libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libXvMCNVIDIA.so
ln -s libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir}/libXvMCNVIDIA_dynamic.so.1
ln -s libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so
ln -s libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.1

# This is 97xx specific. libnvidia-wfb.so is a replacement of libwfb.so
# It is used by card > NV30 but required by G80 and older.
ln -s libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libwfb.so

# 32-bit libs on x86_64
%ifarch x86_64
ln -s libGLcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/libGLcore.so
ln -s libGLcore.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/libGLcore.so.1
ln -s libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/libGL.so
ln -s libGL.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/libGL.so.1
ln -s libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/libnvidia-tls.so.1
ln -s libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/tls/libnvidia-tls.so.1
ln -s libnvidia-cfg.so.%{version} $RPM_BUILD_ROOT%{nvidialibdir32bit}/libnvidia-cfg.so.1
%endif #x86_64

# profile.d files
install -D -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/nvidia.sh
install -D -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/nvidia.csh

# X configuration script
install -D -p -m 0755 %{SOURCE10} $RPM_BUILD_ROOT%{_sbindir}/nvidia-config-display

# Desktop entry for nvidia-settings
desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    --add-category X-Livna \
    --add-category System \
    --add-category Application \
    --add-category GTK \
    %{SOURCE4}

# Install initscript
#install -D -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT%{_initrddir}/nvidia

# modprobe.d file
install -D -p -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/nvidia

# ld.so.conf.d file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo "%{nvidialibdir}" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%ifarch x86_64
echo "%{nvidialibdir32bit}" >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -e %{_initrddir}/nvidia ]; then
	/sbin/chkconfig --del nvidia || :
fi

%post
/sbin/ldconfig
if [ "$1" -eq "1" ]; then
  # Enable nvidia driver when installing
  if /sbin/lsmod | grep nvidia &> /dev/null || /sbin/modprobe nvidia ; then
    %{_sbindir}/nvidia-config-display enable ||:
  fi
  # Add init script and start it
  #/sbin/chkconfig --add nvidia ||:
  #/etc/init.d/nvidia start &>/dev/null ||:
fi

%ifarch x86_64
%post libs-32bit -p /sbin/ldconfig
%endif  #x86_64

%preun
if [ "$1" -eq "0" ]; then
    # Disable driver on final removal
    #%{_initrddir}/nvidia stop &> /dev/null
    test -f %{_sbindir}/nvidia-config-display && %{_sbindir}/nvidia-config-display disable ||:
    #/sbin/chkconfig --del nvidia ||:
fi ||:

%postun -p /sbin/ldconfig
%ifarch x86_64
%postun libs-32bit -p /sbin/ldconfig
%endif  #x86_64

%files
%defattr(-,root,root,-)
%doc nvidiapkg/usr/share/doc/*
%dir %{nvidialibdir}
%dir %{nvidialibdir}/tls
%dir %{nvidialibdir}/vdpau
%dir %{_libdir}/xorg/modules/extensions/nvidia
#%{_initrddir}/nvidia
%{nvidialibdir}/*.so.*
%{nvidialibdir}/tls/*.so.*
%{nvidialibdir}/vdpau/*.so.*
%{_sysconfdir}/profile.d/nvidia*
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_libdir}/xorg/modules/extensions/nvidia/*
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/applications/*nvidia-settings.desktop
%{_datadir}/pixmaps/*.png
%config %{_sysconfdir}/ld.so.conf.d/nvidia.conf
%config %{_sysconfdir}/modprobe.d/nvidia
%{_mandir}/man[1-9]/nvidia*.*
%verify (not user) %attr(0600,root,root) %dev(c,195,0) /dev/nvidia0
%verify (not user) %attr(0600,root,root) %dev(c,195,1) /dev/nvidia1
%verify (not user) %attr(0600,root,root) %dev(c,195,2) /dev/nvidia2
%verify (not user) %attr(0600,root,root) %dev(c,195,3) /dev/nvidia3
%verify (not user) %attr(0600,root,root) %dev(c,195,255) /dev/nvidiactl
%attr(0600,root,root) %dev(c,195,0) %{_sysconfdir}/udev/devices/nvidia0
%attr(0600,root,root) %dev(c,195,1) %{_sysconfdir}/udev/devices/nvidia1
%attr(0600,root,root) %dev(c,195,2) %{_sysconfdir}/udev/devices/nvidia2
%attr(0600,root,root) %dev(c,195,3) %{_sysconfdir}/udev/devices/nvidia3
%attr(0600,root,root) %dev(c,195,255) %{_sysconfdir}/udev/devices/nvidiactl
%dir /etc/OpenCL
%dir /etc/OpenCL/vendors
/etc/OpenCL/vendors/nvidia.icd


%ifarch x86_64
%files libs-32bit
%defattr(-,root,root,-)
%dir %{nvidialibdir32bit}
%dir %{nvidialibdir32bit}/tls
%dir %{nvidialibdir32bit}/vdpau
%{nvidialibdir32bit}/*.so.*
%{nvidialibdir32bit}/tls/*.so.*
%{nvidialibdir32bit}/vdpau/*.so.*
%endif  #x86_64

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/nvidia
%dir %{_includedir}/nvidia/GL
%{_includedir}/nvidia
%{nvidialibdir}/libXvMCNVIDIA.a
%{nvidialibdir}/*.so
%ifarch x86_64
%{nvidialibdir32bit}/*.so
%endif #x86_64


%changelog
* Thu Apr 12 2007 Josko Plazonic <plazonic@math.princeton.edu>
- no need to mess with modprobe.conf

* Thu Mar  8 2007 kwizart < kwizart at gmail.com > - 1.0.9755-3
- Fix nvidia scripts rename and update init .opts

* Thu Mar  8 2007 kwizart < kwizart at gmail.com > - 1.0.9755-2
- Fix Sources URL

* Thu Mar  8 2007 kwizart < kwizart at gmail.com > - 1.0.9755-1
- Update to 1.0.9755
- sync with devel spec lcd excluded for now

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-11
- Bump for new tag
- fi to end if!

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-10
- Bump for new tag

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-9
- Standardize all summaries and descriptions with other nvidia and fglrx
  packages
- Standardize initscript and *config-display with other nvidia and fglrx
  packages
- Move paths from nvidia-glx to nvidia
- Start merge with livna-config-display

* Wed Feb 7 2007 kwizart < kwizar at gmail.com > - 1.0.9746-8
- Update SHA1SUM

* Thu Jan 18 2007 Stewart Adam <s.adam AT diffingo DOT com> - 1.0.9746-7
- Fix initscript empty line problem (#1302)
- Fix typo in the readme
- Put in correct sums into SHA1SUM

* Sun Jan 7 2007 kwizart < kwizart at gmail.com > - 1.0.9746-6
- Quick fix double libs-32bit -p /sbin/ldconfig

* Thu Jan 4 2007 kwizart < kwizart at gmail.com > - 1.0.9746-5
- Create the symlink from libwfb.so to libnvidia-wfb.so.x.y.z 
  the xorg driver search for libwfb.so (it do not use the SONAME).
  http://www.nvnews.net/vbulletin/showthread.php?t=83214

* Wed Jan 3 2007 Stewart Adam < s.adam AT diffingo DOT com  - 1.0.9746-4
- Correct mistake in changelog
- add %%verify to /dev nodes (#1324)
- /etc/profile.d/* are sourced, took away exec bit

* Wed Jan 3 2007 Stewart Adam < s.adam AT diffingo DOT com  - 1.0.9746-3
- Make the 32-bit libs run ldconfig in %%postun and %%post steps
- Possible FIXME for future: "E: xorg-x11-drv-nvidia obsolete-not-provided nvidia-glx'

* Thu Dec 28 2006 kwizart < kwizart at gmail.com > - 1.0.9746-2
- Move the libnvidia-wfb.so lib to the Nvidia xorg extension directory.

* Tue Dec 26 2006 kwizart < kwizart at gmail.com > - 1.0.9746-1
- Update to 1.0.9746 (Final).
- Fix symlink of the new lib which soname is libnvidia-wfb.so.1

* Sun Nov 26 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.9742-3
- use Source0 with "pkg0.run" prefix (smaller)
- use Source1 with "pkg2.run" prefix (cotaints the 32bit libs)

* Thu Nov 23 2006 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9742-2
- Fix URL
- Change %%description, as NV30 and below no longer supported
- Update nvidia desktop file

* Mon Nov 20 2006 kwizart < kwiart at gmail.com > - 1.0.9742-1
- Update to release 1.0.9742
- Include libdir/xorg/modules/libnvidia-wfb.so.1.0.9742

* Tue Nov 07 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.9629-1
- update to release 1.0.9629

* Tue Oct 31 2006 Dams <anvil[AT]livna.org> - 1.0.9626-3
- Another nvidia-config-display update to fix dumb modules section

* Tue Oct 24 2006 Dams <anvil[AT]livna.org> - 1.0.9626-2
- Yet another updated nvidia-config-display : importing python modules
  we use is usualy a good idea
- Updated nvidia-config-display

* Sun Oct 22 2006 Stewart Adam <s.adam AT diffingo DOT com> - 1.0.9626-1
- update to release 1.0.9626

* Fri Oct 20 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8776-1
- update to 1.0.8776-1 -- fixes CVE-2006-5379

* Thu Aug 24 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8774-1
- Nvidia added a png for nvidia-settings, for-loop adjusted accordingly
- update to release 1.0.8774

* Wed Aug 09 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-6
- small changes to sync with legacy package
- place nvidia-bug-report.sh in /usr/bin

* Mon Aug 07 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-5
- more minor changes to spacing and general layout

* Fri Aug 04 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-4
- minor changes to spacing, removal of random tabs, re-arrangements
- remove GNOME category from the desktop file

* Thu May 25 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8762-3
- Obsolete old kmods

* Thu May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8762-2
- add missing defattr to files section for sub-package libs-32bit

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8762-1
- update to 1.0.8762

* Tue May 16 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8756-3
- Conflict with xorg-x11-drv-fglrx and selinux-policy < 2.2.29-2.fc5
- Ship bug-reporting tool as normal executable and not in %%doc

* Sun May 14 2006 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 1.0.8756-2
- Require nvidia-kmod instead of kmod-nvidia (#970).

* Sat Apr 08 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8756-1
- Update to 8756
- put 32bit libs in their own package

* Wed Mar 29 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8178-9
- make every use of the 'install' command consistent
- tweak nvidia-settings' desktop file slightly

* Thu Mar 23 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8178-8
- switch to using modprobe.d rather than editing modprobe.conf directly

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-7
- ExclusiveArch i386 and not %%{ix86} -- we don't want to build for athlon&co

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-6
- drop unused patches

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-5
- drop 0.lvn

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Feb 08 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.5
- use lib64 in nvidia-config-display on x86-64
- fix path to kernel module in init-script
- add patch from Ville for nvidia-README.Fedora
- match permissions of xorg 7

* Wed Feb 01 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.4
- More fixes

* Tue Jan 31 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.3
- Fix wrong provides

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.2
- fix path to kernel module in nvidia-glx-init (thx to Dominik 'Rathann'
  Mierzejewski)
- include device files until udev works probably with kernel module

* Sun Jan 22 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.1
- split into packages for userland and kmod
- rename to xorg-x11-drv-nvidia; yum/rpm should use mesa-libGL{,-devel} then in
  the future when seaching for libGL.so{,.1}
- remove kernel-module part
- remove old cruft
- install stuff without Makefile because it forgets mosts a lot of files anyway

* Thu Dec 22 2005 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 0:1.0.8178-0.lvn.2
- change nvidia-glx.sh and nvidia-glx.csh to point to README.txt rather than README
- reference xorg.conf rather than XF86Config in the init script
- improve readability of instructions and comments, fix some typos
- drop epoch, as it seems to be affecting dependencies according to rpmlint
- tweak the nvidia-settings desktop file so it always shows up on the
  menu in the right location
- add the manual pages for nvidia-settings and nvidia-xconfig
- remove header entries from the nvidia-glx files list. they belong in -devel
- fix changelog entries to refer to 7676 not 7176 (though there was a 7176 x86_64
  release prior to 7174)
- add libXvMCNVIDIA.so
- update to 8178

* Wed Dec 07 2005 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 0:1.0.8174-0.lvn.1
- add the manual pages for nvidia-settings and nvidia-xconfig
- install the new nvidia-xconfig utility and associated libs

* Mon Dec 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.8174-0.lvn.1
- Update to 8174
- desktop entry now Categories=Settings (#665)
- Ship bug-reporting tool in doc (#588)
- Things from Bug 635, Niko Mirthes (straw) <nmirthes AT gmail DOT com>:
-- avoid changing time stamps on libs where possible
-- only add /etc/modprobe.conf entries if they aren't already there
-- add /etc/modprobe.conf entries one at a time
-- only remove /etc/modprobe.conf entries at uninstall, not during upgrade
-- avoid removing any modprobe.conf entries other than our own
-- match Xorg's install defaults where it makes sense (0444)
-- a few other minor tweaks to the files lists

* Sun Sep 04 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.3
- Conflics with nvidia-glx-legacy
- Integrate some minor correction suggested by Niko Mirthes
  <nmirthes AT gmail DOT com> in #475

* Fri Aug 26 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.2
- Rename src5: nvidia.init to nvidia-glx-init
- Fix correct servicename in nvidia-glx-init
- Run nvidia-glx-init before gdm-early-login; del and readd the script
  during post

* Sun Aug 21 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.1
- Update to 7676
- Lots of cleanup from me and Niko Mirthes <nmirthes AT gmail DOT com>
- add NVreg_ModifyDeviceFiles=0 to modprobe.conf (Niko)
- Drop support for FC2
- Nearly proper Udev-Support with workarounds around FC-Bug 151527

* Fri Jun 17 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.5
- Slight change of modprobe.conf rexexp

* Thu Jun 16 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.4
- Fixed a critical bug in modprobe.conf editing where all lines starting with alias and
  ending with then a word starting with any of the letters n,v,i,d,i,a,N,V,r,e is removed.

* Mon Jun 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7174-0.lvn.3
- Adjust kenrnel-module-stuff for FC4
- Ship both x86 and x64 in the SRPM

* Sun Jun 12 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.2
- Only create 16 devices
- Put libXvMCNVIDIA.a in -devel
- Don't remove nvidia options in /etc/modprobe.conf
- Make ld.so.conf file config(noreplace)
- Use same directory permissions as the kernel

* Sat Apr 2 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.1
- New upstream release, 7174

* Wed Mar 30 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.5
- Added x86_64 support patch from Thorsten Leemhuis

* Wed Mar 23 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.4
- Fix kernel module permissions again (644)
- Only create 16 /dev/nvidia* devices, 256 is unnecessary

* Fri Mar 18 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.3
- Fixed kernel-module permissions

* Thu Mar 17 2005 Dams <anvil[AT]livna.org> 0:1.0.7167-0.lvn.2
- Removed provides on kernel-module and kernel-modules

* Sat Mar 05 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.1
- New upstream release 1.0.7167
- Added patch from http://www.nvnews.net/vbulletin/showthread.php?t=47405
- Removed old patch against 2.6.9

* Sat Feb 05 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.7
- Added a number of post-6629 patches from http://www.minion.de/files/1.0-6629
- Fixed permissions of nvidia/nvidia.ko

* Fri Jan 21 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.6
- Fix incorrect MAKDEV behaviour and dependency

* Tue Nov 30 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.4
- Fixed creation of /dev/nvidia* on FC2

* Sat Nov 27 2004 Dams <anvil[AT]livna.org> - 0:1.0.6629-0.lvn.3
- Dont try to print kvariant in description when it's not defined.

* Sun Nov 21 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:1.0.6629-0.lvn.2
- resulting kernel-module package now depends again on /root/vmlinuz-<kernelver>
- Use rpmbuildtags driverp and kernelp

* Sat Nov 06 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.1
- New upstream version, 1.0-6629
- Build without kernel-module-devel by default

* Fri Oct 29 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.6
- Make n-c-display handle misc problems in a better way
- Fixed wrong icon file name in .desktop file
- Re-added the mysteriously vanished sleep line in the init script
  when kernel module wasn't present

* Fri Oct 22 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:1.0.6111-0.lvn.5
- Use fedora-kmodhelper in the way ntfs or ati-fglrx use it
- Allow rpm to strip the kernel module. Does not safe that much space ATM but
  might be a good idea
- Allow to build driver and kernel-module packages independent of each other
- Some minor spec-file changes

* Thu Oct 21 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.4
- udev fixes
- Incorporated fix for missing include line in ld.so.conf from ati-fglrx spec (T Leemhuis)

* Sun Sep 19 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.3
- Remove FC1/kernel 2.4 compability
- Rename srpm to nvidia-glx
- Build with kernel-module-devel

* Sun Aug 15 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.2
- Restore ldsoconfd macro
- Disable autoamtic removal of scripted installation for now; needs testing

* Sat Aug 14 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.1
- Upstream release 6111
- Fixed init script (again)

* Tue Aug  3 2004 Dams <anvil[AT]livna.org> 0:1.0.6106-0.lvn.4
- ld.so.conf.d directory detected by spec file
- Using nvidialibdir in nvidia-glx-devel files section
- Got rid of yarrow and tettnang macros
- libGL.so.1 symlink in tls directory always present

* Mon Jul 19 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.3
- Fixed script bug that would empty prelink.conf
- Added symlink to non-tls libGL.so.1 on FC1

* Tue Jul 13 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.3
- Updated init script to reflect name change -xfree86 -> -display

* Mon Jul 12 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.2
- Fixed backup file naming

* Sun Jul 11 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.1
- Restore working macros
- Always package the gui tool

* Sun Jul 11 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2
- Renamed nvidia-config-xfree86 to nvidia-config-display
- Fixed symlinks
- Use ld.so.conf.d on FC2
- Remove script installation in pre
- Use system-config-display icon for nvidia-settings
- 2 second delay in init script when kernel module not found
- Make nvidia-config-display fail more gracefully
- Add blacklist entry to prelink.conf on FC1

* Mon Jul 05 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.1
- New upstream release
- First attempt to support FC2
- Dropped dependency on XFree86

* Mon Feb 09 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.5336-0.lvn.3
- Use pkg0

* Sun Feb 08 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.5336-0.lvn.2
- New Makefile variable SYSSRC to point to kernel sources.
- kmodhelper fixes.

* Fri Jan 30 2004 Keith G. Robertson-Turner <nvidia-devel[AT]genesis-x.nildram.co.uk> 0:1.0.5336-0.lvn.1
- New upstream release
- Removed (now obsolete) kernel-2.6 patch
- Install target changed upstream, from "nvidia.o" to "module"
- Linked nv/Makefile.kbuild to (now missing) nv/Makefile

* Sun Jan 25 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.18
- Updated nvidia-config-display
- Now requiring pyxf86config

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.17
- Added nvidiasettings macro to enable/disable gui packaging

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.16
- Updated minion.de patches
- Added some explicit requires
- Test nvidia-config-xfree86 presence in kernel-module package
  scriptlets

* Mon Jan 12 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.15
- Updated Readme.fedora
- nvidia-glx-devel package

* Sat Jan  3 2004 Dams <anvil[AT]livna.org> 0:1.0.5328-0.lvn.14
- Hopefully fixed kernel variant thingy

* Fri Jan  2 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.13
- Support for other kernel variants (bigmem, etc..)
- Changed URL in Source0

* Tue Dec 30 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.13
- Dropped nvidia pkgX information in release tag.

* Tue Dec 30 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.12.pkg0
- Renamed kernel module package in a kernel-module-nvidia-`uname -r` way
- Using fedora.us kmodhelper for kernel macro
- Using nvidia pkg0 archive

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.11.pkg1
- kernel-module-nvidia package provides kernel-module
- We wont own devices anymore. And we wont re-create them if they are
  already present

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.10.pkg1
- Yet another initscript update. Really.
- Scriptlets updated too

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.9.pkg1
- Fixed alias in modprobe.conf for 2.6

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.8.pkg1
- Another initscript update

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.7.pkg1
- kernel module requires kernel same kversion
- initscript updated again
- Dont conflict, nor obsolete XFree86-Mesa-libGL. Using ld.so.conf to
  make libGL from nvidia first found. Hope Mike Harris will appreciate.

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.6.pkg1
- kernel-module-nvidia requires kernel same version-release

* Sat Dec 20 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.6.pkg1
- Updated initscript

* Fri Dec 19 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.5.pkg1
- lvn repository tag

* Fri Dec 19 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.5.pkg1
- Added initscript to toggle nvidia driver according to running kernel
  and installed kernel-module-nvidia packages
- Updated scriptlets

* Thu Dec 18 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.4.pkg1
- Arch detection
- Url in patch0

* Tue Dec 16 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.3.pkg1
- Desktop entry for nvidia-settings
- s/kernel-module-{name}/kernel-module-nvidia
- nvidia-glx doesnt requires kernel-module-nvidia-driver anymore
- Using modprobe.conf for 2.6 kernel
- Hopefully fixed symlinks

* Mon Dec 15 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.2.pkg1
- Building kernel module for defined kernel
- kernel module for 2.6 is nvidia.ko
- Patch not to install kernel module on make install
- Updated patch for 2.6
- depmod in scriptlet for defined kernel
- nvidia-glx conflicting XFree86-Mesa-libGL because we 0wn all its
  symlink now
- Dont override libGL.so symlink because it belongs to XFree86-devel
- Added nvidia 'pkgfoo' info to packages release
- Spec file cleanup

* Fri Dec 12 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4620-0.fdr.2
- Fixed repairing of a link in post-uninstall
- Obsolete Mesa instead of Conflict with it, enables automatic removal.

* Mon Dec 08 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4620-0.fdr.1
- Added support for 2.6 kernels
- Cleaned up build section, removed the need for patching Makefiles.
- Added missing BuildReq gcc32
- Don't package libs twice, only in /usr/lib/tls/nvidia
- Made config cript executable and put it into /usr/sbin
- Moved kernel module to kernel/drivers/video/nvidia/
- Fixed libGL.so and libGLcore.so.1 links to allow linking against OpenGL libraries

* Mon Dec 08 2003 Keith G. Robertson-Turner <nvidia-devel at genesis-x.nildram.co.uk> - 0:1.0.4620-0.fdr.0
- New beta 4620 driver
- New GUI control panel
- Some minor fixes

* Thu Nov 20 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.10.1
- Finally fixed SMP builds.

* Wed Nov 19 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.9
- Don't make nvidia-glx depend on kernel-smp

* Tue Nov 18 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.8
- Some build fixes

* Tue Nov 11 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.7
- Added CC=gcc32
- Fixed upgrading issue
- Added driver switching capabilities to config script.

* Fri Nov 07 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.4
- Added conflict with XFree86-Mesa-libGL.
- Disabled showing of the README.Fedora after installation.

* Sun Oct 12 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.3
- Added NVidia configuration script written in Python.
- Some cleanup of files section
- For more info, see https://bugzilla.fedora.us/show_bug.cgi?id=402

* Tue Jul 08 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> - 0:1.0.4363-0.fdr.2
- renamed /sbin/makedevices.sh /sbin/nvidia-makedevices.sh ( noticed by
  Panu Matilainen )
- Fixed name problem
* Sun Jun 22 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> - 0:1.0.4363-0.fdr.1
- Initial RPM release, still some ugly stuff in there but should work...
