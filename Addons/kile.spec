
Name:	 kile
Summary: (La)TeX source editor and TeX shell
Version: 2.0.3
Release: 1%{?dist}.1

License: GPL
Group: 	 Applications/Publishing
URL:	 http://kile.sourceforge.net/
Source0: http://dl.sourceforge.net/sourceforge/kile/kile-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: kdelibs-devel

Requires: tetex-latex
## Optional/recommended, but not absolutely required.
#Requires(hint): gnuplot
#Requires(hint): xfig

# kile-i18n is no longer separate pkg
Obsoletes: kile-i18n < %{version}=%{release}
#Provides: kile-i18n = %{version}-%{release}

%description
Kile is a user friendly (La)TeX editor.  The main features are:
  * Compile, convert and view your document with one click.
  * Auto-completion of (La)TeX commands
  * Templates and wizards makes starting a new document very little work.
  * Easy insertion of many standard tags and symbols and the option to define
    (an arbitrary number of) user defined tags.
  * Inverse and forward search: click in the DVI viewer and jump to the
    corresponding LaTeX line in the editor, or jump from the editor to the
    corresponding page in the viewer.
  * Finding chapter or sections is very easy, Kile constructs a list of all
    the chapter etc. in your document. You can use the list to jump to the
    corresponding section.
  * Collect documents that belong together into a project.
  * Easy insertion of citations and references when using projects.
  * Advanced editing commands.


%prep
%setup -q -n %{name}-%{version}%{?beta}


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

