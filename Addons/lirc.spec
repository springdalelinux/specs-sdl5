# TODO:
# - caraca driver (req: caraca, http://caraca.sf.net/)
# - irman driver (req: libirman, http://lirc.sf.net/software/snapshots/)
# - iguanaIR driver (req: http://iguanaworks.net/ir/usb/installation.shtml)
#   -> would cause license change to "GPLv2"
# - move to -devel (?): irw, *mode2, others?
#   note: xmode2 inflicts a dependency on X, and smode2 on svgalib
#   - does someone actually need xmode2/smode2 for something?
# - split into -libs and -utils (daemons in main package)?
# - don't run as root and/or create dedicated group, reduce fifo permissions?
# - Fixup /etc/lirc(m)d.conf %%ghost'ification, existence after erase etc.

%bcond_without  alsa
%bcond_with     portaudio
%bcond_with     svgalib
%bcond_without  x

Name:           lirc
Version:        0.8.2
Release:        2%{?dist}
Summary:        The Linux Infrared Remote Control package

Group:          System Environment/Daemons
License:        GPLv2+
URL:            http://www.lirc.org/
Source0:        http://downloads.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
Source1:        %{name}.init
Source2:        %{name}.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{__perl}
BuildRequires:  libusb-devel
%if %{with alsa}
BuildRequires:  alsa-lib-devel
%endif
%if %{with portaudio}
BuildRequires:  portaudio-devel >= 18
%endif
%if %{with svgalib}
BuildRequires:  svgalib-devel
%endif
%if %{with x}
BuildRequires:  libXt-devel
%endif
Requires(post): /sbin/chkconfig
Requires(post): /sbin/ldconfig
Requires(preun): /sbin/chkconfig
Requires(postun): /sbin/ldconfig

%description
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.

%package        devel
Summary:        Development files for LIRC
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package includes files for
developing applications that use LIRC.

%package        doc
Summary:        LIRC documentation
Group:          Documentation

%description    doc
LIRC is a package that allows you to decode and send infra-red and
other signals of many (but not all) commonly used remote controls.
Included applications include daemons which decode the received
signals as well as user space applications which allow controlling a
computer with a remote control.  This package contains LIRC
documentation and a collection of remote control configuration files.


