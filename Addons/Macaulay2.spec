
#define beta 20060808svn

%define emacs_sitelisp  %{_datadir}/emacs/site-lisp/
%define xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp/
 
Summary: System for algebraic geometry and commutative algebra
Name:    Macaulay2
Version: 0.9.95
Release: 4%{?dist}

License: GPL
Group:   Applications/Engineering
URL:     http://www.math.uiuc.edu/Macaulay2/
Source0: http://www.math.uiuc.edu/Macaulay2/ftp-site/Macaulay2-%{version}-src.tar.gz
#Source0: Macaulay2-%{version}-%{beta}.tar.bz2
Source1: Macaulay2-svn_checkout.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source10: Macaulay2.png
Source11: Macaulay2.desktop

Patch0: Macaulay2-0.9.8-optflags.patch
Patch1: Macaulay2-0.9.95-xdg_open.patch 
Patch2: Macaulay2-0.9.10-cout.patch
Patch3: Macaulay2-0.9.95-DESTDIR.patch
Patch4: Macaulay2-0.9.10-gcc41.patch
Patch201739: Macaulay2-0.9.95-bz201739.patch

BuildRequires: desktop-file-utils
BuildRequires: gc-devel
BuildRequires: ntl-devel
BuildRequires: factory-devel 
BuildRequires: libfac-devel 
BuildRequires: lapack
%if 0%{?fedora} > 3 || 0%{?rhel} > 4
BuildRequires: lapack-devel
%endif
BuildRequires: gdbm-devel
BuildRequires: readline-devel ncurses-devel
BuildRequires: time
BuildRequires: byacc 
# /sbin/install-info
BuildRequires: info
# etags
BuildRequires: emacs-common
Source20: etags.sh

BuildRequires: automake

Obsoletes: Macaulay2-doc < %{version}-%{release} 
Provides:  Macaulay2-doc = %{version}-%{release}
Obsoletes: Macaulay2-emacs < %{version}-%{release}
Provides:  Macaulay2-emacs = %{version}-%{release}

Requires(post): xdg-utils
Requires(postun): xdg-utils
# M2-help
Requires: xdg-utils

%description
Macaulay 2 is a new software system devoted to supporting research in
algebraic geometry and commutative algebra written by Daniel R. Grayson
and Michael E. Stillman


%prep
%setup -q 

install -p -m755 %{SOURCE20} ./etags

%patch0 -p1 -b .optflags
%patch1 -p1 -b .xdg_open
%patch2 -p1 -b .cout
%patch3 -p1 -b .DESTDIR
%patch4 -p1 -b .gcc41
%patch201739 -p1 -b .bz201739

[ -f configure -a -f include/config.h ] || make 


%build

# We need /sbin:. in PATH to find install-info,etags
export PATH=/sbin:`pwd`:$PATH

%configure  \
  --disable-encap \
  --disable-dumpdata \
  --disable-optimize \
  --disable-static \
  --disable-strip \
  --with-lapacklibs="-llapack"

# Not smp-safe
make 


%check 
# util/screen dies on fc5/buildsystem (could not open pty)
#make -k check ||:


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# app img
install -p -m644 -D %{SOURCE10} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/Macaulay2.png

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --vendor="fedora" \
  %{SOURCE11}

# Make a new home for emacs files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/Macaulay2/emacs
mv $RPM_BUILD_ROOT%{emacs_sitelisp}/M2*.el $RPM_BUILD_ROOT%{_datadir}/Macaulay2/emacs/
 
for dir in %{emacs_sitelisp} %{xemacs_sitelisp} ; do
  install -d -m755 $RPM_BUILD_ROOT$dir
  pushd $RPM_BUILD_ROOT%{_datadir}/Macaulay2/emacs
  for file in M2*.el ; do
    ln -s %{_datadir}/Macaulay2/emacs/$file $RPM_BUILD_ROOT$dir
    touch $RPM_BUILD_ROOT$dir/`basename $file .el`.elc
  done
  popd
done


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%postun
%{_bindir}/xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%triggerin -- emacs-common
if [ -d %{emacs_sitelisp} ]; then 
  for file in %{_datadir}/Macaulay2/emacs/M2*.el ; do
    ln -sf $file %{emacs_sitelisp}/ ||:
  done
fi

%triggerin -- xemacs-common
if [ -d %{xemacs_sitelisp} ]; then
  for file in %{_datadir}/Macaulay2/emacs/M2*.el ; do
    ln -sf $file %{xemacs_sitelisp}/ ||:
  done
fi

