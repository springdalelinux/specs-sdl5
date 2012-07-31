
## Conditional build:
%define _with_orrery --with-orrery
#define _with_maniview --with-maniview

%define beta rc9

Name:    geomview
Summary: Interactive 3D viewing program
Version: 1.8.2
Release: 0.25.%{beta}%{?dist}

License: LGPL
Url:     http://www.geomview.org/
Group:   Applications/Engineering
Source0: http://osdn.dl.sourceforge.net/sourceforge/geomview/geomview-%{version}-%{beta}.tar.bz2
#Source0: geomview-%{cvs}.tar.bz2
#Source1: geomview-cvs_checkout.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# http://bugzilla.redhat.com/bugzilla/182625
#ExcludeArch: x86_64

Source1: geomview.desktop
Source2: geomview.png

# Other plugins
%define orrery_ver 0.9.3
Source100: http://dl.sourceforge.net/geomview/orrery-%{orrery_ver}.tar.gz
%define maniview_ver 2.0.0
Source200: http://dl.sourceforge.net/geomview/maniview-%{maniview_ver}.tar.gz

## Patches
# put moduledir and data in sane locations
Patch1: geomview-1.8.2-fhs.patch
# orrery fhs fixes
Patch100: orrery-0.9.3-fhs.patch

BuildRequires: desktop-file-utils
BuildRequires: automake libtool
BuildRequires: byacc flex
# Until we have a generic BR: motif-devel -- Rex
#if "%{?fedora}" > "5"
#BuildRequires: lesstif-devel
#else
BuildRequires: openmotif-devel
#endif
BuildRequires: xforms-devel
BuildRequires: libGL-devel libGLU-devel
#if "%{?fedora}" > "4"
BuildRequires: libXmu-devel
#endif
BuildRequires: tcl-devel tk-devel


#BuildRequires: /usr/bin/makeinfo 
BuildRequires: texinfo

#BuildRequires: /usr/bin/texi2html
#if "%{?fedora}" > "3"
BuildRequires: texi2html
#else
#BuildRequires: tetex
#endif

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

Obsoletes: %{name}-plugins < %{version}-%{release}
Provides:  %{name}-plugins = %{version}-%{release}

Obsoletes: %{name}-orrery   < %{version}-%{release}
Obsoletes: %{name}-maniview < %{version}-%{release}

%if "%{?_with_orrery:1}" == "1"
Provides: %{name}-orrery   = %{version}-%{release}
Requires: tk tcl
%endif

%if "%{?_with_maniview:1}" == "1"
Provides: %{name}-maniview = %{version}-%{release}
%endif

%description
Geomview is an interactive 3D viewing program for Unix. It lets you view and
manipulate 3D objects: you use the mouse to rotate, translate, zoom in and out,
etc. It can be used as a standalone viewer for static objects or as a display
engine for other programs which produce dynamically changing geometry. It can
display objects described in a variety of file formats. It comes with a wide
selection of example objects, and you can create your own objects too.

%package devel
Summary: Development files for %{name} 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
%{summary}.

%if "%{?_with_orrery:1}" == "1"
%package orrery
Group:   Applications/Engineering
Summary: Solar System Simulator for Geomview
Requires: %{name} = %{version}
Requires: tk tcl
Obsoletes: orrery < %{orrery_ver}-%{release}
Provides:  orrery = %{orrery_ver}-%{release}
%description orrery
The Orrery is Geomview module which is a digital model of the solar
system, named for the mechanical models of the same name (often you'll
see one with just the Sun, Earth and Moon, as little balls supported
on wires); the first such was built for the fourth Earl of Orrery in
the 1700's.  This one includes all nine planets, some of their
satellites, and a few recent comets.
%endif

%if "%{?_with_maniview:1}" == "1"
%package maniview
Group:   Applications/Engineering
Summary: Geomview module for viewing 3D manifolds
Requires: %{name} = %{version}
Obsoletes: maniview < %{maniview_ver}-%{release}
Provides:  maniview = %{maniview_ver}-%{release}
%description maniview
%{summary}.
%endif


%prep
%define src_dir %{name}-%{version}%{?beta:-%{beta}}
%setup -q -n %{src_dir} 

# purge CVS crud 
find . -name CVS -type d | xargs rm -rf
find . -name .cvsignore | xargs rm -f

