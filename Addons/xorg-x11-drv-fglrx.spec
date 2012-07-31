%define          atilibdir       %{_libdir}/fglrx
%define          atilibdir32bit  %{_prefix}/lib/fglrx

# we need this to remove libGL.so from provides
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}

Name:           xorg-x11-drv-fglrx
Version:        8.455.2
%define newativersion 8-02
Release:       13%{?dist}
Summary:    AMD's proprietary driver for ATI graphic cards
Group:          User Interface/X Hardware Support
License:        BSD/Commercial/GPL/QPL
URL:               http://www.ati.com/support/drivers/linux/radeon-linux.html

Source0:       https://a248.e.akamai.net/f/674/9206/0/www2.ati.com/drivers/linux/ati-driver-installer-%{newativersion}-x86.x86_64.run
Source1:	filterprovides.sh
Source3:       fglrx-README.Fedora
Source10:     fglrx-config-display
Source11:     fglrx-init
Source12:     fglrx.profile.d
Source13:     fglrx-atieventsd.init
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  x86_64 i386

#BuildRequires:      qt-devel, mesa-libGLU-devel, mesa-libGL-devel
#BuildRequires:      libXmu-devel, libXxf86vm-devel

Requires:               fglrx-kmod >= %{version}
Requires(post):   fglrx-kmod >= %{version}

# Needed in all nvidia or fglrx driver packages
BuildRequires:      desktop-file-utils
#Requires:               livna-config-display
#Requires(post):   livna-config-display
#Requires(preun): livna-config-display
Requires(post):   chkconfig
Requires(post):   ldconfig
Requires(preun): chkconfig

Provides:        fglrx-kmod-common = %{version}
Conflicts:        xorg-x11-drv-nvidia
Conflicts:        xorg-x11-drv-nvidia-legacy
Conflicts:        xorg-x11-drv-nvidia-96xx
Conflicts:        selinux-policy < 2.2.29-2.fc5
Obsoletes:     ati-fglrx
Obsoletes:     fglrx-kmod < %{version}
# ATI auto-generated RPMs
Conflicts:        ATI-fglrx
Conflicts:        ATI-fglrx-control-panel
Conflicts:        ATI-fglrx-devel
Conflicts:        kernel-module-ATI-fglrx
%ifarch x86_64
Conflicts:        ATI-fglrx-IA32-libs
%endif

%description
This package provides the most recent proprietary AMD display driver which
allows for hardware accelerated rendering with ATI Mobility, FireGL and
Desktop GPUs. Some of the Desktop and Mobility GPUs supported are the
Radeon 9500 series to the Radeon X1900 series.

For the full product support list, please consult the release notes
for release %{version}.


%package devel
Summary:    Development files for %{name}
Group:          Development/Libraries
Requires:     %{name} = %{version}-%{release}
Requires:     %{_includedir}/X11/extensions, %{_includedir}/GL

%description devel
This package provides the development files of the %{name} package,
such as OpenGL headers.


%ifarch x86_64
%package libs-32bit
Summary:    32 bit version of %{name}
Group:          User Interface/X Hardware Support
Requires:     %{name} = %{version}-%{release}

%description libs-32bit
This package provides the 32 bit version of %{name}. Please see description
of package %{name} for more information.
%endif #x86_64


%prep
%setup -q -c -T
sh %{SOURCE0} --extract fglrx
tar -cjf fglrx-kmod-data-%{version}.tar.bz2 fglrx/ATI_LICENSE.TXT fglrx/common/*/modules/fglrx/ fglrx/arch/*/*/modules/fglrx/
mkdir fglrxpkg