%prep
%setup -q
chmod 644 contrib/*
sed -i -e 's|/usr/local/etc/|/etc/|' contrib/irman2lirc
sed -i -e 's/\r//' remotes/hercules/lircd.conf.smarttv_stereo \
    remotes/adstech/lircd.conf.usbx-707
sed -i -e 's|/sbin/init.d/lircd|%{_initrddir}/lirc|' contrib/lircs
for f in remotes/chronos/lircd.conf.chronos \
    remotes/creative/lircd.conf.livedrive remotes/atiusb/lircd.conf.atiusb \
    NEWS ChangeLog AUTHORS contrib/lircrc ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done
sed -i -e 's|"/lib /usr/lib |"/%{_lib} %{_libdir} |' configure # lib64 rpath
# *cough* I wish there was a good way to disable alsa/portaudio/svgalib...
%if ! %{with alsa}
sed -i -e 's/asoundlib.h/ALSA_DISABLED/g' configure*
%endif
%if ! %{with portaudio}
sed -i -e 's/portaudio.h/PORTAUDIO_DISABLED/g' configure*
%endif
%if ! %{with svgalib}
sed -i -e 's/vga.h/SVGALIB_DISABLED/g' configure*
%endif
touch -r acconfig.h aclocal.m4 configure.in # avoid autofoo re-run


%build
%configure \
  --disable-static \
  --disable-dependency-tracking \
  --enable-sandboxed \
%if ! %{with x}
  --without-x \
%endif
  --with-syslog=LOG_DAEMON \
  --with-driver=userspace
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __docs

make install DESTDIR=$RPM_BUILD_ROOT
install -pm 755 contrib/irman2lirc $RPM_BUILD_ROOT%{_bindir}
%if ! %{with svgalib}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/smode2.1*
%endif
%if ! %{with x}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/irxevent.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xmode2.1*
%endif

install -Dpm 644 doc/lirc.hwdb $RPM_BUILD_ROOT%{_datadir}/lirc/lirc.hwdb

install -Dpm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/lirc
%{__perl} -pi -e \
  's|/etc/|%{_sysconfdir}/|g ;
   s|/var/|%{_localstatedir}/|g ;
   s|/usr/sbin/|%{_sbindir}/|g' \
  $RPM_BUILD_ROOT%{_initrddir}/lirc
install -Dpm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lirc

mkdir __docs
cp -pR doc contrib __docs
cd __docs
rm -rf doc/Makefile* doc/.libs doc/man* doc/lirc.hwdb
rm -rf contrib/irman2lirc contrib/lirc.* contrib/sendxevent.c
cd ..

touch $RPM_BUILD_ROOT%{_sysconfdir}/lirc{d,md}.conf

install -dm 755 $RPM_BUILD_ROOT/dev
touch $RPM_BUILD_ROOT/dev/lirc{d,m}

rm $RPM_BUILD_ROOT%{_libdir}/liblirc_client.la


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
/sbin/chkconfig --add lirc

%preun
if [ $1 -eq 0 ] ; then
  %{_initrddir}/lirc stop >/dev/null || :
  /sbin/chkconfig --del lirc || :
fi

%postun
/sbin/ldconfig
if [ $1 -gt 0 ] ; then
  %{_initrddir}/lirc try-restart >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc ANNOUNCE AUTHORS ChangeLog COPYING NEWS README TODO
%ghost %config(noreplace) %{_sysconfdir}/lirc*d.conf
%config(noreplace) %{_sysconfdir}/sysconfig/lirc
%{_initrddir}/lirc
%{_bindir}/*ir*
%{_bindir}/*mode2
%{_sbindir}/lirc*d
%{_libdir}/liblirc_client.so.*
%{_datadir}/lirc/
%{_mandir}/man1/*ir*.1*
%{_mandir}/man1/*mode2*.1*
%{_mandir}/man8/lirc*d.8*
%ghost /dev/lirc*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lirc/
%{_libdir}/liblirc_client.so

%files doc
%defattr(-,root,root,-)
%doc __docs/* remotes/


%changelog
* Wed Aug 15 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.2-2
- License: GPLv2+

* Sun Jun 10 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.2-1
- 0.8.2.

* Wed Jun  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.2-0.1.pre3
- 0.8.2pre3.
- Fix up linefeeds and char encodings of more docs.

* Fri May 18 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.2-0.1.pre2
- 0.8.2pre2.

* Sun Jan  7 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-1
- 0.8.1.

* Sat Dec 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.2.pre5
- 0.8.1pre5.

* Tue Dec 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.2.pre4
- 0.8.1pre4.

* Thu Nov 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.2.pre3
- 0.8.1pre3.

* Sun Oct 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.2.pre2
- 0.8.1pre2, optflags patch no longer needed.

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.2.pre1
- Rebuild.

* Sat Jul  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.1-0.1.pre1
- 0.8.1pre1.
- Add rpmbuild options for enabling/disabling ALSA, portaudio and/or X
  support, ALSA and X enabled by default, portaudio not.
- Split most of the documentation to -doc subpackage.
- Install irman2lirc as non-doc.

* Tue Feb 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-3
- Avoid standard rpaths on lib64 archs.

* Sat Jan 21 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-2
- 0.8.0.

* Sat Jan 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-0.2.pre4
- 0.8.0pre4.

* Sun Jan  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-0.2.pre3
- 0.8.0pre3.

* Tue Dec 27 2005 Ville Skyttä <ville.skytta at iki.fi>
- Split kernel modules into separate package.
- Disable debugging features.

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-0.2.pre2
- 0.8.0pre2, kernel >= 2.6.15 USB patch applied upstream.
- lirc_clientd renamed to lircrcd.

* Tue Nov 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-0.2.pre1
- Pull security fix for the new lirc_clientd from upstream CVS, and
  while at it, some other useful post-0.8.0pre1 changes.
- Kernel >= 2.6.15 patchwork based on initial patch from Andy Burns (#172404).
- Disable lirc_cmdir kernel module (unknown symbols).
- Adapt to modular X.Org packaging.

* Wed Nov  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.8.0-0.1.pre1
- 0.8.0pre1, usage message patch applied upstream.

* Sun Oct 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-0.1.pre1
- 0.7.3pre1, "no device" crash fix applied upstream.
- Fix lircd and lircmd usage messages.

* Wed Aug 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.2-3
- Make the init script startup earlier and shutdown later by default.

* Sun Aug 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.2-2
- 0.7.2, patch to fix crash at startup when no device is specified.
- Enable audio input driver support (portaudio).
- Improve package description.
- Don't ship static libraries.
- Drop pre Fedora Extras backwards compatibility hacks.
- Make svgalib support (smode2) build conditional, disabled by default.
- Simplify module package build (still work in progress, disabled by default).
- Other minor specfile cleanups and maintainability improvements.

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.1-3
- Adjust kernel module build for FC4 and add hauppauge, igorplugusb, imon,
  sasem, and streamzap to the list of modules to build.  This stuff is still
  disabled by default, rebuild with "--with modules --target $arch" to enable.

* Sun Apr 17 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.1-2
- 0.7.1.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Dec  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0.7.0-1
- Update to 0.7.0; major rework of the package:
- Change default driver to "any".
- Add -devel subpackage.
- Improve init script, add %%{_sysconfdir}/sysconfig/lirc for options.
- Rename init script to "lirc" to follow upstream; the script is not only
  for lircd, but lircmd as well.
- Log to syslog instead of separate log file.
- %%ghost'ify /dev/lirc*.
- Build kernel modules when rebuilt with "--with kmod".  This stuff was mostly
  borrowed from Axel Thimm's packages, and is not really ready for FC3+ yet.
- Enable debugging features.
- Specfile cleanups.

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.6.6-3
- Added missing /sbin/ldconfig calls.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Rebuild for Fedora Core 2... this spec file still _really_ needs reworking!

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Rebuild for Fedora Core 1... this spec file _really_ needs reworking!

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9... this spec file needs some reworking!

* Mon Oct  7 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.6.6 final.

* Mon Sep 16 2002 Matthias Saou <http://freshrpms.net/>
- Updated to latest pre-version.
- Kernel modules still need to be compiled separately and with a custom
  kernel :-(

* Thu May  2 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.6.5.
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Thu Oct  4 2001 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.

