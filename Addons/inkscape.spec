Name:           inkscape
Version:        0.46
Release:        2%{?dist}.1
Summary:        Vector-based drawing program using SVG

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://inkscape.sourceforge.net/
Source0:        http://download.sourceforge.net/inkscape/%{name}-%{version}.tar.bz2
Patch0:         inkscape-16571-cxxinclude.patch
Patch1:         inkscape-0.45.1-desktop.patch
Patch2:         inkscape-0.46pre2-icons.patch
Patch3:         inkscape-0.46-fixlatex.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atk-devel
BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel
BuildRequires:  gc-devel >= 6.4
BuildRequires:  gettext
BuildRequires:  gtkmm24-devel >= 2.8.0
BuildRequires:  gtkspell-devel
BuildRequires:  gnome-vfs2-devel >= 2.0
BuildRequires:  libpng-devel >= 1.2
BuildRequires:  libxml2-devel >= 2.6.11
BuildRequires:  libxslt-devel >= 1.0.15
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
BuildRequires:  lcms-devel >= 1.13
BuildRequires:  cairo-devel
BuildRequires:  openssl-devel
BuildRequires:  dos2unix
BuildRequires:  perl-XML-Parser
BuildRequires:  python-devel
BuildRequires:  poppler-devel
BuildRequires:  loudmouth-devel
BuildRequires:  boost-devel

# Use popt-devel if Fedora 8, RHEL 6, newer or unknown,
# rely on popt otherwise
%if %{!?fedora:8}%{?fedora} < 8 || %{!?rhel:6}%{?rhel} < 6
BuildRequires:  popt
%else
BuildRequires:  popt-devel
%endif

Requires:       pstoedit
Requires:       perl(Image::Magick)
Requires:       numpy
Requires:       PyXML
Requires:       python-lxml

Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

%description
Inkscape is a vector-based drawing program, like CorelDraw® or Adobe
Illustrator® from the proprietary software world, and Sketch or Karbon14 from
the free software world. It is free software, distributed under the terms of
the Gnu General Public License, Version 2.

Inkscape uses W3C SVG as its native file format. It is therefore a very useful
tool for web designers and as an interchange format for desktop publishing.

It has a relatively modern display engine, giving you finely antialiased
display, alpha transparencies, vector fonts and so on. Inkscape is written in
C and C++, using the Gtk+ toolkit and optionally some Gnome libraries.


