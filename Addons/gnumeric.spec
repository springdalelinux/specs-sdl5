Name:             gnumeric
Epoch:            1
Version:          1.6.3
Release:          15%{?dist}.2
Summary:          Spreadsheet program for GNOME
Group:            Applications/Productivity
# bug filed upstream about this being GPL v2 only:
# http://bugzilla.gnome.org/show_bug.cgi?id=463247
License:          GPLv2
URL:              http://www.gnome.org/gnumeric/
Source:           ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/1.6/%{name}-%{version}.tar.bz2
Patch0:           gnumeric-1.6.1-desktop.patch
Patch1:           gnumeric-1.4.1-excelcrash.patch
Patch2:           gnumeric-1.6.3-helppath.patch
Patch3:           gnumeric-1.6.3-gda3.patch
Patch4:           gnumeric-1.6.3-gpl-md5.patch
Patch5:           gnumeric-1.6.3-stf-parse.patch
Patch6:           gnumeric-1.6.3-excel-overflow.patch
Patch7:           gnumeric-1.6.3-pypath.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-root
BuildRequires:    libgnomeui-devel >= 2.4.0
BuildRequires:    libgnomeprintui22-devel >= 2.8.2
BuildRequires:    libgsf-devel >= 1.13.2
BuildRequires:    libgnomedb-devel >= 3.0.0
BuildRequires:    pygtk2-devel >= 2.6.0
BuildRequires:    goffice-devel >= 0.2.0
BuildRequires:    python-devel guile-devel perl(XML::Parser) scrollkeeper
BuildRequires:    gettext desktop-file-utils
Requires:         scrollkeeper hicolor-icon-theme
Requires(pre):    GConf2
Requires(post):   /sbin/ldconfig GConf2 scrollkeeper
Requires(preun):  GConf2
Requires(postun): /sbin/ldconfig scrollkeeper

%description
Gnumeric is a spreadsheet program for the GNOME GUI desktop
environment.


%package devel
Summary: Files necessary to develop gnumeric-based applications
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Gnumeric is a spreadsheet program for the GNOME GUI desktop
environment. The gnumeric-devel package includes files necessary to
develop gnumeric-based applications.


%prep
%setup -q
%patch0 -p1 -b .desktop
%patch1 -p1 -b .excelcrash
%patch2 -p1 -b .helppath
%patch3 -p1 -b .gda3
%patch4 -p1 -b .gpl-md5
%patch5 -p1 -b .csv
%patch6 -p1 -b .excel
%patch7 -p1 -b .pypath
chmod -x plugins/excel/rc4.?


%build
%configure --without-gb --enable-ssindex
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

/usr/lib/rpm/find-lang.sh $RPM_BUILD_ROOT %{name} --all-name --with-gnome

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora --delete-original                  \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications                         \
  --add-category Office                                                 \
  --add-category Spreadsheet                                            \
  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

#put icon in the proper place
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/48x48/apps
mv $RPM_BUILD_ROOT/usr/share/pixmaps/gnome-%{name}.png \
  $RPM_BUILD_ROOT/usr/share/icons/hicolor/48x48/apps/%{name}.png

#remove unused mime type icons
rm $RPM_BUILD_ROOT/%{_datadir}/pixmaps/gnome-application-*.png
rm $RPM_BUILD_ROOT/%{_datadir}/pixmaps/%{name}/gnome-application-*.png

#remove spurious .ico thing
rm $RPM_BUILD_ROOT/usr/share/pixmaps/win32-%{name}.ico
rm $RPM_BUILD_ROOT/usr/share/pixmaps/%{name}/win32-%{name}.ico

#remove scrollkeeper stuff
rm -rf $RPM_BUILD_ROOT/var

