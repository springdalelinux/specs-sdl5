Name:           gkrellm
Version:        2.3.0
Release:        4%{?dist}.1
Summary:        Multiple stacked system monitors in one process
Group:          Applications/System
License:        GPLv3+
URL:            http://www.gkrellm.net/
Source0:        http://members.dslextreme.com/users/billw/gkrellm/%{name}-%{version}.tar.bz2
Source1:        gkrellmd.init
Source2:        gkrellm.desktop
Source3:        gkrellm.png
Patch0:         gkrellm-2.3.0-gnutls.patch
Patch1:         gkrellm-2.1.28-config.patch
Patch2:         gkrellm-2.2.4-sansfont.patch
Patch3:         gkrellm-2.2.7-width.patch
Patch4:         gkrellm-2.2.9-libdir.patch
Patch5:         gkrellm-2.3.0-sensorscheck.patch
BuildRequires:  gtk2-devel gnutls-devel libSM-devel desktop-file-utils gettext
%ifarch %{ix86} x86_64 alpha
BuildRequires:  lm_sensors-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GKrellM charts CPU, load, Disk, and all active net interfaces
automatically.  An on/off button and online timer for the PPP
interface is provided, as well as monitors for memory and swap usage,
file system, internet connections, APM laptop battery, mbox style
mailboxes, and temperature sensors on supported systems.  Also
included is an uptime monitor, a hostname label, and a clock/calendar.
Additional features are:

  * Autoscaling grid lines with configurable grid line resolution.
  * LED indicators for the net interfaces.
  * A gui popup for configuration of chart sizes and resolutions.


%package daemon
Summary:        The GNU Krell Monitors Server
Group:          System Environment/Daemons
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description daemon
gkrellmd listens for connections from gkrellm clients. When a gkrellm
client connects to a gkrellmd server all builtin monitors collect their
data from the server.


%package        devel
Summary:        Development files for the GNU Krell Monitors
Group:          Development/System
Requires:       gtk2-devel

%description devel
Development files for the GNU Krell Monitors.


%prep
%setup -q
%patch0 -p1 -z .gnutls
%patch1 -p1 -z .config
%patch2 -p1 -z .sansfont
%patch3 -p1 -z .width
%patch4 -p1 -z .libdir2
%patch5 -p1 -z .sensorscheck

for i in gkrellmd.1 gkrellm.1 README Changelog Changelog-plugins.html; do
   sed -i -e "s@/usr/lib/gkrellm2/plugins@%{_libdir}/gkrellm2/plugins@" $i
   sed -i -e "s@/usr/lib/gkrellm/plugins@%{_libdir}/gkrellm2/plugins@" $i
done
for i in gkrellmd.1 gkrellm.1 README Changelog Changelog-plugins.html; do
   sed -i -e "s@/usr/local/lib/gkrellm2/plugins@/usr/local/%{_lib}/gkrellm2/plugins@" $i
   sed -i -e "s@/usr/local/lib/gkrellm/plugins@/usr/local/%{_lib}/gkrellm2/plugins@" $i
done


%build
make %{?_smp_mflags} INSTALLROOT=%{_prefix} PKGCONFIGDIR=%{_libdir}/pkgconfig \
  INCLUDEDIR=%{_includedir} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gkrellm2/themes
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gkrellm2/plugins

make install \
    LOCALEDIR=$RPM_BUILD_ROOT%{_datadir}/locale \
    INSTALLDIR=$RPM_BUILD_ROOT%{_bindir} \
    SINSTALLDIR=$RPM_BUILD_ROOT%{_sbindir} \
    MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    PKGCONFIGDIR=$RPM_BUILD_ROOT%{_libdir}/pkgconfig \
    INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir} \
    STRIP=""
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/gkrellmd
install -m 644 server/gkrellmd.conf $RPM_BUILD_ROOT%{_sysconfdir}/gkrellmd.conf
%find_lang %name

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor gnome             \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE2}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -p -m 644 %{SOURCE3} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%pre daemon
getent group gkrellmd >/dev/null || groupadd -r gkrellmd
getent passwd gkrellmd >/dev/null || \
useradd -r -g gkrellmd -M -d / -s /sbin/nologin -c "GNU Krell daemon" gkrellmd
:

