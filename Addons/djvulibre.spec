Summary: DjVu viewers, encoders, utilities and web browser plugin
Name: djvulibre
Version: 3.5.18
Release: 1%{?dist}
License: GPL
Group: Applications/Publishing
URL: http://djvu.sourceforge.net/
Source: http://dl.sf.net/djvu/djvulibre-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): xdg-utils, /sbin/ldconfig
Requires(preun): xdg-utils
BuildRequires: qt-devel, libjpeg-devel, libtiff-devel
BuildRequires: xdg-utils
# Virtual provides... might be worth splitting out for multilib, but then we'd
# probably need a separate -libs package to have 64bit tools and 32bit plugin
Provides: mozilla-djvulibre = %{version}-%{release}

%description
DjVu is a web-centric format and software platform for distributing documents
and images. DjVu can advantageously replace PDF, PS, TIFF, JPEG, and GIF for
distributing scanned documents, digital documents, or high-resolution pictures.
DjVu content downloads faster, displays and renders faster, looks nicer on a
screen, and consume less client resources than competing formats. DjVu images
display instantly and can be smoothly zoomed and panned with no lengthy
re-rendering.

DjVuLibre is a free (GPL'ed) implementation of DjVu, including viewers, browser
plugins, decoders, simple encoders, and utilities.


%package devel
Summary: Development files for djvulibre
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
Development files for djvulibre.


%prep
%setup


%build
%configure
# In 3.5.14 %{?_smp_mflags} broke the build - still in 3.5.18
%{__make} OPTS="%{optflags}"


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Move plugin from the netscape directory to the main mozilla one
%{__mkdir_p} %{buildroot}%{_libdir}/mozilla/plugins/
%{__mv} %{buildroot}%{_libdir}/netscape/plugins/nsdejavu.so \
        %{buildroot}%{_libdir}/mozilla/plugins/nsdejavu.so

# Fix for the libs to get stripped correctly (still required in 3.5.18)
find %{buildroot}%{_libdir} -name '*.so*' | xargs %{__chmod} +x


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/ldconfig
# Menu entry (icons and desktop file)
%{_datadir}/djvu/djview3/desktop/register-djview-menu install || :
# MIME types (icons and desktop file)
%{_datadir}/djvu/osi/desktop/register-djvu-mime install || :

%preun
# Removal, not update
if [ $1 -eq 0 ]; then
    # Menu entry (icons and desktop file)
    %{_datadir}/djvu/djview3/desktop/register-djview-menu uninstall || :
    # MIME types (icons and desktop file)
    %{_datadir}/djvu/osi/desktop/register-djvu-mime uninstall || :
fi

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc README COPYRIGHT COPYING NEWS TODO doc/
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/mozilla/plugins/nsdejavu.so
%{_datadir}/djvu/
%{_mandir}/man1/*
#lang(de) %{_mandir}/de/man1/*
#lang(fr) %{_mandir}/fr/man1/*
%lang(ja) %{_mandir}/ja/man1/*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/libdjvu/
%{_libdir}/pkgconfig/ddjvuapi.pc
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Mon Feb  5 2007 Matthias Saou <http://freshrpms.net/> 3.5.18-1
- Update to 3.5.18.
- Remove no longer needed /usr/include/qt3 replacing.
- Replace desktop build requirements and scriplets with new xdg utils way.
- Include new de and fr man page translations... not! Directories are empty.
- Split -devel sub-package, as the new djview4 should build require it.
- No longer build require a web browser, the plugin always gets built now.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 3.5.17-2
- FC6 rebuild.
- Use mozilla up to FC5, and seamonkey for FC6+ and non-Fedora.
- Build require gnome-mime-data to get build time detected dirs in place.

* Sun Jul  2 2006 Matthias Saou <http://freshrpms.net/> 3.5.17-1
- Update to 3.5.17.

* Tue Mar 14 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-3
- Update to CVS snapshot, fixes the build with gcc 4.1 (sf.net #1420522).. NOT!
- Include workaround for wrong qt3 includes in gui/djview/Makefile.dep.
- Add new pkgconfig ddjvuapi.pc file.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-2
- FC5 rebuild... nope.

* Mon Jan 30 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-1
- Update to 3.5.16.
- Add conditional to build with/without modular X depending on FC version.
- Remove no longer needed gcc4 patch.
- Add extra qualification patch.

* Thu Aug  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.15-2
- Include djvulibre-3.5.15-gcc401.patch to fix compilation with gcc 4.0.1.
- Add hicolor-icon-theme build req for /usr/share/icons/hicolor/48x48/mimetypes
  to exist.

* Thu Aug  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.15-1
- Update to 3.5.15.
- Move desktop icon to datadir/icons/hicolor.
- Add gtk-update-icon-cache calls for the new icon.
- Move browser plugin from netscape to mozilla directory instead of symlinking.
- Clean build requirements and add libtiff-devel.
- Add redhat-menus build req since it owns /etc/xdg/menus/applications.menu,
  which the configure script checks to install the desktop file.
- Add OPTS to the make line (#156208 - Michael Schwendt).

* Tue May  3 2005 David Woodhouse <dwmw2@infradead.org> 3.5.14-6
- Remove files that were installed only for older KDE versions.

* Mon Feb 14 2005 David Woodhouse <dwmw2@infradead.org> 3.5.14-4
- Include %%{_datadir}/mimelnk/image/x-djvu.desktop

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-3
- Bump release to provide Extras upgrade path.

* Fri Nov  5 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-2
- Re-enable the lib/mozilla/ symlink to the plugin.
- Add source of /etc/profile.d/qt.sh to fix weird detection problem on FC3...
  ...doesn't fix it, some lib required by qt is probably installed after and
  ldconfig not run.
- Added lib +x chmod'ing to get proper stripping and debuginfo package.

* Sat Oct 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-2
- Added update-desktop-database scriplet calls.

* Mon Aug 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-1
- Update to 3.5.14.
- Added newly introduced files to the package.

* Mon May 17 2004 Matthias Saou <http://freshrpms.net/> 3.5.13-1
- Update to 3.5.13.
- Added new Japanese man pages.

* Wed May  5 2004 Matthias Saou <http://freshrpms.net/> 3.5.12-4
- Changed the plugin directory for mozilla to %{_libdir}/mozilla,
  as suggested by Matteo Corti.
- Shortened the description.

* Wed Jan 14 2004 Matthias Saou <http://freshrpms.net/> 3.5.12-3
- Added XFree86-devel and libjpeg-devel build requirements.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 3.5.12-2
- Rebuild for Fedora Core 1.

* Mon Sep  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.12.

* Thu May  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.11.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Thu Mar 20 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.10.

* Wed Jul 24 2002 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.7.

* Fri Jul 19 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup and fixes.

* Wed May 29 2002 Leon Bottou <leon@bottou.org>
- bumped to version 3.5.6-1

* Mon Apr 1 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.5-2
- changed group to Applications/Publishing

* Tue Mar 25 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.5-2

* Tue Jan 22 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.4-1.
- fixed for properly locating the man directory.
- bumped to version 3.5.4-2.

* Wed Jan 16 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.3-1

* Fri Dec  7 2001 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.2-1.

* Wed Dec  5 2001 Leon Bottou <leonb@users.sourceforge.net>
- created spec file for rh7.x.

