
%define _with_aiksaurus --with-aiksaurus
%define _without_included_boost --without-included-boost

Summary: WYSIWYM (What You See Is What You Mean) document processor
Name:	 lyx
Version: 1.6.4
Release: 1%{?dist}

License: GPLv2+
Group: 	 Applications/Publishing
Url: 	 http://www.lyx.org/
#Source0: ftp://ftp.lyx.org/pub/lyx/stable/lyx-%{version}.tar.bz2
Source0: ftp://ftp.devel.lyx.org/pub/lyx/stable/lyx-%{version}%{?pre}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: lyx-1.6.4-xdg_open.patch

Source1: lyxrc.dist

Source10: lyx.desktop

%if 0%{?_with_aiksaurus:1}
BuildRequires: aiksaurus-devel
%endif
BuildRequires: aspell-devel
%if 0%{?_without_included_boost:1}
BuildRequires: boost-devel
%endif
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: python
BuildRequires: qt4-devel
BuildRequires: zlib-devel

# optional minimal qt4 dep
%{?_qt_version:Requires: qt4 >= %{_qt4_version}}

Obsoletes: %{name}-qt < 1.5.0 
Provides:  %{name}-qt = %{version}-%{release}
Obsoletes: %{name}-xforms < 1.5.0 

BuildRequires: tetex-dvips tetex-latex tetex-fonts
Requires(post): tetex-fonts
Requires(postun): tetex-fonts
Requires: tetex-dvips tetex-latex
Requires: mathml-fonts
Requires: ghostscript
Requires(hint): tetex-dvipost
Requires(hint): tetex-preview
Requires(hint): tetex-IEEEtran
# convert doc files to lyx (bug #193858)
Requires(hint): wv
Requires(hint): xdg-utils

%description
LyX is a modern approach to writing documents which breaks with the
obsolete "typewriter paradigm" of most other document preparation
systems.

It is designed for people who want professional quality output
with a minimum of time and effort, without becoming specialists in
typesetting.

The major innovation in LyX is WYSIWYM (What You See Is What You Mean).
That is, the author focuses on content, not on the details of formatting.
This allows for greater productivity, and leaves the final typesetting
to the backends (like LaTeX) that are specifically designed for the task.

With LyX, the author can concentrate on the contents of his writing,
and let the computer take care of the rest.



%prep

%setup -q -n %{name}-%{version}%{?pre}

%patch1 -p1 -b .xdg_open


%build

%configure \
  --disable-dependency-tracking \
  --disable-rpath \
  --enable-build-type=release \
  --enable-optimization="%{optflags}" \
  --with-aspell \
  --with-qt4-dir=`pkg-config --variable=prefix QtCore` \
  %{?_with_aiksaurus} \
  %{?_without_included_boost}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# misc/extras
install -p -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/lyx/lyxrc.dist

# Set up the lyx-specific class files where TeX can see them
texmf=%{_datadir}/texmf
mkdir -p %{buildroot}${texmf}/tex/latex
mv %{buildroot}%{_datadir}/lyx/tex \
   %{buildroot}${texmf}/tex/latex/lyx

# .desktop
desktop-file-install --vendor="" \
  --dir="%{buildroot}%{_datadir}/applications" \
  %{SOURCE10}

# icon
install -p -D -m644 lib/images/lyx.png \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/lyx.png

# ghost'd files
touch %{buildroot}%{_datadir}/lyx/lyxrc.defaults
touch %{buildroot}%{_datadir}/lyx/{packages,textclass}.lst
touch %{buildroot}%{_datadir}/lyx/doc/LaTeXConfig.lyx

# unpackaged files
rm -rf %{buildroot}%{_datadir}/lyx/fonts

%find_lang %{name}


%check
make check


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  texhash >& /dev/null 
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
texhash >& /dev/null
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

## Catch installed/uninstalled helpers
##   not sure if this is really needed anymore, as it seems to be a per-user thing,
##   and besides, we use xdg-open now -- Rex
%triggerin -- latex2html,wv
if [ $2 -gt 1 ]; then
cd %{_datadir}/lyx && ./configure.py --without-latex-config > /dev/null 2>&1 ||:
fi