#patch1 -p1 -b .fhs

#libtoolize --force
#aclocal -I m4
#./reconf -n

%if "%{?_with_orrery:1}" == "1"
%setup -q -T -D -n %{src_dir}/src/bin -a 100
%patch100 -p0 -b .orrery-fhs
pushd orrery-%{orrery_ver}
libtoolize --force
aclocal -I ../../../m4
autoreconf -i -I ../../../m4
#autoheader
#automake -a
popd
%setup -T -D -n %{src_dir}
%endif

%if "%{?_with_maniview:1}" == "1"
%setup -q -T -D -n %{src_dir}/src/bin -a 200
pushd maniview-%{maniview_ver}
#libtoolize --force
#aclocal -I ../../../m4
#autoreconf -i -I ../../../m4
popd
%setup -T -D -n %{src_dir}
%endif


%build

export ACLOCAL=aclocal
export AUTOMAKE=automake

# --config-cache (for maniview)
%configure \
  --enable-shared \
  --disable-static

# Either do (re)automake steps above for addons, or this. -- Rex
%if 0
#--no-recursion
%{?_with_orrery:(cd src/bin/orrery-%{orrery_ver};%configure)}
%{?_with_maniview:(cd src/bin/maniview-%{maniview_ver};%configure --cache-file=../../../config.cache)}
%endif

# not smp-safe
#make MATHLIB=-lm 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# .desktop entry
desktop-file-install --vendor="fedora" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}

# app icon
install -D -m644 -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/geomview.png

# fixup info, We'll use install-info later
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# maniview manpage
%{?_with_maniview:install -D -m644 -p src/bin/maniview-%{maniview_ver}/maniview.1 $RPM_BUILD_ROOT%{_mandir}/man1/maniview.1}

# rename animate.1 that Conflicts: ImageMagick (#202039)
mv $RPM_BUILD_ROOT%{_mandir}/man1/animate.1 \
   $RPM_BUILD_ROOT%{_mandir}/man1/geomview-animate.1 ||:
# rename sweep.1 that Conflicts: lam (#212435)
mv $RPM_BUILD_ROOT%{_mandir}/man1/sweep.1 \
   $RPM_BUILD_ROOT%{_mandir}/man1/geomview-sweep.1 ||:

# rpmdocs
make -k -C doc docdir=`pwd`/rpmdocs          install-docDATA ||:
make -k -C doc dochtmldir=`pwd`/rpmdocs/html install-dochtmlDATA ||:
for dir in src/bin/orrery* src/bin/maniview* ; do
  for file in AUTHORS ChangeLog COPYING README TODO ; do
    test -s "$dir/$file" && install -p -m644 -D "$dir/$file" "rpmdocs/`basename $dir`/$file"
  done