%prep
%setup -q
%patch0 -p1 -b .cxxinclude
%patch1 -p1 -b .desktop
%patch2 -p1 -b .icons
%patch3 -p1 -b .fixlatex
find -type f -regex '.*\.\(cpp\|h\)' -perm +111 -exec chmod -x {} ';'
find share/extensions/ -type f -regex '.*\.py' -perm +111 -exec chmod -x {} ';'
dos2unix -k -q share/extensions/*.py


%build
%configure                     \
--disable-dependency-tracking  \
--with-xinerama                \
--enable-static=no             \
--with-python                  \
--with-perl                    \
--with-gnome-vfs               \
--with-inkjar                  \
--enable-inkboard              \
--enable-lcms                  \
--enable-poppler-cairo

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions/outline2svg.*
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions/txt2svg.*

desktop-file-install --vendor fedora --delete-original     \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications            \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%post
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%postun
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc %{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/fr/man1/*


%changelog
* Fri Apr 11 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-2.1
- More buildrequires more flexible, so that this builds on RHEL

* Sat Apr 05 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-2
- Fix LaTeX rendering, #441017

* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-1
- 0.46 released

* Sun Mar 23 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.3.pre3
- Rebuild for newer Poppler

* Wed Mar 12 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.2.pre3
- Probably last prerelease?

* Fri Feb 22 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.2.pre2
- Panel icon sizes

* Sun Feb 17 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.1.pre2
- 0.46pre2
- Dropping upstreamed patches

* Sat Feb 16 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-5
- Attempt to fix the font selector (#432892)

* Thu Feb 14 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-4
- Tolerate recoverable errors in OCAL feeds
- Fix OCAL insecure temporary file usage (#432807)

* Wed Feb 13 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-3
- Fix crash when adding text objects (#432220)

* Thu Feb 07 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-2
- Build with gcc-4.3

* Wed Feb 06 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-1
- 0.46 prerelease
- Minor cosmetic changes to satisfy the QA script
- Dependency on Boost
- Inkboard is not optional
- Merge from Denis Leroy's svn16571 snapshot:
- Require specific gtkmm24-devel versions
- enable-poppler-cairo
- No longer BuildRequire libsigc++20-devel

* Wed Dec  5 2007 Denis Leroy <denis@poolshark.org> - 0.45.1-5
- Rebuild with new openssl

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-4
- Added missing dependencies for modules (#301881)

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-3
- Satisfy desktop-file-validate, so that Rawhide build won't break

* Sat Dec 01 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-2
- Use GTK print dialog
- Added compressed SVG association (#245413)
- popt headers went into popt-devel, post Fedora 7
- Fix macro usage in changelog

* Wed Mar 21 2007 Denis Leroy <denis@poolshark.org> - 0.45.1-1
- Update to bugfix release 0.45.1
- Added R to ImageMagick-perl (#231563)

* Wed Feb  7 2007 Denis Leroy <denis@poolshark.org> - 0.45-1
- Update to 0.45
- Enabled inkboard, perl and python extensions
- Added patch for correct python autodetection
- LaTex patch integrated upstreamed, removed
- Some rpmlint cleanups

* Wed Dec  6 2006 Denis Leroy <denis@poolshark.org> - 0.44.1-2
- Added patches to fix LaTex import (#217699)
- Added patch to base postscript import on pstoedit plot-svg

* Thu Sep  7 2006 Denis Leroy <denis@poolshark.org> - 0.44.1-1
- Update to 0.44.1
- Removed png export patch, integrated upstream
- Some updated BRs

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 0.44-6
- FE6 Rebuild

* Tue Aug 22 2006 Denis Leroy <denis@poolshark.org> - 0.44-5
- Removed skencil Require (bug 203229)

* Thu Aug 10 2006 Denis Leroy <denis@poolshark.org> - 0.44-4
- Added patch to fix png dpi export problem (#168406)

* Wed Aug  9 2006 Denis Leroy <denis@poolshark.org> - 0.44-3
- Bumping up release to fix upgrade path

* Wed Jun 28 2006 Denis Leroy <denis@poolshark.org> - 0.44-2
- Update to 0.44
- Removed obsolete patches
- Disabled experimental perl and python extensions
- Added pstoedit, skencil, gtkspell and LittleCms support
- Inkboard feature disabled pending further security tests

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 0.43-3
- Rebuild

* Mon Jan 16 2006 Denis Leroy <denis@poolshark.org> - 0.43-2
- Updated GC patch, bug 171791

* Sat Dec 17 2005 Denis Leroy <denis@poolshark.org> - 0.43-1
- Update to 0.43
- Added 2 patches to fix g++ 4.1 compilation issues
- Enabled new jabber/loudmouth-based inkboard feature

* Mon Sep 26 2005 Denis Leroy <denis@poolshark.org> - 0.42.2-2
- rebuilt with newer glibmm

* Thu Sep  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42.2-1
- update to 0.42.2

* Thu Aug 18 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-3
- rebuilt
- add patch to repair link-check of GC >= 6.5 (needs pthread and dl)

* Fri Jul 29 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-2
- Extend ngettext/dgettext patch for x86_64 build.

* Tue Jul 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-1
- update to 0.42 (also fixes #160326)
- BR gnome-vfs2-devel
- no files left in %%_libdir/inkscape
- include French manual page
- GCC4 patch obsolete, 64-bit patch obsolete, dgettext patch split off

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-7
- append another 64-bit related patch (dgettext configure check failed)

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-6
- remove explicit aclocal/autoconf calls in %%build as they create a
  bad Makefile for FC4/i386, which causes build to fail (#156228),
  and no comment explains where they were added/needed

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-5
- bump and rebuild as 0.41-4 failed in build system setup

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.41-4
- add patch for gcc4 problems (ignacio, #156228)
- fix build on 64bit boxes.  sizeof(int) != sizeof(void*)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.41-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Feb 09 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.41-1
- 0.41.
- enable python.

* Sat Dec 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.40-1
- 0.40.

* Mon Nov 16 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.40-0.pre3
- 0.40pre3.

* Thu Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.39-0.fdr.2
- post/postun for new mime system.
- Dropped redundant BR XFree86-devel.

* Sun Aug 29 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.39-0.fdr.1
- 0.39.

* Fri Apr 10 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.1-0.fdr.1
- respin real fix for Provides/Requires for perl(SpSVG)

* Fri Apr 9 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.1-0.fdr.0
- respin with updated tarball with fix for postscript printing

* Thu Apr 8 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38-0.fdr.2
- respin to fix provides

* Thu Apr 8 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.0.fdr.1
- version upgrade with many improvements and bug fixes

* Fri Mar 19 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.7
- repsin - sourceforge does not allow reloading files with same name
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.6
- fix typo in provides
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.5
- add %%{release} to provides perl(SpSVG) = %%{epoch}:%%{version}:%%{release} only
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.4
- add %%{release} to provides
* Sun Mar 14 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.3
- add arch dependent flags
* Thu Mar 11 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.2
- add libsigc++-devel instead of add libsigc++ - duh
- add BuildRequires:  perl-XML-Parser
- fix package name to follow package naming guidelines
* Mon Mar 1 2004   P Linnell <scribusdocs at atlantictechsolutions.com>   0:0.37.1.fdr.1
- disable static libs
- enable inkjar
* Tue Feb 10  2004 P Linnell <scribusdocs at atlantictechsolutions.com>   0:0.37.0.fdr.1
- pgp'd tarball from inkscape.org
- clean out the cvs tweaks in spec file
- enable gnome-print
- add the new tutorial files
- make sure .mo file gets packaged
- add provides: perlSVG
- submit to Fedora QA
* Sat Feb 7  2004 P Linnell <scribusdocs at atlantictechsolutions.com>
- rebuild of current cvs
- tweaks to build cvs instead of dist tarball
- add inkview
* Sat Dec 20 2003 P Linnell <scribusdocs at atlantictechsolutions.com>
- First crack at Fedora/RH spec file
- nuke gnome print - it won't work (bug is filed already)