%triggerun -- latex2html,wv
if [ $2 -eq 0 ]; then
cd %{_datadir}/lyx && ./configure.py --without-latex-config > /dev/null 2>&1 ||:
fi


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ANNOUNCE lib/CREDITS NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/lyx/
%config(noreplace) %{_datadir}/lyx/lyxrc.dist
%ghost %{_datadir}/lyx/lyxrc.defaults
%ghost %{_datadir}/lyx/*.lst
%ghost %{_datadir}/lyx/doc/LaTeXConfig.lyx
%{_datadir}/texmf/tex/latex/lyx/


%changelog
* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.6.3-1
- lyx-1.6.3

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.6.2-2
- scriptlet optimization

* Sun Mar 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.6.2-1
- lyx-1.6.2
- use --without-included-boost unconditionally

* Wed Mar 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.6.1-3
- --without-included-boost (f11+)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.1-1
- lyx-1.6.1

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.6.0-2
- Rebuild for Python 2.6

* Fri Nov 07 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-1
- lyx-1.6.0(final)

* Tue Oct 28 2008 José Matos <jamatos@fc.up.pt> - 1.6.0-0.11.rc5
- lyx-1.6.0rc5

* Fri Oct 24 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-0.10.rc4
- lyx-1.6.0rc4

* Tue Sep 30 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-0.9.rc3
- lyx-1.6.0rc3

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-0.8.rc3
- lyx-1.6.0rc3-svn26576

* Fri Sep 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-0.7.rc2
- lyx-1.6.0rc2

* Wed Aug 06 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-0.6.rc1
- lyx-1.6.0rc1

* Sun Aug 03 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-0.5.beta4
- Requires: dvipdfm (f9+, #448647)
- add (optional) minimal qt4 dep
- make Req: tex-simplecv fedora only
- drop file deps (texhash)

* Wed Jul 16 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6.0-0.4.beta4
- Changelog has been removed from the distribution

* Wed Jul 16 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6.0-0.3.beta4
- icon has changed from xpm to png

* Wed Jul 16 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6.0-0.2.beta4
- revert to use pre instead of devrel.
- require tex-simplecv (#428526)

* Wed Jul 16 2008 José Matos <jamatos[AT]fc.up.pt> - 1.6.0-0.1.beta4
- lyx-1.6.0beta4
- --enable-build-type=release disables extra debug information (no
    warnings, debug, assertions, concept-checks and stdlib-debug).

* Mon May 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5.5-1
- lyx-1.5.5

* Mon Feb 25 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5.4-1
- lyx-1.5.4 (#434689)
- reintroduce xdg-utils patch (reverted upstream).
- omit bakoma ttf fonts

* Mon Feb 11 2008 José Matos <jamatos[AT]fc.up.pt> - 1.5.3-2
- Rebuild for gcc 4.3

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.3-1
- lyx-1.5.3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.2-2
- drop scriptlet optimization hack

* Mon Oct 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.2-1
- lyx-1.5.2

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.1-2
- respin (BuildID)

* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.1-1
- lyx-1.5.1
- License: GPLv2+

* Wed Jul 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-1
- lyx-1.5.0(final)

* Sun Jul 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.10.rc2
- upstream patch for 'lyx --export latex' crasher (#248282)

* Thu Jun 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.9.rc2
- scriptlet optmization

* Thu Jun 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.8.rc2
- lyx-1.5.0rc2

* Fri Jun 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.7.rc1
- lyx-1.5.0rc1

* Fri May 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.6.beta3
- lyx-1.5.0beta3

* Sun Apr 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.5.beta2
- lyx-1.5.0beta2

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.4.beta1
- fix qt-4.3 crasher

* Tue Mar 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.3.beta1
- stop omitting -fexceptions

* Wed Mar 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.2.beta1
- +Requires: tetex-IEEEtran (#232840)

* Mon Mar 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5.0-0.1.beta1
- lyx-1.5.0beta1
- tweak lyxrc.dist

* Thu Feb 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.4-2
- biffed sources, respin

* Wed Feb 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.4-1
- lyx-1.4.4
- .desktop's: -Category=Application
- mark -xforms as deprecated

* Sun Oct 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.3-3
- sync .desktop files with upstream
- use xdg-open as default helper, +Requires: xdg-utils

* Thu Sep 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.3-1
- lyx-1.4.3

* Thu Sep 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.2-5
- fc6 respin

* Thu Aug 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.2-4
- owowned files, incomplete package removal (bug #201197)

* Thu Jul 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.2-2
- 1.4.2

* Wed Jun 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-9
- Requires(hint): wv (bug #193858)
- fix dependancy -> dependency

* Thu Jun 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-8
- BR: gettext
- fc4: restore Requires(hint): tetex-preview

* Thu May 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-7.1
- fc4: drop Requires: tetex-preview, it's not ready yet.

* Wed May 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-7
- use serverpipe "~/.lyx/lyxpipe" instead, that was the old default
  and what pybibliographer expects.

* Tue May 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-6
- set defaults for (see %{_datadir}/lyx/lyxrc.defaults.custom)
  screen_font_roman "Serif"
  screen_font_sans "Sans"
  screen_font_typewriter "Monospace"
  screen_zoom 100
  serverpipe "~/.lyx/pipe"
  (bug #192253)

* Mon May 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-5
- Requires(hint): tetex-preview

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-4
- add generic app icon (rh #191944)

* Fri Apr 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-3
- Requires(hint): tetex-dvipost
  adds support for lyx's Document->Change Tracking

* Tue Apr 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.1-2
- 1.4.1

* Thu Mar 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-5
- %%trigger ImageMagick (#186319)

* Thu Mar 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-4
- fix stripping of -fexceptions from %%optflags

* Wed Mar 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-3
- include beamer.layout

* Wed Mar 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-2
- 1.4.0(final)
- drop boost bits

* Tue Mar 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.12.rc
- 1.4.0rc
- drop boost patch (for now)

* Fri Mar 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.11.pre6
- 1.4.0pre6
- --disable-stdlib-debug --disable-assertions --disable-concept-checks
- don't use --without-included-boost (for now)

* Mon Feb 20 2006 Rex Dieter <rexdieter[AT]usres.sf.net> 1.4.0-0.10.pre5
- gcc41 patch
- document boost/gcc41 patches
- avoid --without-included-boost on fc4/gcc-4.0.2 (gcc bug)

* Tue Feb 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.9.pre5
- updated boost patch
- drop -fexceptions from %%optflags

* Mon Feb 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.7.pre5
- --without-included-boost
- BR: boost-devel

* Mon Feb 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.5.pre5
- 1.4.0pre5

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.2.pre4
- 1.4.0pre4

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0-0.1.pre3
- 1.4.0pre3

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.7-4
- cleanup/fix snarfing of intermediate frontend builds.

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.7-2
- BR: libXpm-devel

* Tue Jan 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.7-1
- 1.3.7
- -qt/-xforms: frontend pkgs (#178116)

* Fri Oct 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.6-5
- %%post/%%postun: update-desktop-database

* Fri Sep 02 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.6-4
- leave out kde-redhat bits in Fedora Extras build
- define/use safer (esp for x86_64) QTDIR bits

* Fri Aug 05 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.6-3
- touchup helpers script
- fix for (sometimes missing) PSres.upr

* Mon Aug 01 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.6-2
- use triggers to configure/unconfigure helper (ps/pdf/html) apps

* Sat Jul 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.3.6-1
- 1.3.6

* Mon May 23 2005 Rex Dieter <rexdieter[At]users.sf.net> 1.3.5-4
- qt_immodule patch (lyx bug #1830)
- update -helpers patch to look-for/use evince (rh bug #143992)
- drop (not-strictly-required) Req's on helper apps
  htmlview, gsview (rh bug #143992)
- %%configure: --with-aiksaurus
- %%configure: --enable-optimization="$$RPM_OPT_FLAGS"
- %%configure: --disable-dependency-tracking

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.3.5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Oct 21 2004 Rex Dieter <rexdieter[At]users.sf.net> 0:1.3.5-3
- BR: htmlview
- Requires: htmlview, gsview (so build-time-detected helper apps are
  available at runtime)

* Thu Oct 21 2004 Rex Dieter <rexdieter[At]users.sf.net> 0:1.3.5-0.fdr.3
- BR: htmlview
- Requires: htmlview, gsview (so build-time-detected helper apps are
  available at runtime)

* Wed Oct 20 2004 Rex Dieter <rexdieter[At]users.sf.net> 0:1.3.5-0.fdr.2
- BR: pspell-devel -> aspell-devel
- BR: tetex-* (helper detection, fonts)
- -helpers patch: find/use htmlview, gsview, kdvi, ggv, kghostview
- .desktop: GenericName: WYSIWYM document processor

* Wed Oct 06 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.5-0.fdr.1
- 1.3.5

* Fri Apr 30 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.6
- BR: libtool

* Fri Apr 23 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.5
- Group: Applications/Publishing
- BR: desktop-file-utils
- Requires(post,postun): tetex

* Sat Apr 10 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.4
- .desktop: separate file
- .desktop: drop 'Utility' category, add 'Qt'
- .desktop: Name: lyx -> LyX
- .desktop: Comment: lyx 1.3.4 -> WYSIWYM document processor
- convert icon xpm -> png

* Thu Mar 11 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.3
- dynamically determine version for qt dependency.

* Tue Mar 09 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.2
- add a few (mostly superfluous) BuildRequires to make fedora.us's
  buildsystem happy.

* Tue Mar 09 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.1
- Allow building/use for any qt >= 3.1

* Thu Feb 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.3.4-0.fdr.0
- 1.3.4
- Categories=Office

* Mon Nov 24 2003 Rex Dieter <rexdieter at sf.net> 0:1.3.3-0.fdr.3
- Requires: tetex-latex
- support MimeType(s): application/x-lyx;text/x-lyx

* Sat Nov 22 2003 Rex Dieter <rexdieter at sf.net> 0:1.3.3-0.fdr.2
- let rpm auto-require qt.
- remove (optional) xforms support.
- Requires: latex-xft-fonts

* Mon Oct 06 2003 Rex Dieter <rexdieter at sf.net> 0:1.3.3-0.fdr.1
- 1.3.3
- update macros for Fedora Core.

* Mon May 12 2003 Rex Dieter <rexdieter at users.sf.net> 0:1.3.2-0.fdr.0
- 1.3.2
- fedora-ize.

* Tue Mar 25 2003 Rex Dieter <rexdieter at users.sf.net> 1.3.1-1.0
- 1.3.1 release.

* Fri Feb 21 2003 Rex Dieter <rexdieter at users.sf.net> 1.3.0-1.0
- yank kmenu

* Fri Feb 07 2003 Rex Dieter <rexdieter at users.sf.net> 1.3.0-0.0
- 1.3.0