done

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{src_dir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.gz ||:
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor > /dev/null 2>&1 ||:
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 ||:

%preun
if [ $1 -eq 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.gz ||:
fi

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor > /dev/null 2>&1 ||:
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 ||:


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%doc rpmdocs/geomview.pdf rpmdocs/html/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/geomview/
%{_libdir}/lib*.so.*
%{_libexecdir}/geomview/
%if "%{?_with_orrery:1}" == "1"
%doc rpmdocs/orrery*/AUTHORS rpmdocs/orrery*/ChangeLog rpmdocs/orrery*/COPYING 
%doc rpmdocs/orrery*/README
%endif

%if "%{?_with_maniview:1}" == "1"
%doc rpmdocs/maniview*/ChangeLog rpmdocs/maniview*/COPYING
%doc rpmdocs/maniview*/README
%endif

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/geomview/


%changelog
* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.25.rc9
- re-instate dfi --vendor=fedora (thanks Ville!) 

* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.24.rc9
- fixup desktop-file-install usage
- fixup geomview.desktop Categories

* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.22.rc9
- rename (man/man1/)sweep.1 -> geomview-sweep.1 to avoid
  Conflicts: lam (bug #212435)

* Sun Oct 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.21.rc9
- 1.8.2rc9

* Thu Sep 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.20.rc8
- fc6: BR: openmotif-devel -> lesstif-devel

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.19.rc8
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.18.rc8
- rename (man/man1/)animate.1 -> geomview-animate.1 to avoid 
  Conflicts: ImageMagick (bug #202039)

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.17.rc8
- 1.8.2-rc8
- -devel pkg

* Mon Jul 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.14.rc7
- BR: tcl-devel tk-devel

* Mon Jul 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.13.rc7
- 1.8.2-rc7

* Thu Jul 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.12.rc6
- 1.8.2-rc6

* Tue Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.11.rc4
- 1.8.2-rc4

* Fri Jul 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.10.rc3
- patch to fix ppc build

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.8.rc3
- 1.8.2-rc3
- --without-maniview (for now, doesn't build)
- drop -maniview, -orrery subpkgs

* Sat Jun 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.7.cvs20060623
- omit zero-length files

* Fri Jun 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.6.cvs20060623
- geomview-cvs20060623, (hopefully) will yield a usable, x86_64 build (#182625)
- --disable-seekpipe

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.5.cvs20040221
- BR: automake libtool

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.3.cvs20040221
- updated (transparent) icon (rh bug #190218)
- drop deprecated BR: libGL.so.1,libGLU.so.1 bits
- ExcludeArch: x86_64 (#182625)
- .desktop: MimeType: application/x-geomview

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Jan 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.2.cvs20040221
- rework Obsoletes/Provides: geomview-plugins

* Mon Jan 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.2-0.1.cvs20040221
- cvs20040421
- --with-xforms unconditional, Obsoletes/Provides: geomview-plugins

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]usres.sf.net> 1.8.1-12
- follow/use icon spec

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Sep 20 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-10
- update Source URL
- fix un-owned /usr/share/geomview/modules
- Requires(post,preun): /sbin-install-info
- -orrery: Requires: tk
- License: LGPL, %%doc COPYING
- comment out the Obsoleting of subpkgs with using --without.  I think
  the logic there is wrong.
- relax subpkgs to Requires: %{name} = %%epoch:%%version

* Tue Sep 14 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.9
- fix build for fc3
- remove unused gcc_ver cruft
- remove unused (by default) lesstif bits

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.8
- .desktop Categories += Education;Math;

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.7
- BR: libGL.so.1 libGLU.so.1

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.6
- fix file list (possible dups)

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.5
- BR: libtool flex
- BR: XFree86-devel (for lib{GL/GLU})

* Thu Jun 03 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.4
- .desktop: Categories += Graphics

* Tue Mar 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.3
- use patch from geomview sf site to allow gcc3.
- use desktop-file-install

* Wed Sep 24 2003 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.2
- cleanup for formal submission to fedora.

* Fri Aug 08 2003 Rex Dieter <rexdieter at sf.net> 0:1.8.1-0.fdr.1
- Build against openmotif.

* Mon May 12 2003 Rex Dieter <rexdieter at users.sf.net> 0:1.8.1-0.fdr.0
- fedora'ize
- rh73: link xforms static (for now, so rh80+ users could use if they
  want/need plugins/maniview subpkgs).
- rh80+: use g++296, no xforms.
- Obsoletes: subpkgs not built.

* Fri Jun 21 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-8
- Obsoletes/Provides: pluginname=version-release for extra plugins
  (so to gracefully handle upgrade from Mark's orrery rpm)

* Fri Jun 21 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-7
- use macros for all subpkgs
- include orrery-0.9.3.
- remove %_smp_mflags (makefile is not smp safe)

* Thu Jun 20 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-6
- include maniview-2.0.0.
- include geomview info/man pages.

* Thu Feb 27 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-5
- rebuild to link xforms dynamic

* Wed Feb 20 2002 Rex Dieter <rexdieter at users.sf.net> 1.8.1-4
- conditionally use xforms (no by default)
- make subpkg require %%name-%%version-%%release
- tweak to work with new lesstif

* Tue Dec 11 2001 Rex Dieter <rexdieter at users.sf.net> 1.8.1-3
- really use the app-icon this time.
- use Prefix to at least pretend relocatability

* Wed Nov 7 2001 Rex Dieter <rexdieter at users.sf.net> 1.8.1-2
- make -plugins subpkg for plugins that use xforms.

* Fri Oct 5 2001 Rex Dieter <rexdieter at users.sf.net > 1.8.1-1
- cleanup specfile
- make icon/desktop files
- include option to link xforms-static (untested)

* Fri Sep 28 2001 Rex Dieter <rexdieter at users.sf.net> 1.8.1-0
- first try.
- TODO: make subpkgs manual(html), modules, modules-xforms