%post daemon
/sbin/chkconfig --add gkrellmd || :

%preun daemon
if [ "$1" = "0" ]; then
    /sbin/service gkrellmd stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del gkrellmd || :
fi

%postun daemon
if [ "$1" -ge "1" ]; then
    /sbin/service gkrellmd condrestart > /dev/null 2>&1 || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYRIGHT Changelog README Themes.html
%{_bindir}/%{name}
%{_libdir}/gkrellm2
%{_datadir}/gkrellm2
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/gnome-%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

%files devel
%defattr(-,root,root,-)
%{_includedir}/gkrellm2
%{_libdir}/pkgconfig/%{name}.pc

%files daemon
%defattr(-,root,root,-)
%{_initrddir}/gkrellmd
%{_sbindir}/gkrellmd
%{_mandir}/man1/gkrellmd.*
%config(noreplace) %{_sysconfdir}/gkrellmd.conf


%changelog
* Wed Sep  5 2007 Ville Skyttä <ville.skytta at iki.fi> - 2.3.0-4.1
- Adapt to lm_sensors availability/setup in EL.

* Wed Sep  5 2007 Ville Skyttä <ville.skytta at iki.fi> - 2.3.0-4
- Rewrite gkrellmd init script: better LSB compliance, hddtemp
  interoperability, avoidance of X error messages, general cleanup.

* Tue Sep  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 2.3.0-3
- Fix gnutls detection/build and use it instead of openssl.
- Sync user and group creation with current Fedora guidelines.

* Tue Aug  7 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.0-2
- Update License tag for new Licensing Guidelines compliance

* Sun Jul 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.3.0-1
- New upstream release 2.3.0

* Fri Jul 20 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.10-3
- Rebuild, including libsensors support on ppc and ppc64 as lm_sensors is
  available there now.

* Wed Nov  8 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.10-2
- Add special case for via 686 volt sensors <sigh> (bug 213304)

* Tue Oct 31 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.10-1
- New upstream release 2.2.10
- Drop integrated lmsensors and sysfs sensors patches

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.2.9-10
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.9-9
- Fixup .desktop so that gkrellm actually gets shown in the menu (bz 206775)

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.9-8
- FE6 Rebuild

* Sun Jul 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.9-7
- Add -r to groupadd
- Add || : to the gkrellmd service related scripts (deviation from the wiki).
- Don't make -devel package require the main one as it doesn't need it
- Install .desktop file with --vendor gnome to not break existing kde panel
  buttons, etc.
- Drop "StartupNotify=false" from .desktop to not interfere with kde's 
  internal startup notification
- use gkrellmd as group in default gkrellmd.conf

* Sat Jul 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.9-6
- Various specfile improvements by Ville Skyttä (ville.skytta@iki.fi)
- Make the daemon package scripts match the ScriptletSnippets wiki page
- Add LSB aliases (try-restart, force-reload) to the -daemon initscript
- Add %%{?dist} to the release for consistency with other packages I maintain

* Sat Jul 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.9-5
- Remove Obsoletes/Provides gkrellm-server
- Don't remove user on uninstall
- Only build with lm_sensors support on x86 / x86_64 since lm_sensors is not
  available on other archs.
- Use %%{_sysconfdir} instead of /etc in %%install

* Fri Jul  7 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2.9-4
- Moving to Fedora Extras, initial FE submission
- Various specfile improvements / cleanups
- Remove gkrellm-wireless (will be submitted as a seperate package)
- Use libsensors instead of DIY code to read lm_sensors sensors
- Don't strip the binaries when installing so we get a usable -debuginfo rpm

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 2.2.9-3
- fix libdir patch

* Mon May 15 2006 Karsten Hopp <karsten@redhat.de> 2.2.9-2
- fix header file conflict between 32bit and 64bit archs

* Mon Apr 03 2006 Karsten Hopp <karsten@redhat.de> 2.2.9-1
- update to 2.2.9
- remove explicit UID/GUIs from useradd/groupadd (#186974)  

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 2.2.7-7
- BuildRequires: libSM-devel

* Wed Feb 15 2006 Karsten Hopp <karsten@redhat.de> 2.2.7-6
- fix chkconfig requires

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.7-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.7-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 2.2.7-5
- Fix references to obsolete /usr/X11R6 path

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 2.2.7-4
- rebuilt with new openssl

* Thu Sep 06 2005 Karsten Hopp <karsten@redhat.de> 2.2.7-3
- fix path to gkrellm2 plugins on 64bit archs (#164066)

* Thu Aug 18 2005 Florian La Roche <laroche@redhat.com>
- the the kernel dep form a Requires: into a Conflicts:

* Thu Jun 09 2005 Karsten Hopp <karsten@redhat.de> 2.2.7-1
- update to 2.2.7
- add Requires: /sbin/chkconfig for -daemon subpackage
- allow gkrellm width up to 1600 pixel
- change spec file to valid UTF-8 (#159578)

* Tue May 17 2005 Karsten Hopp <karsten@redhat.de> 2.2.4-5
- use Sans fonts (Ville Skytta, #157899)

* Fri Apr 01 2005 Karsten Hopp <karsten@redhat.de> 2.2.4-4
- Include gkrellm2/plugins directories (Michael Schwendt)
  #153073

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 2.2.4-3
- build with gcc-4

* Thu Feb 03 2005 Karsten Hopp <karsten@redhat.de> 2.2.4-2 
- BuildRequires openssl-devel (#137548)

* Tue Nov 16 2004 Karsten Hopp <karsten@redhat.de> 2.2.4-1 
- update

* Mon Sep 06 2004 Karsten Hopp <karsten@redhat.de> 2.2.2-2
- change group of wireless subpackage (#131699)
- add icon

* Tue Aug 03 2004 Karsten Hopp <karsten@redhat.de> 2.2.2-1
- update to 2.2.2 to fix pixbuf memory leak

* Wed Jun 23 2004 Karsten Hopp <karsten@redhat.de> 2.2.1-1
- update to latest stable release

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 31 2004 Warren Togami <wtogami@redhat.com> 2.2.0-1
- upgrade to 2.2.0
- #123846 bogus dep
- Cleanup deps, build deps, and docs

* Mon Mar 15 2004 Karsten Hopp <karsten@redhat.de> 2.1.28-3 
- remove Provides: gkrellm-devel from main package (#117105)

* Thu Mar 11 2004 Karsten Hopp <karsten@redhat.de> 2.1.28-2 
- don't run gkrellmd as nobody, use a unique UID (#116314)
- fix chkconfig at package removal

* Wed Mar 10 2004 Karsten Hopp <karsten@redhat.de> 2.1.28-1 
- update
- add runlevel links with chkconfig (#107481)
- use slightly patched config file from the tarball for gkrellmd
- add wireless plugin

* Wed Mar 03 2004 Karsten Hopp <karsten@redhat.de> 2.1.26-2
- fix -devel provision (#117105)
- remove stringfreeze hack

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 25 2004 Karsten Hopp <karsten@redhat.de> 2.1.26-1
- update to 2.1.26, which fixes sensor data being 10x to high (#115850)
- requires kernel >= 2.6.2

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- mv /etc/init.d -> /etc/rc.d/init.d

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 09 2004 Karsten Hopp <karsten@redhat.de> 2.1.24-1
- update to 2.1.24

* Mon Oct 13 2003 Karsten Hopp <karsten@redhat.de> 2.1.21-1
- update:
- fix temperature reads from /proc/acpi
- Use username instead of userid in session management userid property.
  Fixes no session restarts in KDE 3.1.4.
- de.po update

* Thu Oct 09 2003 Karsten Hopp <karsten@redhat.de> 2.1.20-3
- make it compatible with 3d party packages

* Thu Oct 09 2003 Karsten Hopp <karsten@redhat.de> 2.1.20-2
- added patches from Ville Skyttä <ville.skytta at iki.fi>:
  - Add icon for desktop entry
  - Install daemon in %%{_sbindir}
  - Include themes and plugins dirs in main package
  - Make -daemon obsolete -server
  - devel subpackage (disabled because of string freeze)


* Wed Oct 08 2003 Karsten Hopp <karsten@redhat.de> 2.1.20-1
- update to make it work with kernel 2.6

* Wed Oct 01 2003 Karsten Hopp <karsten@redhat.de> 2.1.19-1
- Update to 2.1.19, includes fix for #106073

* Tue Jul 08 2003 Karsten Hopp <karsten@redhat.de> 2.1.14-3
- run as user nobody
- fix file ownership

* Mon Jul 07 2003 Karsten Hopp <karsten@redhat.de> 2.1.14-2
- add init script and config file for gkrellmd
- daemon subpackage
- fix pkgconfig file

* Thu Jun 26 2003 Karsten Hopp <karsten@redhat.de> 2.1.14-1
- update to fix buffer overflow in gkrellmd_client_read

* Wed Jun 18 2003 Karsten Hopp <karsten@redhat.de> 2.1.13-1
- update

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 05 2003 Karsten Hopp <karsten@redhat.de> 2.1.9-2
- rebuild

* Thu Apr 10 2003 Karsten Hopp <karsten@redhat.de> 2.1.9-1
- update to 2.1.9
- daily/weekly/monthly transfer stats

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 14 2003 Karsten Hopp <karsten@redhat.de> 2.1.5-2
- rename menu entry (#81876)

* Sun Jan 12 2003 Karsten Hopp <karsten@redhat.de> 2.1.5-1
- update (#81620)

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 2.1.3-2
- rebuild

* Wed Dec 11 2002 Karsten Hopp <karsten@redhat.de>
- 2.1.3-1
- Battery monitor can display multiple batteries
- Net timer lost the minutes display with large connect times
- use disk stats from /proc/partitions if available

* Tue Dec 03 2002 Karsten Hopp <karsten@redhat.de> 2.1.2-1
- updated translations
- .desktop file (#78562)
- minor bugfixes

* Mon Nov 11 2002 Karsten Hopp <karsten@redhat.de>
- update to 2.1 (glib2, gtk2)

* Wed Jul 17 2002 Karsten Hopp <karsten@redhat.de>
- update
- own /usr/include/gkrellm directory

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Karsten Hopp <karsten@redhat.de>
- Update to 1.2.11

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Karsten Hopp <karsten@redhat.de>
- Update to 1.2.9

* Wed Jan 23 2002 Karsten Hopp <karsten@redhat.de>
- Update to 1.2.6

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Dec 13 2001 Karsten Hopp <karsten@redhat.de>
- update to 1.2.5-1
- nls patch not required anymore

* Mon Nov 26 2001 Karsten Hopp <karsten@redhat.de>
- enable nls

* Mon Nov 26 2001 Karsten Hopp <karsten@redhat.de>
- update to 1.2.4

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Add %%defattr
- langify
- Don't define name, ver and rel at the top of the spec file

* Wed Jun 27 2001 Karsten Hopp <karsten@redhat.de>
- fix _mandir
- fix BuildRequires

* Wed Jun 27 2001 SATO Satoru <ssato@redhat.com>
- clean up (use system-defined macros)
- enable NLS

* Wed Mar 14 2001 Rob Lineweaver <rbline@wm.edu>
- fixed new manpage inclusion for newer RPM versions
- source is 1.0.7
- compiled for PPC and i386

* Fri Jan 19 2001 Kevin Ford <klford@uitsg.com>
- general cleanup of spec file

* Thu Jan 18 2001 Kevin Ford <klford@uitsg.com>
- Updated spec file to work with both v3 & v4 rpm
- moved changelog to bottom of spec file
- added defines for common items

* Thu Apr 6 2000 Bill Wilson
- added INCLUDEDIR to the make install

* Fri Oct 29 1999 Gary Thomas <gdt@linuxppc.org>
- .spec file still broken

* Thu Oct 7 1999 David Mihm <davemann@ionet.net>
- fixed spec.