%ifarch %{ix86}
cp -r fglrx/common/* fglrx/x710/* fglrx/arch/x86/* fglrxpkg/
%endif

%ifarch x86_64
cp -r fglrx/common/* fglrx/x710_64a/* fglrx/arch/x86_64/* fglrxpkg/
%endif

%build

%install
rm -rf $RPM_BUILD_ROOT ./__doc

set +x
for file in $(cd fglrxpkg &> /dev/null; find . -type f | grep -v -e 'amdcccle.kdelnk$' -e '.*packages.*amdcccle.desktop$' -e 'fireglcontrol.kdelnk$' -e 'fireglcontrol.desktop$' -e 'lib/modules/fglrx$' -e 'ati.xpm$' -e 'fireglcontrolpanel$' -e '/usr/share/doc/fglrx/' -e 'fglrx_panel_sources.tgz$' -e 'fireglcontrol_kde3.desktop$' -e 'amdcccle_kde3.desktop$' -e 'fglrx_sample_source.tgz$' -e 'fglrx_sample_source.tgz$' -e '^./lib/modules/fglrx')
do
  if [[ ! "/${file##}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} ./__doc/${file##./usr/share/doc/fglrx/}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules/drivers}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/drivers/${file##./usr/X11R6/%{_lib}/modules/drivers}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules/dri}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_prefix}/%{_lib}/dri/${file##./usr/X11R6/%{_lib}/modules/dri}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/${file##./usr/X11R6/%{_lib}/modules}
  elif [[ ! "/${file##./usr/X11R6/lib/modules/dri}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_prefix}/lib/dri/${file##./usr/X11R6/lib/modules/dri}
  elif [[ ! "/${file##./usr/X11R6/include/X11/extensions}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_includedir}/X11/extensions/${file##./usr/X11R6/include/X11/extensions}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{atilibdir}/${file##./usr/X11R6/%{_lib}/}
  elif [[ ! "/${file##./usr/X11R6/lib/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{atilibdir32bit}/${file##./usr/X11R6/lib/}
  elif [[ ! "/${file##./usr/X11R6/bin/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_bindir}/${file##./usr/X11R6/bin/}
  elif [[ ! "/${file##./usr/bin/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_sbindir}/${file##./usr/bin/}
  elif [[ ! "/${file##./usr/sbin/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_sbindir}/${file##./usr/sbin/}
  elif [[ ! "/${file##./etc/ati/}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_sysconfdir}/ati/${file##./etc/ati/}
  elif [[ ! "/${file##./usr/include/}" = "/${file}" ]] || [[ ! "/${file##./etc/}" = "/${file}" ]] || [[ ! "/${file##./usr/share/man/}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/${file}
  elif [[ ! "/${file##./usr/share/icons/}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_datadir}/pixmaps/${file##./usr/share/icons/}
  elif [[ ! "/${file##./usr/share/ati/amdcccle/amdcccle_}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_datadir}/ati/amdccle/${file##./usr/share/ati/amdcccle/}
  elif [[ ! "/${file##./usr/share/gnome/apps/amdcccle.desktop}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_datadir}/applications/amdcccle.desktop
    echo 'Categories=Application;SystemSetup;X-Red-Hat-Base;' >> $RPM_BUILD_ROOT/%{_datadir}/applications/amdcccle.desktop
  else
    echo ${file} found -- don\'t know how to handle
    exit 1
  fi
done
set -x

# Change perms on static libs. Can't fathom how to do it nicely above.
find $RPM_BUILD_ROOT/%{atilibdir} -type f -name "*.a" -exec chmod 0644 '{}' \;

ln -s libGL.so.1.2 $RPM_BUILD_ROOT/%{atilibdir}/libGL.so.1
ln -s libfglrx_gamma.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_gamma.so.1
ln -s libfglrx_dm.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_dm.so.1
ln -s libfglrx_pp.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_pp.so.1
ln -s libfglrx_tvout.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_tvout.so.1

# workaround for modular X, part1
mkdir -p $RPM_BUILD_ROOT/usr/X11R6/%{_lib}/modules/dri/
ln -s %{_libdir}/dri/fglrx_dri.so $RPM_BUILD_ROOT/usr/X11R6/%{_lib}/modules/dri/fglrx_dri.so
#ln -s %{_libdir}/dri/atiogl_a_dri.so $RPM_BUILD_ROOT/usr/X11R6/%{_lib}/modules/dri/atiogl_a_dri.so
#ifarch x86_64
#mkdir -p $RPM_BUILD_ROOT/usr/X11R6/lib/modules/dri/
#ln -s %{_prefix}/lib/dri/fglrx_dri.so $RPM_BUILD_ROOT/usr/X11R6/lib/modules/dri/fglrx_dri.so
##ln -s %{_prefix}/lib/dri/atiogl_a_dri.so $RPM_BUILD_ROOT/usr/X11R6/lib/modules/dri/atiogl_a_dri.so
#endif

#install -D -p -m 0644 fglrx_panel_sources/ati.xpm $RPM_BUILD_ROOT/%{_datadir}/pixmaps/ati.xpm
#install -D -p -m 0755 fglrx_panel_sources/fireglcontrol $RPM_BUILD_ROOT/%{_bindir}/fireglcontrol
install -D -p -m 0644 %{SOURCE3} fglrx/usr/share/doc/fglrx/%(basename %{SOURCE3})
#install -D -p -m 0755 %{SOURCE10} $RPM_BUILD_ROOT%{_sbindir}/%(basename %{SOURCE10})
#install -D -p -m 0755 %{SOURCE11} $RPM_BUILD_ROOT%{_initrddir}/fglrx
#install -D -p -m 0755 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/fglrx.sh
install -D -p -m 0755 %{SOURCE13} $RPM_BUILD_ROOT%{_initrddir}/atieventsd
install -D -p -m 0755 fglrx/packages/Fedora/ati-powermode.sh $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/ati-powermode.sh
install -D -p -m 0644 fglrx/packages/Fedora/a-ac-aticonfig $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/a-ac-aticonfig.conf
install -D -p -m 0644 fglrx/packages/Fedora/a-lid-aticonfig $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/a-lid-aticonfig.conf

# rename some progs
mv $RPM_BUILD_ROOT%{_sbindir}/atigetsysteminfo.sh $RPM_BUILD_ROOT%{_sbindir}/atigetsysteminfo

# Avoid disturbing Fedora Core/Red Hat Mesa packages
%ifarch %{ix86}
if [ -d %{_sysconfdir}/ld.so.conf.d ]; then
  mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
  pushd $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
  cat <<EOF > fglrx-x86.conf
%{_libdir}/fglrx
EOF
  popd
fi
%endif

%ifarch x86_64
if [ -d %{_sysconfdir}/ld.so.conf.d ]; then
  mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
  pushd $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
  cat <<EOF > fglrx-x86_64.conf
%{_libdir}/fglrx
EOF
  popd
fi
%endif

# Create a proper desktop file in the right location for Fedora Core
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
pushd $RPM_BUILD_ROOT%{_datadir}/applications
cat <<EOF > ati-controlcenter.desktop
[Desktop Entry]
Encoding=UTF-8
Name=AMD Catalyst Control Center
GenericName=AMD Catalyst Control Center
Comment=The ATI Catalyst Control Center For Linux
Exec=amdcccle
Icon=ccc_large.xpm
Terminal=false
Type=Application
Categories=Qt;Application;System;
Version=%{version}
EOF
popd

# Set the correct path for gdm's Xauth file
sed -i 's|GDM_AUTH_FILE=/var/lib/gdm/$1.Xauth|GDM_AUTH_FILE=/var/gdm/$1.Xauth|' fglrxpkg/etc/ati/authatieventsd.sh

# Fix odd perms
find fglrxpkg -type f -perm 0555 -exec chmod 0755 '{}' \;
chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/ati/*.xbm.example
chmod 755 $RPM_BUILD_ROOT/%{_sysconfdir}/ati/*.sh

# make doc files rw by root
chmod -R a+rX,u+w fglrxpkg/usr/share/doc

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -e /etc/init.d/fglrx ]; then
  /sbin/chkconfig --del fglrx &>/dev/null ||:
fi

%post
/sbin/ldconfig ||:
if [ "${1}" -eq 1 ]; then
  ## Add init script
  #/sbin/chkconfig --add fglrx ||:
  ### Enable fglrx driver when installing
  ##%{_sbindir}/fglrx-config-display enable ||:
  if [ -e /etc/X11/xorg.conf ]; then
    /usr/bin/aticonfig --initial >/dev/null 2>&1 ||:
    ## Start init script
    #/etc/init.d/fglrx start &>/dev/null ||:
  fi
fi ||:
/usr/sbin/semanage fcontext -a -t textrel_shlib_t %{_libdir}/xorg/modules/glesx.so  >/dev/null 2>&1 || :
/sbin/fixfiles restore %{_libdir}/xorg/modules/glesx.so >/dev/null 2>&1 || :

%ifarch x86_64
%post libs-32bit
/sbin/ldconfig
%endif  #x86_64

%preun
if [ "${1}" -eq 0 ]; then
  ### Disable driver on final removal
  ##test -f %{_sbindir}/fglrx-config-display && %{_sbindir}/fglrx-config-display disable ||:
  ##/etc/init.d/fglrx stop &>/dev/null
  ##/sbin/chkconfig --del fglrx
  # if we are using fglrx, disable it
  if [ -e /etc/X11/xorg.conf ] && grep -q "Driver.*fglrx" /etc/X11/xorg.conf; then
    /usr/bin/system-config-display --set-driver=vesa >/dev/null 2>&1
  fi
fi ||:

%postun
/sbin/ldconfig
if [ "${1}" -eq 0 ]; then
	/usr/sbin/semanage fcontext -d -t textrel_shlib_t %{_libdir}/xorg/modules/glesx.so  >/dev/null 2>&1 || :
fi

# no more 32bit libs it seems
#ifarch x86_64
#postun libs-32bit
#sbin/ldconfig
#endif #x86_64

%files
%defattr(-,root,root,-)
%doc fglrxpkg/usr/share/doc/fglrx/*
%dir %{_sysconfdir}/ati
%dir %{atilibdir}
# workaround for modular X, part2a
%dir %{_prefix}/X11R6/
%dir %{_prefix}/X11R6/%{_lib}
%dir %{_prefix}/X11R6/%{_lib}/modules
%dir %{_prefix}/X11R6/%{_lib}/modules/dri
%{_prefix}/X11R6/%{_lib}/modules/dri/*so*
# end of workaround
##%{_sysconfdir}/profile.d/fglrx.sh
%config(noreplace) %{_sysconfdir}/ati/atiogl.xml
%config(noreplace) %{_sysconfdir}/ati/signature
%config(noreplace) %{_sysconfdir}/ati/control
%config %{_sysconfdir}/ati/logo.xbm.example
%config %{_sysconfdir}/ati/logo_mask.xbm.example
%config %{_sysconfdir}/ld.so.conf.d/fglrx*.conf
%config %{_sysconfdir}/acpi/events/*aticonfig.conf
%config %{_sysconfdir}/ati/amdpcsdb.default
%{_sysconfdir}/ati/authatieventsd.sh
%{_sysconfdir}/acpi/actions/ati-powermode.sh
%{_initrddir}/atieventsd
#%{_initrddir}/fglrx
%{_sbindir}/atigetsysteminfo
%{_sbindir}/atieventsd
%{_sbindir}/amdnotifyui
%{_bindir}/aticonfig
%{_bindir}/fgl_glxgears
%{_bindir}/fglrxinfo
%{_bindir}/fglrx_xgamma
%{atilibdir}/*.so.*
%{_libdir}/dri/fglrx_dri.so
%{_libdir}/xorg/modules/drivers/fglrx_drv.so
%{_libdir}/xorg/modules/linux/libfglrxdrm.so
%{_libdir}/xorg/modules/glesx.so
%{_mandir}/man[1-9]/atieventsd.*
%{_bindir}/amdcccle
%{_datadir}/applications/ati-controlcenter.desktop
%{_datadir}/applications/amdcccle.desktop
%{_datadir}/pixmaps/ccc_large.xpm
%{_datadir}/pixmaps/ccc_small.xpm
%dir %{_datadir}/ati
%dir %{_datadir}/ati/amdccle
%{_datadir}/ati/amdccle/*qm

%files devel
%defattr(-,root,root,-)
%doc fglrxpkg/usr/src/ati/fglrx_sample_source.tgz
%{atilibdir}/*.a
%{_includedir}/GL/glxATI.h
%{_includedir}/GL/glATI.h
%{_includedir}/X11/extensions/fglrx_gamma.h
%{_libdir}/xorg/modules/esut.a

#ifarch x86_64
#files libs-32bit
#defattr(-,root,root,-)
#dir %{atilibdir32bit}
#{atilibdir32bit}/*.so.*
#{_prefix}/lib/dri/
## workaround for modular X, part2b
#dir %{_prefix}/X11R6/
#dir %{_prefix}/X11R6/lib
#dir %{_prefix}/X11R6/lib/modules
#dir %{_prefix}/X11R6/lib/modules/dri
#{_prefix}/X11R6/lib/modules/dri/*so*
## end of workaround
#endif

%changelog
* Sun Nov 03 2007 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 8.42.3

* Fri Oct 05 2007 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to new version (for new chipset support), remove libGL.so
  from provides and add the new control panel

* Sun Mar 25 2007 Stewart Adam < s.adam AT diffingo DOT com > - 8.34.8-10
- Sync devel with FC-6
- Fix up initscript a little
- Update README

* Fri Mar 9 2007 Stewart Adam < s.adam AT diffingo DOT com > - 8.34.8-9
- Fix up scriptlets a little so that 'Driver already enabled|disabled'
  doesn't always appear on install or remove
- Update *-config-display files for majorVendor and not plain vendor

* Fri Mar 2 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-8
- New config-display
- New initscript
- Bump to -8

* Mon Feb 26 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-6
- Remove broken symlink atiogl_a_dri.so
- It's AMD not ATI's driver now!

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 8.34.8-5
- Bump for new tag

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 8.34.8-4
- Standardize all summaries and descriptions with other nvidia and fglrx
  packages
- Standardize initscript and *config-display with other nvidia and fglrx
  packages
- Start merge with livna-config-display
- No more ghost!

* Thu Feb 22 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-3
- Add the profile.d script back, it was used for something else then
  workaround for the RH bug

* Wed Feb 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-2
- Seems I can't overwrite a tag.. Bump I go!
- Fix changelog date for 8.34.8-1

* Wed Feb 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-1
- Update to 8.34.8
- Move paths and names to plain fglrx, not ati-fglrx, the driver's name's
  long changed!
- Don't own /usr/X11R6... It's part of the standard hierarchy!
- Fix funny permissions on /etc/ files
- Mark config files as %%config

* Sun Feb 18 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-4
- Fix %%post, make it %%postun for libs-32bit

* Sat Feb 17 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-3
- Change descriptions to more informative, easy-to-understand ones
- Requires pyxf86config

* Fri Jan 12 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-2
- ldconfig in %%postun for 32-bit libs, too!

* Fri Jan 12 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-1
- Update to 8.33.6
- ldconfig in %%post for 32-bit libs

* Tue Nov 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-3
- re-add workaround -- seems some machines still search in /usr/X11R6 for dri
  files

* Mon Nov 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-2
- add modified version of a patch from Stewart Adam to put the DRI .so files
  to the right spot and remove the old workaround

* Fri Nov 17 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-1
- Update to 8.31.5, patch from Edgan in #livna

* Sat Oct 14 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.29.6-1
- Update to 8.29.6 (needed for 2.6.18 suppport/FC6)

* Fri Aug 18 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.28.8-1
- Update to 8.28.4
- refactored %%prep now that ATi's installer has merged arches

* Fri Aug 18 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-4
- updated/improved atieventsd init script
- removed remove excess tabs/whitespace from fglrx-config-display
- make tar quiet when creating the kmod tarball

* Sat Aug 05 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-3
- don't try to use '*.sh' in the for loop
- tone down the rant in ati-fglrx.profile.d

* Tue Aug 01 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-2
- fix perms on static libs
- added powerplay acpi bits
- made authatieventsd actually do something. Thorsten's for loop hurts little children
- rearranged files sections somewhat
- move all *.a files to devel package
- make the package actually build (file libaticonfig.a dropped upstream)

* Sun Jul 30 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-1
- Update to 8.27.10
- minor changes to spacing, removal of random tabs, re-arrangements

* Tue Jun 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.26.18-1
- Update to 8.26.18

* Fri Jun 02 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.25.18-2
- Fix 32bit libs

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.25.18-1
- Update to 8.25.18

* Fri May 19 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.24.8-3
- Change security context in %%post until #191054 is fixed
- conflict with nvidia packages

* Sun May 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.24.8-2
- Require fglrx-kmod instead of kmod-fglrx, obsolete incompatible kmods (#970).

* Sat Apr 15 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.24.8-1
- Update to 8.24.8

* Sun Apr 02 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-6
- Fix a "lib != %%{_lib}"

* Wed Mar 29 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.23.7-5
- fix perms on the headers
- tweak nvidia-settings' desktop file slightly

* Sun Mar 26 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-4
- fix another stupid oddity of fglrx with modular X

* Sun Mar 26 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-3
- fix deps in devel
- separate package for 32bit libs
- some cleanups from straw
- always activate driver
- try to unload drm and radeon in profile.d script

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-2
- update fglrx-config-display
- packge /usr/lib/xorg/modules/dri/fglrx_dri.so for now

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-1
- drop 0.lvn
- update to 8.23.7
- ExclusiveArch i386 and not %%{ix86} -- we don't want to build for athlon&co
- package some links that ldconfig normally would create

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- split into packages for userland and kmod
- rename to xorg-x11-drv-fglrx; yum/rpm should use mesa-libGL{,-devel} then in
  the future when seaching for libGL.so{,.1}
- remove kernel-module part
- remove old cruft

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
- Fix moduleline.split in fglrx-config-display (#582)
- Unload drm in fglrx-config-display, too
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
- fix x86-64 in spec-file and in fglrx-config-display
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
- Update one para in README and fglrx-config-display output

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
- intergrate Readme, init-script and fglrx-config-display (stolen from
  nvidia package)

* Sat Jul 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.1
- Initial RPM release.