%triggerun -- emacs-common
[ $2 -eq 0 ] && rm -f %{emacs_sitelisp}/M2*.el* || :

%triggerun -- xemacs-common
[ $2 -eq 0 ] && rm -f %{xemacs_sitelisp}/M2*.el* || :


%files
%defattr(-,root,root,-)
%doc Macaulay2/CHANGES Macaulay2/COPYING
%{_bindir}/*
%{_datadir}/Macaulay2/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
# FIXME
%{_docdir}/Macaulay2
%{_infodir}/*
%{_mandir}/man1/*
%ghost %{emacs_sitelisp} 
%ghost %{xemacs_sitelisp}


%changelog
* Mon Jan 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-4
- Ob/Pr: Macaulay2-doc, not -docs (#222609)

* Sat Jan 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-3
- re-enable ppc build (#201739)

* Tue Jan 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.95-2
- ./configure --disable-strip, for usable -debuginfo (#220893)

* Mon Dec 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.95-1
- Macaulay2-0.9.95

* Wed Nov 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.5.20060808svn
- .desktop Categories: -Application,Scientific,X-Fedora +ConsoleOnly

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.4.20060808svn
- fc6 respin

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.3.20060808svn
- ExcludeArch: ppc (bug #201739)
- %ghost (x)emacs site-lisp bits (using hints from fedora-rpmdevtools)

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.2.20060808svn
- 20060808 snapshot

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.20-0.1.20060724svn
- 2006-07-15-0.9.20

* Wed Jul 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.10-0.6.20060710svn
- 0.9.10

-* Mon Jul 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.6.cvs20060327
- BR: ncurses-devel

* Fri May 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.4.cvs20060327
- 64bit patch (#188709)

* Wed Apr 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.3.cvs20060327 
- omit x86_64, for now (#188709)

* Tue Apr 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.8-0.2.cvs20060327
- 0.9.8 (cvs, no tarball yet)
- drop -doc subpkg (in main now)

* Mon Apr 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-22
- fix icon location (#188384)

* Thu Mar 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-21
- really disable %%check (fails on fc5+ anyway) 

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-20
- .desktop: drop Category=Development
- app icon: follow icon spec
- drop -emacs subpkg (in main now) 

* Fri Sep 16 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-19
- disable 'make check' (fc5/buildsystem error), besides, we get a 
  good consistency check when M2 builds all the doc examples.

* Wed Sep 14 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-18
- rebuild against gc-6.6

* Thu May 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.2-17
- rebuild (build system x86_64 repository access failed for 0.9.2-16)
- fix build for GCC 4 (#156223)

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.2-15
- rebuilt

* Mon Feb 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.9.2-14
- x86_64 issues (%%_libdir -> %%_prefix/lib )
- remove desktop_file macro usage

* Sat Oct 23 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.13
- BR: time (again)
- omit m2_dir/setup (not needed/wanted)

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.12
- actually *apply* gcc34 patch this time.

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.11
- gcc34 patch

* Fri Oct 1 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.10
- explicit BR versions for gc-devel, libfac-devel, factory-devel

* Tue Aug 10 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.9
- BR: time

* Thu Jun 03 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.8
- .desktop: remove Terminaloptions to be desktop agnostic
- .desktop: Categories += Education;Math;Development (Devel only
  added so it shows *somewhere* in gnome menus)

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.7
- disable default 'make check' (util/screen fails on fc2)

* Tue Mar 30 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.6
- desktop-file is now on by default
- use separate (not inline) .desktop file

* Mon Jan 05 2004 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.5
- fix BuildRequires: desktop-file-utils to satisfy rpmlint.
- put emacs files in emacs subdir too (to follow supplied docs)
- *really* nuke .cvsignore files
- fix desktop-file-install --add-cateagories usage

* Tue Dec 23 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.4
- -emacs: use %%defattr
- -emacs: fix M2-init.el

* Mon Nov 17 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.3
- update/simplify macros
- desktop_file support.
- emacs subpkg.
- relax Req's on subpkgs to just: Requires: %%name = %%epoch:%%version
- use non-versioned BuildRequires
- remove redundant BuildRequires: gmp-devel
- remove gc patch, no longer needed.
- delete/not-package a bunch of unuseful files.
- use --disable-strip when debug_package is in use.

* Thu Nov 13 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.2
- no longer explictly Requires: emacs

* Wed Nov 05 2003 Rex Dieter <rexdieter at sf.net> 0:0.9.2-0.fdr.1
- missing Epoch: 0

* Fri Sep 12 2003 Rex Dieter <rexdieter at sf.net> 0.9.2-0.fdr.0
- fedora'ize