#remove .la files
rm $RPM_BUILD_ROOT/%{_libdir}/libspreadsheet.la
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}/%{version}/plugins/*/*.la

#remove bogus mc stuff
rm -r $RPM_BUILD_ROOT/%{_datadir}/mc


%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}*.schemas > /dev/null || :
fi


%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
/usr/bin/gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/%{name}*.schemas > /dev/null || :
scrollkeeper-update -q -o %{_datadir}/omf/%{name} || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}*.schemas > /dev/null || :
fi


%postun
/sbin/ldconfig
scrollkeeper-update -q || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc HACKING AUTHORS ChangeLog NEWS BUGS README COPYING
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
%{_libdir}/libspreadsheet-%{version}.so
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{version}
%{_libdir}/bonobo/servers/GNOME_Gnumeric.server
%{_datadir}/pixmaps/%{name}
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{version}
%exclude %{_datadir}/%{name}/%{version}/idl
%{_datadir}/mime-info
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/omf/%{name}
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_datadir}/%{name}/%{version}/idl
%{_libdir}/libspreadsheet.so


%changelog
* Fri Jan 10 2009 Lubomir Rintel <lkundrak@v3.sk> 1:1.6.3-15.2
- Fix CVE-2009-0318 untrusted search path vulnerability

* Tue Sep 23 2008 Lubomir Rintel <lkundrak@v3.sk> 1:1.6.3-15.1
- libgsf-gnome-devel does not exist in el5 yet, replace with libgsf-devel
- Package the omf file

* Wed Feb  6 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-15
- Fix launching of gnome-database-properties from the Data -> Databases
  menu-entry (bug 431618)

* Sun Feb  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-14
- Fix integer overflow and signedness errors in XLS processing (Bug 431229)

* Thu Nov 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-13
- Fix opening of csv files in non-English locales (bz 385441)

* Wed Sep 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-12
- Replace GPL incompatible licensed md5 code with GPL compatible code from
  gnulib

* Fri Aug 31 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-11
- Fix Source0 URL

* Mon Aug  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-10
- Update License tag for new Licensing Guidelines compliance
- Don't regenerate all the autoxxx stuff (not needed) this fixes building with
  the latest intltool

* Sun Jun 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-9
- Remove yelp Requires again <sigh> (bz 243361)

* Fri Jun  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-8
- Add yelp Requires so that the help will always work (bz 243361)

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-7
- Build against new libgda + libgnomedb

* Mon Feb 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-6
- Change BuildRequires: libgsf-devel to libgsf-gnome-devel to fix rawhide build

* Sat Sep  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-5
- Various specfile cleanups
- Don't own /usr/share/omf (bug 205667)

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-4
- FE6 Rebuild

* Fri Jul 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-3
- Fix idl file being in both the main and the devel package
- Move libspreadsheet.so symlink to the devel package

* Sun May 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-2
- Add Patch3 fixing gnumeric not finding its help files (bz 192581).

* Tue May  2 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-1
- new upstream version 1.6.3

* Sat Apr  8 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.2-3
- drop bogus mc stuff (bz 169332)

* Tue Mar 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.2-2
- rebuild for new libgsf

* Thu Feb 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.2-1
- New upstream version
- Rebuild for new gcc4.1 and glibc
- add %%{?dist} for consistency with my other packages
- Update scripts to match the scriptlets wiki page

* Sat Jan 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.1-3
- Cleanup Requires
- Add (missing) call of gtk-update-icon-cache to %%post and %%postun

* Thu Dec  8 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.1-2
- Switch to core version of libgsf now Core has 1.13 instead of using special
  Extras libgsf113 version.

* Sat Nov 26 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.1-1
- new upstream stable version 1.6.1
- drop 2 integrated patches
- own dirs /usr/share/mc/templates /usr/share/mc (bug 169332)
- proper use of desktop-file-install (bug 171963)
- put icon in the proper freedesktop.org spec matching icon dir (bug 171964)
- remove unused mime-type icons
- clean up specfile, own all dirs not owned by Required packages.
- add --enable-ssindex (bug 172164)

* Thu Aug 18 2005 Jeremy Katz <katzj@redhat.com> - 1:1.4.3-6
- rebuild for changes in the devel tree

* Fri Aug 5 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.3-5
- gtk2-devel and libart_lgpl-devel where not getting sucked in because
  of a bug in another package this has been fixed now so the buildrequires
  have been removed again.

* Mon Jul 4 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.3-4
- For some reason gtk2-devel no longer gets sucked in by our other
  buildrequires so explicitly add it.
- libart_lgpl-devel is now needed for building, so add this.
- I also noticed in the configure output that gnumeric can
  use pygtk2, so add this.

* Fri Jun 17 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.3-3
- Add patch3: fix excell export with libgsf >= 0.12 (bugzilla #160075),
  Thanks to Caolan McNamara.

* Tue Mar 15 2005 Caolan McNamara <caolanm@redhat.com> 1.4.3-2
- add libgnomedb to extras and gnumeric's requires

* Mon Mar 14 2005 Caolan McNamara <caolanm@redhat.com> 1.4.3-1
- bump to latest, first in extras
- drop helppath

* Fri Feb 18 2005 Caolan McNamara <caolanm@redhat.com> 1.4.2-3
- rh#149005#

* Mon Feb  7 2005 Matthias Clasen <mclasen@redhat.com> 1.4.2-2
- rebuild

* Thu Jan 27 2005 Caolan McNamara <caolanm@redhat.com> 1.4.2-1
- bump to next version

* Wed Dec 22 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-5
- RH#143587# pango-devel >= 1.4.0

* Sun Dec 19 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-4
- libgsf must be >= 1.10.0

* Fri Dec 17 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-3
- dubious "lib" usage from 64bit POV

* Thu Dec 17 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-2
- RH#143161# crash on reading corrupt excel file

* Wed Dec 15 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-1
- bump to new version
- drop integrated 64bit patch
- drop integrated desktop.in patch
- drop integrated latex patch
- drop disable bonobo patch
- add enable perl configure patch
- add quickfix for help being searched for in wrong place #gnome161404#

* Tue Nov 02 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-9
- #rh137694# backport latex exporter fix
- #rh137692# backport x64 excel fix

* Sat Oct 30 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-7
- #rh137565# Requires libgnomedb

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 1.2.13-6
- Change Requires(post) to PreReq

* Thu Sep 30 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-5
- #rh134250# improve Requires: desktop-file-utils

* Thu Sep 30 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-4
- #rh134175# invalid mime type entry

* Mon Sep 27 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-3
- make a wild stab at #rh133662#

* Mon Sep 6 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-2
- update .keys to .desktop

* Tue Jul 27 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13
- update to 1.2.13 
- #107278# --without-bonobo, help is fairly nonfunctional otherwise

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 5 2004 Caolan McNamara <caolanm@redhat.com> 1.2.12
- update to 1.2.12 some exported excel workbooks will not work in Excel
with older versions
_ delete unused patches

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 1.2.8-2
- #74034 own plugin dir
- #111112 BR intltool scrollkeeper gettext desktop-file-utils
- some cleanup

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 1.2.8-1
- Update to 1.2.8

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 6 2004 Daniel Reed <dreed@redhat.com> 1:1.2.6-1
- Version bump (1.2.6)

* Tue Oct 14 2003 Jonathan Blandford <jrb@redhat.com> 1:1.2.1-2
- add ssconvert

* Tue Oct 14 2003 Havoc Pennington <hp@redhat.com> 1:1.2.1-1
- add %%post to install schemas
- 1.2.1

* Fri Sep 19 2003 Havoc Pennington <hp@redhat.com> 1:1.2.0-1
- 1.2.0 final

* Mon Aug 25 2003 Jonathan Blandford <jrb@redhat.com>
- new version for GNOME 2.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 29 2003 Tim Powers <timp@redhat.com> 1:1.0.12-5
- rebuild to fix broken libgal dep

* Tue Feb 18 2003 Elliot Lee <sopwith@redhat.com> 1:1.0.12-4
- Put in a fix for the no-python-on-lib64 problem.

* Wed Feb 12 2003 Havoc Pennington <hp@redhat.com> 1:1.0.12-3
- add --without-guile due to crash on 64-bit #82977

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Havoc Pennington <hp@redhat.com>
- 1.0.12
- remove libtoolize/autotools invocations, dunno why they were there

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 1.0.9-6
- Run libtool/auto*
- Rebuild

* Thu Dec 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- also disable python for mainframe, this should be fixed properly
  at some point...
- add guile to filelist

* Wed Nov  6 2002 Bill Nottingham <notting@redhat.com> 1.0.9-4
- rebuild everywhere
- no python on hammer ATM

* Thu Oct 24 2002 Jeremy Katz <katzj@redhat.com>
- rebuild against new gal
- fixup file lists to use correct macros and include all files

* Fri Aug  2 2002 Havoc Pennington <hp@redhat.com>
- desktop file fixage

* Fri Jul 26 2002 Akira TAGOH <tagoh@redhat.com> 1.0.9-1
- update to 1.0.9
- gnumeric-0.67-excel95-ja.patch: we no longer need it. removed. (Bug#62776)

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- update to 1.0.8
- remove exceljpfonts patch that no longer applies

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 10 2002 Havoc Pennington <hp@redhat.com>
- add jp excel reading patch #62776

* Wed Mar 27 2002 Havoc Pennington <hp@redhat.com>
- add multibyte patch #61624

* Mon Mar 11 2002 Havoc Pennington <hp@redhat.com>
- 1.0.5

* Wed Jan 30 2002 Tim Powers <timp@redhat.com>
- update to 1.0.3

* Tue Nov 20 2001 Jonathan Blandford <jrb@redhat.com>
- Version 0.76

* Mon Oct  8 2001 Matt Wilson <msw@redhat.com>
- removed patch4 (gnumeric-0.67-sheet_corruption.patch), in CVS now.
- removed patch8 (gnumeric-0.67-xlsscale.patch), no longer needed.
- removed patch4 (gnumeric-0.67-s390.patch), no longer needed.
- regenerated patch6 (gnumeric-0.67.lengthen-warning.patch) against 0.71
- removed patch2 (gnumeric-0.67-mb.patch), in CVS now.
- removed patch9 (gnumeric-0.67-backspace.patch), came from CVS.
- removed patch5 (gnumeric-0.67-desktop.patch), ditto
- renamed remaining patches:
    patch3 (gnumeric-0.67-excel95-ja.patch) -> patch2
    patch6 (gnumeric-0.71-lengthen-warning.patch) -> patch3
- removed source10, ja.po from upstream is more up to date.
- added files needed for bonobo gnumeric back into file list

* Wed Sep  5 2001 Owen Taylor <otaylor@redhat.com>
- Add patch from CVS to fix backspace (#53062)

* Tue Aug  7 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem with scaling percentage and XLS files (#51054)
- Fix problem where default font for ja and other locales was backwards

* Mon Aug  6 2001 Owen Taylor <otaylor@redhat.com>
- Install all files from the plugins in the main package. Putting .la
  files in the main package didn't make sense, and we were missing
  some files for the gnome-glossary package.

* Fri Aug  3 2001 Owen Taylor <otaylor@redhat.com>
- Add some missing directories to the main package (#50701)

* Tue Jul 31 2001 Than Ngo <than@redhat.com>
- add patch to build on s390, s390x

* Fri Jul 27 2001 Jonathan Blandford <jrb@redhat.com>
- change 'old copy' dialog to popup after 9 months

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Add missing contents of .desktop file from CVS

* Thu Jul 19 2001 Owen Taylor <otaylor@redhat.com>
- Move desktop file to /etc/X11/applnk (#23488)
- Added BuildPrereq on python-devel (#45029)
- Add BuildPrereq on gal-devel (#45027)
- Add <locale.h> include to .mb patch 
  (don't know why it works for me / in the build system, #32388)

* Mon Jul 16 2001 Jonathan Blandford <jrb@redhat.com>
- backport sheet corruption fix

* Tue Jul 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make devel subpackage depend on main package

* Sat Jul 07 2001 Owen Taylor <otaylor@redhat.com>
- Version 0.67

* Fri Jun 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- support newer gettext version

* Fri Mar  9 2001 Akira TAGOH <tagoh@redhat.com> 0.61-9
- Fixed read excel95's .xls for Japanese.

* Fri Feb 23 2001 Akira TAGOH <tagoh@rehdat.com> 0.61-8
- Fixed jp patch with gnome-print.

* Mon Feb 19 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed jp patch.

* Thu Feb 08 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix about Japanese translation (ja.po)

* Wed Feb 07 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update Japanese translation.

* Tue Feb 06 2001 Akira TAGOH <tagoh@redhat.com>
- Added Japanese patch.
- Updated Japanese translation.
  Note: Please remove Source10 when the next upstream release.

* Thu Jan 18 2001 Matt Wilson <msw@redhat.com>
- don't use bin:bin for files in devel.

* Wed Jan 03 2001 Preston Brown <pbrown@redhat.com>
- standard file and directory modes/ownership

* Fri Dec 29 2000 Matt Wilson <msw@redhat.com>
- use rpm > 3.0.5 macros
- 0.61

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Tue Jul 18 2000 Owen Taylor <otaylor@redhat.com>
- Fix DocDir:

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild
