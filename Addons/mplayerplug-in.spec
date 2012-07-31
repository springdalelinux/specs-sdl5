# $Id: mplayerplug-in.spec 5214 2007-02-26 15:22:36Z dag $
# Authority: dries
# Upstream: Kevin DeKorte <kdekorte$users,sourceforge,net>
# Upstream: <mplayerplug-in-devel$lists,sourceforge,net>

#%define mversion %(rpm -q mozilla-devel --qf "%%{epoch}:%%{version}")

%{?dist: %{expand: %%define %dist 1}}

%define mozilla seamonkey
%{!?dist:%define mozilla firefox}
%{?el5:%define mozilla firefox}
%{?fc6:%define mozilla firefox}

%{?fc4:%define _without_modxorg 1}
%{?el4:%define _without_modxorg 1}
%{?fc3:%define _without_modxorg 1}
%{?fc2:%define _without_modxorg 1}
%{?fc1:%define _without_modxorg 1}
%{?el3:%define _without_modxorg 1}
%{?rh9:%define _without_modxorg 1}
%{?rh9:%define mozilla mozilla}
%{?rh7:%define _without_modxorg 1}
%{?rh7:%define mozilla mozilla}
%{?el2:%define _without_modxorg 1}
%if "%{rhel}" == "4"
%define _without_modxorg 1
%endif

Summary: Browser plugin for MPlayer
Name: mplayerplug-in
Version: 3.50
Release: 0.1%{?dist}
License: GPL
Group: Applications/Multimedia
URL: http://mplayerplug-in.sourceforge.net/

Packager: Dries Verachtert <dries@ulyssis.org>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

#Source: http://dl.sf.net/mplayerplug-in/mplayerplug-in-%{version}.tar.gz
Source: http://dl.sf.net/mplayerplug-in/mplayerplug-in-daily.tar.gz
Patch1: mplayerplug-in.rpmtweaks.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: %{mozilla}-devel, gtk2-devel >= 2.2.1
BuildRequires: gcc-c++, gettext
%{!?_without_modxorg:BuildRequires: libXt-devel, libXpm-devel}
%{?_without_modxorg:BuildRequires: XFree86-devel}

Obsoletes: mozilla-mplayer < 3.25-2
#Requires: mplayer, mozilla = %{mversion}
#Requires: %{_libdir}/mozilla/plugins/
Requires: mplayer

%description
mplayerplug-in is a browser plugin that uses mplayer to play videos
in your browser.

%prep
%setup -n %{name}
%patch1 -p1 -b .rpmtweaks

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc ChangeLog INSTALL README TODO
%config(noreplace) %{_sysconfdir}/mplayerplug-in.conf
%config(noreplace) %{_sysconfdir}/mplayerplug-in.types
%{_libdir}/mozilla/plugins/mplayerplug-in.so
%{_libdir}/mozilla/plugins/mplayerplug-in.xpt
%{_libdir}/mozilla/plugins/mplayerplug-in-dvx.so
%{_libdir}/mozilla/plugins/mplayerplug-in-dvx.xpt
%{_libdir}/mozilla/plugins/mplayerplug-in-qt.so
%{_libdir}/mozilla/plugins/mplayerplug-in-qt.xpt
%exclude %{_libdir}/mozilla/plugins/mplayerplug-in-rm.so
%exclude %{_libdir}/mozilla/plugins/mplayerplug-in-rm.xpt
%{_libdir}/mozilla/plugins/mplayerplug-in-wmp.so
%{_libdir}/mozilla/plugins/mplayerplug-in-wmp.xpt

%changelog
* Tue Jan 22 2008 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to daily snapshot, sort of 3.50+...

* Mon Apr 2 2007 Josko Plazonic <plazonic@math.princeton.edu>
- make sure alsa is default and drop realplayer plugins, we have
  the realplayer

* Wed Mar 21 2007 Dag Wieers <dag@wieers.com> - 3.40-1 - 5214+/dag
- Updated to release 3.40.

* Thu Jan 11 2007 Dag Wieers <dag@wieers.com> - 3.35-1
- Updated to release 3.35.

* Fri Oct 20 2006 Matthias Saou <http://freshrpms.net/> 3.31-2
- Pull in firefox instead of mozilla for FC6 and non-Fedora.
- Remove the libxpcom.so filtering since firefox now provides it again.

* Tue Aug 29 2006 Dag Wieers <dag@wieers.com> - 3.31-1
- Updated to release 3.31.

* Tue May 30 2006 Matthias Saou <http://freshrpms.net/> 3.25-2
- Add modular X build requirements and conditional.
- Clean up build requirements.
- Filter out libxpcom.so from the requirements since it would pull in mozilla
  to satisfy it, although firefox alone works fine since it includes it too,
  although it doesn't provide it (why?...).

* Tue Apr 11 2006 Dag Wieers <dag@wieers.com> - 3.25-1
- Updated to release 3.25.

* Mon Feb 13 2006 Dag Wieers <dag@wieers.com> - 3.21-1
- Updated to release 3.21.

* Thu Dec 08 2005 Dag Wieers <dag@wieers.com> - 3.17-1
- Updated to release 3.17.

* Wed Nov 30 2005 Dag Wieers <dag@wieers.com> - 3.16-1
- Updated to release 3.16.

* Wed Sep 14 2005 Dag Wieers <dag@wieers.com> - 3.11-1
- Updated to release 3.11.

* Tue Sep 13 2005 Dag Wieers <dag@wieers.com> - 3.10-1
- Updated to release 3.10.

* Sat Aug 06 2005 Dag Wieers <dag@wieers.com> - 3.05-1
- Updated to release 3.05.

* Wed Jul 13 2005 Dag Wieers <dag@wieers.com> - 2.85-1
- Updated to release 2.85.

* Tue Feb 15 2005 Dag Wieers <dag@wieers.com> - 2.80-13
- Added makefile patch, that adds locale.
- Increased the accidental release inflation :)

* Tue Feb 15 2005 Dag Wieers <dag@wieers.com> - 2.80-1
- Updated to release 2.80.

* Thu Nov 18 2004 Dag Wieers <dag@wieers.com> - 2.70-2
- Removed %%{_libdir}/mozilla/plugins/

* Mon Sep 27 2004 Dag Wieers <dag@wieers.com> - 2.70-1
- Updated to release 2.70.

* Thu Aug 12 2004 Dag Wieers <dag@wieers.com> - 2.66-1
- Don't require mozilla. (Wayne Steenburg)
- Updated to release 2.66.

* Sat Jun 19 2004 Dag Wieers <dag@wieers.com> - 2.65-1
- Updated to release 2.65.

* Thu Apr 22 2004 Dag Wieers <dag@wieers.com> - 2.60-2
- Moved mozilla-devel from Obsolets to BuildRequires, duh. (Kevin DeKorte)

* Wed Apr 21 2004 Dag Wieers <dag@wieers.com> - 2.60-1
- Renamed package back to mplayerplug-in.
- Updated to release 2.60.

* Fri Oct 10 2003 Dag Wieers <dag@wieers.com> - 0.95-1
- Disabled using MIME-types and fix config files.

* Mon Oct 06 2003 Dag Wieers <dag@wieers.com> - 0.95-0
- Updated to release 0.95.

* Thu Sep 11 2003 Dag Wieers <dag@wieers.com> - 0.91-0
- Updated to release 0.91.

* Sun Apr 20 2003 Dag Wieers <dag@wieers.com> - 0.71-0
- Initial package. (using DAR)