%configure \
  --disable-rpath \
  --disable-gcc-hidden-visibility \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependency-tracking --enable-final 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
  --add-category="X-Fedora" --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde \
  $RPM_BUILD_ROOT%{_datadir}/applications/kde/*.desktop
  
## File lists
# locale's
%find_lang %{name} || touch %{name}.lang
# HTML (1.0)
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d $RPM_BUILD_ROOT$HTML_DIR ]; then
for lang_dir in $RPM_BUILD_ROOT$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done
fi

## conflicting files (with kde > 3.2)
rm -rf $RPM_BUILD_ROOT%{_datadir}/apps/katepart


%post
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:

%postun
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/*
%{_datadir}/apps/kile/
%{_datadir}/apps/kconf_update/kile*
%config %{_datadir}/config*/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/kde/*.desktop
%{_datadir}/mimelnk/*/*.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Nov 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.3-1
- kile-1.9.3, CVE-2006-6085 (#217238)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.2-4
- revert to saner/simpler symlink handling

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.2-3
- fc6 respin

* Sun Aug 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.2-1
- kile-1.9.2

* Sat Jun 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.1-1
- kile-1.9.1

* Mon May 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9-2
- safer abs->rel symlink conversion 

* Fri Mar 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9-1
- 1.9(final)

* Mon Mar 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9-0.1.rc
- 1.9rc1

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Thu Nov 10 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.3-7
- fix symlinks
- simplify configure

* Fri Oct 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.3-5
- %%description: < 80 columns
- %%post/%%postun: update-desktop-database
- touchup %%post/%%postun icon handling to match icon spec
- absolute->relative symlinks
- remove Req: qt/kdelibs crud

* Tue Oct 11 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.3-4
- use gtk-update-icon-cache (#170291)

* Thu Aug 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.1-3
- fix broken Obsoletes (#166300)

* Thu Jun 02 2005 Rex Dieter 1.8.1-1
- 1.8.1
- x86_64 fix (bug #161343)

* Tue May 31 2005 Rex Dieter 1.8-2
- Obsoletes: kile-i18n

* Mon May 23 2005 Rex Dieter 1.8-1
- 1.8 

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.7.1
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:1.7.1-3
- fix (katepart) conflicts with kde >= 3.2
- update %%description

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:1.7.1-0.fdr.2
- -katepart: fix conflicts with kde >= 3.3 (optional)

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:1.7.1-0.fdr.1
- 1.7.1

* Tue Sep 28 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.3-0.fdr.2
- respin (against kde-3.3)

* Fri May 14 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.3-0.fdr.1
- 1.6.3

* Sun Mar 28 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.2-0.fdr.2
- BuildRequires: gettext

* Mon Mar 22 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.2-0.fdr.1
- 1.6.2

* Wed Mar 17 2004 Rex Dieter <rexdietet at sf.net> 0:1.6.1-0.fdr.7
- fix detection/usage of desktop-file-install

* Thu Mar 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.6
- properly fix desktop file.
- BuildRequires: fam-devel for lame/broken (err, fc2) kde builds.

* Thu Mar 11 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.5
- dynamically determine versions for qt and kdelibs dependancies.

* Wed Mar 10 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.4
- loosen Requires a bit

* Tue Mar 09 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.3
- --disable-rpath

* Tue Mar 09 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.2
- respin for kde-3.2.1

* Wed Feb 11 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.1
- Allow for building on/for both kde-3.1/kde-3.2

* Sun Feb 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.0
- 1.6.1

* Mon Dec 01 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.5
- add BuildRequires to satisfy fedora's build system.

* Wed Nov 26 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.4
- removed Utility;TextEditor desktop Categories.

* Wed Nov 26 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.3
- Requires: tetex-latex
- configure --disable-rpath
- remove Obsoletes: ktexmaker2

* Mon Nov 24 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.2
- fixup file lists
- update macros for Fedora Core support

* Sat Nov 01 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.1
- 1.6

* Wed Sep 17 2003 Rex Dieter <rexdieter at sf.net> 0:1.5.2-0.fdr.4
- fix missing latexhelp.html

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:1.5.2-0.fdr.3
- patch1 

* Wed Aug 20 2003 Rex Dieter <rexdieter at sf.net> 0:1.5.2-0.fdr.2
- 1.5.2

* Fri May 30 2003 Rex Dieter <rexdieter at sf.net> 0:1.5-0.fdr.2
- re-add %%find_lang and %%doc files not present in 1.5.2a

* Thu May 29 2003 Rex Dieter <rexdieter at sf.net> 0:1.5-0.fdr.1
- resync with unstable branch.

* Fri May 16 2003 Rex Dieter <rexdieter at sf.net> 0:1.5-0.fdr.0
- bite bullet now, revert back to 1.5.
- fedora versioning.

* Fri Apr 25 2003 Rex Dieter <rexdieter at sf.net> 1.50-0.0
- 1.5 release, artificially use 1.50 so rpm thinks it is > 1.32.

* Fri Apr 25 2003 Rex Dieter <rexdieter at sf.net> 1.40-1.3
- remove %%doc NEWS

* Mon Mar 03 2003 Rex Dieter <rexdieter at sf.net> 1.40-1.2 
- version: 1.4 -> 1.40 so silly rpm knows that 1.40 is newer than 1.32
- use epochs in Obsoletes/Provides/Requires.

* Fri Feb 21 2003 Rex Dieter <rexdieter at sf.net> 1.4-1.1
- yank kmenu

* Tue Feb 18 2003 Rex Dieter <rexdieter at sf.net> 1.4-1.0
- 1.40
- use desktop-create-kmenu

* Fri Feb 07 2003 Rex Dieter <rexdieter at sf.net> 1.32-0.0
- 1.32
- kde-redhat versioning

* Tue Jan 14 2003 Rex Dieter <rdieter@unl.edu> 1.31-0
- 1.31
- update Url, Vendor
- specfile cleanup

* Fri Oct 25 2002 Rex Dieter <rdieter@unl.edu> 1.3-1
- 1.3 (final).

* Wed Oct 23 2002 Rex Dieter <rdieter@unl.edu> 1.3-0.beta.1
- 1.3beta.

* Mon Sep 09 2002 Rex Dieter <rdieter@unl.edu> 1.2-0
- 1.2

* Wed Aug 21 2002 Rex Dieter <rdieter@unl.edu> 1.1-1.1
- workaround automake bug.

* Wed Aug 14 2002 Rex Dieter <rdieter@unl.edu> 1.1-1.0
- rebuild on/for kde 3.0.3

* Fri Aug 09 2002 Rex Dieter <rdieter@unl.edu> 1.1-0.0
- first shot at 1.1

* Mon Jul 08 2002 Rex Dieter <rdieter@unl.edu. 1.0-2
- rebuild for kde 3.0.2

* Sun Jun 16 2002 Rex Dieter <rdieter@unl.edu> 1.0-1
- 1.0
