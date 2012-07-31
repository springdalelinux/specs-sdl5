# Fedora Review: http://bugzilla.redhat.com/188180

# -no-pch disables precompiled headers, make ccache-friendly
%global no_pch -no-pch

%global _default_patch_fuzz 3 

# enable kde-qt integration/patches (currently a no-op)
%global kde_qt 1

# See http://bugzilla.redhat.com/223663
%global multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9

Summary: Qt toolkit
Name:    qt46
Epoch:   1
Version: 4.6.2
Release: 20%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and ASL 2.0 and BSD and FLT and MIT
Group: System Environment/Libraries
Url: http://www.qtsoftware.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-%{version}.tar.gz

# default Qt config file
Source4: Trolltech.conf

# header file to workaround multilib issue
Source5: qconfig-multilib.h

# gstreamer logos
Source10: http://gstreamer.freedesktop.org/data/images/artwork/gstreamer-logo.svg
Source11: hi16-phonon-gstreamer.png
Source12: hi22-phonon-gstreamer.png
Source13: hi32-phonon-gstreamer.png
Source14: hi48-phonon-gstreamer.png
Source15: hi64-phonon-gstreamer.png
Source16: hi128-phonon-gstreamer.png

# desktop files
Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qtdemo.desktop
Source24: qtconfig.desktop

# upstream qt4-logo, http://trolltech.com/images/products/qt/qt4-logo
Source30: hi128-app-qt4-logo.png
Source31: hi48-app-qt4-logo.png

# set default QMAKE_CFLAGS_RELEASE
Patch2: qt-x11-opensource-src-4.2.2-multilib-optflags.patch

# font rendering issue in as_IN
Patch5: qt-all-opensource-src-4.4.0-rc1-as_IN-437440.patch

# hack around gcc/ppc crasher, http://bugzilla.redhat.com/492185
Patch13: qt-x11-opensource-src-4.5.0-gcc_hack.patch

# enable ft lcdfilter
Patch15: qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch

# include kde4 plugin path, http://bugzilla.redhat.com/498809
Patch16: qt-x11-opensource-src-4.5.1-kde4_plugins.patch

# make PulseAudio the default device in Phonon
Patch17: qt-x11-opensource-src-4.5.2-pulseaudio.patch
Patch19: qt-x11-opensource-src-4.5.1-phonon.patch
Patch21: qt-everywhere-opensource-src-4.6.0-gst-pulsaudio.patch

# use system ca-bundle certs, http://bugzilla.redhat.com/521911
Patch22: qt-x11-opensource-src-4.5.3-system_ca_certificates.patch 

## upstreamable bits
# http://bugzilla.redhat.com/485677
Patch51: qt-everywhere-opensource-src-4.6.0-beta1-qdoc3.patch 

# fix invalid inline assembly in qatomic_{i386,x86_64}.h (de)ref implementations
Patch53: qt-x11-opensource-src-4.5.0-fix-qatomic-inline-asm.patch

# fix invalid assumptions about mysql_config --libs
# http://bugzilla.redhat.com/440673
Patch54: qt-x11-opensource-src-4.5.1-mysql_config.patch

# http://bugs.kde.org/show_bug.cgi?id=180051#c22
Patch55: qt-everywhere-opensource-src-4.6.2-cups.patch

# fix s390x FTBFS
Patch56: qt-everywhere-opensource-src-4.6.2-webkit-s390x.patch

# bz#562049, bz#562060, bn-IN/kn-IN Incorrect rendering
Patch57: qt-4.6.3-bn-rendering-bz562049.patch

# bz#562058, bn_IN init feature is not applied properly
Patch58: qt-4.6.3-bn-rendering-bz562058.patch

# bz#631732, indic invalid syllable's are not recognized properly
Patch59: qt-4.6.3-indic-rendering-bz631732.patch

# bz#636399, oriya script open type features are not applied properly
Patch60: qt-4.6.3-indic-rendering-bz636399.patch

# bz562132, [ml_IN] Malayalam rakar is not getting reordered
Patch61: qt-everywhere-opensource-src-4.6-bz#562132.patch

# security patches
Patch100: qt-x11-opensource-src-4.5.3-cve-2010-0046-css-format-mem-corruption.patch
Patch101: qt-x11-opensource-src-4.5.3-cve-2010-0049-freed-line-boxes-ltr-rtl.patch
Patch102: qt-x11-opensource-src-4.5.3-cve-2010-0050-crash-misnested-style-tags.patch
Patch103: qt-x11-opensource-src-4.5.3-cve-2010-0052-destroyed-input-cached.patch
Patch104: qt-everywhere-opensource-src-4.6.2-cve-2010-0051-lax-css-parsing-cross-domain-theft.patch
Patch105: qt-everywhere-opensource-src-4.6.2-cve-2010-0054-image-element-pointer-name-getter.patch
Patch106: qt-everywhere-opensource-src-4.6.2-cve-2010-0656.patch
Patch107: qt-everywhere-opensource-src-4.6.2-cve-2010-0047.patch
Patch108: qt-everywhere-opensource-src-4.6.2-cve-2010-0648.patch
Patch109: qt-everywhere-opensource-src-4.6.2-cve-2011-3193-harfbuzz-buffer-overflow.patch
Patch110: qt-everywhere-opensource-src-4.6.2-cve-2011-3194-buffer-overflow-greyscale-images.patch

# kde-qt git patches
Patch201: 0001-This-patch-uses-object-name-as-a-fallback-for-window.patch
Patch202: 0002-This-patch-makes-override-redirect-windows-popup-men.patch
Patch203: 0003-This-patch-changes-QObjectPrivateVersion-thus-preven.patch
Patch204: 0004-This-patch-adds-support-for-using-isystem-to-allow-p.patch
Patch205: 0005-When-tabs-are-inserted-or-removed-in-a-QTabBar.patch
Patch206: 0006-Fix-configure.exe-to-do-an-out-of-source-build-on-wi.patch
Patch207: 0007-When-using-qmake-outside-qt-src-tree-it-sometimes-ge.patch
Patch208: 0008-This-patch-makes-the-raster-graphics-system-use-shar.patch
Patch209: 0009-Restore-a-section-of-the-file-that-got-removed-due-t.patch
Patch212: 0012-Add-context-to-tr-calls-in-QShortcut.patch
Patch213: qt-x11-opensource-src-4.6.2-tablet-wacom-QTBUG-8599.patch
Patch214: qt-everywhere-opensource-src-4.6.2-QTBUG-6932.patch
Patch215: qt-everywhere-opensource-src-4.6.2-atomic-s390.patch
Patch216: qt-everywhere-opensource-src-4.6.2-cups-QTBUG-6471.patch

# optional plugin bits
# set to -no-sql-<driver> to disable
# set to -qt-sql-<driver> to enable *in* qt library
%global mysql -plugin-sql-mysql
%global odbc -plugin-sql-odbc
#global psql -plugin-sql-psql
#global sqlite -plugin-sql-sqlite
%global sqlite -no-sql-sqlite
%global phonon -phonon
%global phonon_backend -phonon-backend
%global phonon_internal 1
%global phonon_backend_packaged 1
%global phonon_version 4.3.50
%global phonon_version_major 4.3
%global phonon_release 1
%global webkit -webkit
%global gtkstyle -gtkstyle
%global nas -no-nas-sound
%global dbus -dbus-linked
%global demos 1
%global docs 1
%global examples 1

# See http://bugzilla.redhat.com/196901
%global _qt4 %{name}
%global _qt4_prefix %{_libdir}/qt46
%global _qt4_bindir %{_qt4_prefix}/bin
%global _qt4_datadir %{_qt4_prefix}
%global _qt4_demosdir %{_qt4_prefix}/demos
%global _qt4_docdir %{_docdir}/qt46
%global _qt4_examplesdir %{_qt4_prefix}/examples
%global _qt4_headerdir %{_includedir} 
%global _qt4_libdir %{_libdir}
%global _qt4_plugindir %{_qt4_prefix}/plugins
%global _qt4_sysconfdir %{_sysconfdir}
%global _qt4_translationdir %{_datadir}/qt46/translations

BuildRequires: alsa-lib-devel
BuildRequires: dbus-devel >= 0.62
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig

## In theory, should be as simple as:
#define x_deps libGL-devel libGLU-devel
## but, "xorg-x11-devel: missing dep on libGL/libGLU" - http://bugzilla.redhat.com/211898 
%define x_deps libICE-devel libSM-devel libXcursor-devel libXext-devel libXfixes-devel libXft-devel libXi-devel libXinerama-devel libXrandr-devel libXrender-devel libXt-devel libX11-devel xorg-x11-proto-devel libGL-devel libGLU-devel
BuildRequires: %{x_deps}

%if "%{?nas}" != "-no-nas-sound"
BuildRequires: nas-devel
%endif

%if "%{?mysql}" != "-no-sql-mysql"
BuildRequires: mysql-devel >= 4.0
%endif

%if "%{?phonon_backend}" == "-phonon-backend"
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel 
%endif

%if "%{?gtkstyle}" == "-gtkstyle"
BuildRequires: gtk2-devel
%endif

%if "%{?psql}" != "-no-sql-psql"
BuildRequires: postgresql-devel
# added deps to workaround http://bugzilla.redhat.com/440673
BuildRequires: krb5-devel libxslt-devel openssl-devel pam-devel readline-devel zlib-devel
%endif

%if "%{?odbc}" != "-no-sql-odbc"
BuildRequires: unixODBC-devel
%endif

%if "%{?sqlite}" != "-no-sql-sqlite"
%define _system_sqlite -system-sqlite
BuildRequires: sqlite-devel
%endif

%{?_isa:Provides: qt4%{?_isa} = %{version}-%{release}}
Provides: qt46 = %{version}-%{release}
Provides: qgtkstyle = 0.1-1
Provides: qt46-config = %{version}-%{release}
Requires: openssl

%description 
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package -n phonon-backend-gstreamer
Summary: Gstreamer phonon backend
Group:   Applications/Multimedia
Requires: phonon%{?_isa} >= %{phonon_version_major} 
Provides: phonon-backend%{?_isa} = %{phonon_version}-%{phonon_release}
Provides:  %{name}-backend-gst = %{phonon_version}-%{phonon_release}

%description -n phonon-backend-gstreamer
%{summary}.

%package demos
Summary: Demonstration applications for %{name}
Group:   Documentation
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description demos
%{summary}.

%package doc
Summary: API documentation for %{name}
Group: Documentation
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-assistant
Provides:  qt46-doc = %{version}-%{release}
# help workaround yum bug http://bugzilla.redhat.com/502401

%description doc
%{summary}.  Includes:
Qt Assistant

%package devel
Summary: Development files for the Qt toolkit
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-x11%{?_isa}
Requires: %{x_deps}
Requires: libpng-devel
Requires: libjpeg-devel
Requires: pkgconfig
%if 0%{?phonon:1}
Provides: qt46-phonon-devel = %{version}-%{release}
%endif
%if 0%{?phonon_internal}
Provides:  phonon-devel = %{phonon_version}-%{phonon_release}
%endif
%if 0%{?webkit:1}
Provides:  WebKit-qt-devel = 1.0.0-1
%endif
Provides:  qt46-designer = %{version}-%{release}
# as long as libQtUiTools.a is included
Provides:  %{name}-static = %{version}-%{release}
Provides:  qt46-devel = %{version}-%{release}
%{?_isa:Provides: qt46-devel%{?_isa} = %{version}-%{release}}
Provides:  qt46-static = %{version}-%{release}
Provides: qt-assistant-adp-devel = %{version}-0.%{release}
%{?_isa:Provides: qt-assistant-adp-devel%{?_isa} = %{version}-0.%{release}}

%description devel
This package contains the files necessary to develop
applications using the Qt toolkit.  Includes:
Qt Linguist


%package examples
Summary: Programming examples for %{name}
Group: Documentation
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description examples
%{summary}.


%package mysql
Summary: MySQL driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt46-MySQL = %{version}-%{release}
Provides:  qt46-mysql = %{version}-%{release}
%{?_isa:Provides: qt46-mysql%{?_isa} = %{version}-%{release}}

%description mysql 
%{summary}.


%package odbc 
Summary: ODBC driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt46-ODBC = %{version}-%{release}
Provides:  qt46-odbc = %{version}-%{release}
%{?_isa:Provides: qt46-odbc%{?_isa} = %{version}-%{release}}

%description odbc 
%{summary}.


%package postgresql 
Summary: PostgreSQL driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt46-PostgreSQL = %{version}-%{release}
Provides:  qt46-postgresql = %{version}-%{release}
%{?_isa:Provides: qt46-postgresql%{?_isa} = %{version}-%{release}}

%description postgresql 
%{summary}.

%package sqlite
Summary: SQLite driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt46-SQLite = %{version}-%{release}
Provides:  qt46-sqlite = %{version}-%{release}
%{?_isa:Provides: qt46-sqlite%{?_isa} = %{version}-%{release}}

%description sqlite
%{summary}.

%package x11
Summary: Qt GUI-related libraries
Group: System Environment/Libraries
%if 0%{?phonon:1}
Requires:  phonon-backend%{?_isa} >= %{phonon_version_major} 
%endif
%if 0%{?phonon_internal}
Provides:  phonon = %{phonon_version}-%{phonon_release}
Provides:  phonon%{?_isa} = %{phonon_version}-%{phonon_release}
Provides:  qt46-phonon = %{version}-%{release}
%endif
%if 0%{?webkit:1}
Provides:  WebKit-qt = 1.0.0-1
%endif
Provides: qt46-assistant = %{version}-%{release}
Provides: %{name}-assistant = %{version}-%{release}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:  qt46-x11 = %{version}-%{release}
Provides: qt-assistant-adp = %{version}-0.%{release}
%{?_isa:Provides: qt-assistant-adp%{?_isa} = %{version}-0.%{release}}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description x11
Qt libraries used for drawing widgets and OpenGL items.

%prep
%setup -q -n qt-everywhere-opensource-src-%{version}

%patch2 -p1
%patch5 -p1 -b .bz#437440-as_IN-437440

%patch13 -p1 -b .gcc_hack
%patch15 -p1 -b .enable_ft_lcdfilter
%patch16 -p1 -b .kde4_plugins
%patch17 -p1 -b .phonon-pulseaudio
%patch19 -p1 -b .servicesfile
%patch21 -p1 -b .gst-pulsaudio
%patch22 -p1 -b .system_ca_certificates
%patch51 -p1 -b .qdoc3
%patch53 -p1 -b .qatomic-inline-asm
%patch54 -p1 -b .mysql_config
%patch55 -p1 -b .cups-1
%patch56 -p1 -b .s390x-FTBFS
%patch57 -p1 -b .bn-rendering-bz562049
%patch58 -p1 -b .bn-rendering-bz562058
%patch59 -p1 -b .indic-rendering-bz631732
%patch60 -p1 -b .indic-rendering-bz636399
%patch61 -p1 -b .ml_IN-rendering-bz#562132

# security fixes
%patch100 -p1 -b .cve-2010-0046-css-format-mem-corruption
%patch101 -p1 -b .cve-2010-0049-freed-line-boxes-ltr-rtl
%patch102 -p1 -b .cve-2010-0050-crash-misnested-style-tags
%patch103 -p1 -b .cve-2010-0052-destroyed-input-cached
%patch104 -p1 -b .cve-2010-0051-lax-css-parsing-cross-domain-theft
%patch105 -p1 -b .cve-2010-0054-image-element-pointer-name-getter
%patch106 -p1 -b .cve-2010-0656
%patch107 -p1 -b .cve-2010-0047
%patch108 -p1 -b .cve-2010-0648
%patch109 -p1 -b .cve-2011-3193-harfbuzz-buffer-overflow
%patch110 -p1 -b .cve-2011-3194-buffer-overflow-greyscale-images

# kde-qt branch
%patch201 -p1 -b .kde-qt-0001
%patch202 -p1 -b .kde-qt-0002
%patch203 -p1 -b .kde-qt-0003
%patch204 -p1 -b .kde-qt-0004
%patch205 -p1 -b .kde-qt-0005
%patch206 -p1 -b .kde-qt-0006
%patch207 -p1 -b .kde-qt-0007
%patch212 -p1 -b .kde-qt-0012
%patch213 -p1 -b .tablet-wacom-QTBUG-8599
%patch214 -p1 -b .QTBUG-6932
%patch215 -p1 -b .atomic-s390
%patch216 -p1 -b .cups-QTBUG-6471

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

# set default platform
# https://bugzilla.redhat.com/478481
%global platform linux-g++

# some 64bit platforms assume -64 suffix, https://bugzilla.redhat.com/569542
%if "%{?__isa_bits}"  == "64"
%global platform linux-g++-64                                                                      
%endif

# use the rpm opt flags
sed -i \
    -e "s|-O2|$RPM_OPT_FLAGS|g" \
    -e "s|g++.conf|g++-multilib.conf|g" mkspecs/%{platform}/qmake.conf

# disable QMAKE_CFLAGS_RELEASE
sed -e "s|^QMAKE_CFLAGS_RELEASE|#QMAKE_CFLAGS_RELEASE|g" \
  mkspecs/common/g++.conf > mkspecs/common/g++-multilib.conf
  
# unset QMAKE_LIBDIR_QT
sed -i -e "s|^QMAKE_LIBDIR_QT.*=.*|QMAKE_LIBDIR_QT       =|" mkspecs/common/linux.conf

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
sed -i -e "s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|" mkspecs/common/linux.conf 

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  sed -i -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  sed -i -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

%build

# build shared, threaded (default) libraries
./configure -v \
  -confirm-license \
  -opensource \
  -optimized-qmake \
  -prefix %{_qt4_prefix} \
  -bindir %{_qt4_bindir} \
  -datadir %{_qt4_datadir} \
  -demosdir %{_qt4_demosdir} \
  -docdir %{_qt4_docdir} \
  -examplesdir %{_qt4_examplesdir} \
  -headerdir %{_qt4_headerdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -sysconfdir %{_qt4_sysconfdir} \
  -translationdir %{_qt4_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -cups \
  -fontconfig \
  -largefile \
  -gtkstyle \
  -qt-gif \
  -no-rpath \
  -reduce-relocations \
  -no-separate-debug-info \
  %{?phonon} %{!?phonon:-no-phonon} \
  %{?phonon_backend} \
  %{?no_pch} \
  -no-javascript-jit \
  -sm \
  -stl \
  -system-libmng \
  -system-libpng \
  -system-libjpeg \
  -system-libtiff \
  -system-zlib \
  -xinput \
  -xcursor \
  -xfixes \
  -xinerama \
  -xshape \
  -xrandr \
  -xrender \
  -xkb \
  -glib \
  -openssl-linked \
  -xmlpatterns \
  %{?dbus} %{!?dbus:-no-dbus} \
  %{?webkit} %{!?webkit:-no-webkit } \
  %{?nas} \
  %{?mysql} \
  %{?psql} \
  %{?odbc} \
  %{?sqlite} %{?_system_sqlite} \
  %{!?docs:-nomake docs} \
  %{!?demos:-nomake demos} \
  %{!?examples:-nomake examples}

# create Makefile correctly
qtbuilddir=%{_builddir}/qt-everywhere-opensource-src-%{version}
for d in complexpingpong pingpong ; do
  pushd examples/dbus/$d
  $qtbuilddir/bin/qmake -spec $qtbuilddir/mkspecs/%{platform}/
  popd
done

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}

# Add desktop file(s)
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt4" \
  %{?docs:%{SOURCE20}} %{SOURCE21} %{SOURCE22} %{?demos:%{SOURCE23}} %{SOURCE24}

## pkg-config
# strip extraneous dirs/libraries 
# FIXME?: qt-4.5 seems to use Libs.private properly, so this hackery should 
#         no longer be required -- Rex
# safe ones
glib2_libs=$(pkg-config --libs glib-2.0 gobject-2.0 gthread-2.0)
ssl_libs=$(pkg-config --libs openssl)
for dep in \
  -laudio -ldbus-1 -lfreetype -lfontconfig ${glib2_libs} \
  -ljpeg -lm -lmng -lpng ${ssl_libs} -lsqlite3 -lz \
  -L/usr/X11R6/%{_lib} -L%{_libdir} ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la ||:
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done

# riskier
for dep in -lXrender -lXrandr -lXcursor -lXfixes -lXinerama -lXi -lXft -lXt -lXext -lX11 -lSM -lICE -ldl -lpthread ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la ||:
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc 
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done

# nuke dangling reference(s) to %buildroot
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" %{buildroot}%{_qt4_libdir}/*.prl
sed -i -e "s|-L%{_builddir}/qt-x11-opensource-src-%{version}/lib||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc

# nuke QMAKE_PRL_LIBS, seems similar to static linking and .la files (#520323)
sed -i -e "s|^QMAKE_PRL_LIBS|#QMAKE_PRL_LIBS|" %{buildroot}%{_qt4_libdir}/*.prl

# drop .la files
rm -f %{buildroot}%{_qt4_libdir}/lib*.la

# let rpm handle binaries conflicts
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt4_bindir}
for i in * ; do
  case "${i}" in
    assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
      mv $i ../../../bin/${i}-qt4
      ln -s ../../../bin/${i}-qt4 .
      ln -s ../../../bin/${i}-qt4 $i
      ;;
    *)
      mv $i ../../../bin/
      ln -s ../../../bin/$i .
      ;;
  esac
done
popd

# _debug targets (see bug #196513)
pushd %{buildroot}%{_qt4_libdir}
for lib in libQt*.so ; do
   libbase=`basename $lib .so | sed -e 's/^lib//'`
#  ln -s $lib lib${libbase}_debug.so
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.so 
done
for lib in libQt*.a ; do
   libbase=`basename $lib .a | sed -e 's/^lib//' `
#  ln -s $lib lib${libbase}_debug.a
   echo "INPUT(-l${libbase})" > lib${libbase}_debug.a
done
popd

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-%{_arch}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-multilib.h
  ln -sf qconfig-multilib.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig.h
  ln -sf ../QtCore/qconfig.h %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h
%endif

# Trolltech.conf
install -p -m644 -D %{SOURCE4} %{buildroot}%{_qt4_sysconfdir}/Trolltech.conf

# qt4-logo (generic) icons
install -p -m644 -D %{SOURCE30} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qt4-logo.png
install -p -m644 -D %{SOURCE31} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/qt4-logo.png

%if 0%{?docs}
  # assistant icons
  install -p -m644 -D tools/assistant/tools/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant.png
  install -p -m644 -D tools/assistant/tools/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant.png
%endif

# designer icons
install -p -m644 -D tools/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer.png

# linguist icons
for icon in tools/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist.png
done

# Qt.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt.pc<<EOF
prefix=%{_qt4_prefix}
bindir=%{_qt4_bindir}
datadir=%{_qt4_datadir}
demosdir=%{_qt4_demosdir}
docdir=%{_qt4_docdir}
examplesdir=%{_qt4_examplesdir}
headerdir=%{_qt4_headerdir}
libdir=%{_qt4_libdir}
plugindir=%{_qt4_plugindir}
qmake=%{_qt4_bindir}/qmake
sysconfdir=%{_qt4_sysconfdir}
translationdir=%{_qt4_translationdir}

Name: Qt
Description: Qt Configuration
Version: %{version}
EOF

# rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >%{buildroot}%{_sysconfdir}/rpm/macros.qt4<<EOF
%%_qt4 %{name}
%%_qt46 %{version}
%%_qt4_version %{version}
%%_qt4_prefix %%{_libdir}/qt4
%%_qt4_bindir %%{_qt4_prefix}/bin
%%_qt4_datadir %%{_qt4_prefix}
%%_qt4_demosdir %%{_qt4_prefix}/demos
%%_qt4_docdir %%{_docdir}/qt4
%%_qt4_examples %%{_qt4_prefix}/examples
%%_qt4_headerdir %%{_includedir}
%%_qt4_libdir %%{_libdir}
%%_qt4_plugindir %%{_qt4_prefix}/plugins
%%_qt4_qmake %%{_qt4_bindir}/qmake
%%_qt4_sysconfdir %%{_sysconfdir}
%%_qt4_translationdir %%{_datadir}/qt4/translations 
EOF

# create/own %%_qt4_plugindir/styles
mkdir %{buildroot}%{_qt4_plugindir}/styles

# create/own %%_qt4_plugindir/gui_platform
mkdir %{buildroot}%{_qt4_plugindir}/gui_platform

%if 0%{?phonon_internal}
  mkdir -p %{buildroot}%{_qt4_plugindir}/phonon_backend
  # workaround remove symlinks issue which breaks qt update
  mv %{buildroot}%{_qt4_headerdir}/phonon %{buildroot}%{_qt4_headerdir}/Phonon
  mkdir -p %{buildroot}%{_qt4_headerdir}/phonon
  mv %{buildroot}%{_qt4_headerdir}/Phonon/*.h %{buildroot}%{_qt4_headerdir}/phonon/
  rm -f %{buildroot}%{_qt4_headerdir}/Phonon/?honon
  mv %{buildroot}%{_qt4_headerdir}/Phonon %{buildroot}%{_qt4_headerdir}/phonon/
  sed -i -e  's| "| "../../phonon/|' %{buildroot}%{_qt4_headerdir}/phonon/Phonon/*
%else
  rm -fv  %{buildroot}%{_qt4_libdir}/libphonon.so*
  rm -rfv %{buildroot}%{_libdir}/pkgconfig/phonon.pc
  # contents slightly different between phonon-4.3.1 and qt-4.5.0
  rm -fv  %{buildroot}%{_includedir}/phonon/phononnamespace.h
  # contents dup'd but should remove just in case
  rm -fv  %{buildroot}%{_includedir}/phonon/*.h
  rm -rfv %{buildroot}%{_qt4_headerdir}/phonon*
  rm -fv %{buildroot}%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%endif

%if 0%{?phonon_backend_packaged}
  install -D -m 0644 %{SOURCE10} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/phonon-gstreamer.svg
  install -D -m 0644 %{SOURCE11} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/phonon-gstreamer.png
  install -D -m 0644 %{SOURCE12} %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/phonon-gstreamer.png
  install -D -m 0644 %{SOURCE13} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/phonon-gstreamer.png
  install -D -m 0644 %{SOURCE14} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/phonon-gstreamer.png
  install -D -m 0644 %{SOURCE15} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/phonon-gstreamer.png
  install -D -m 0644 %{SOURCE16} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/phonon-gstreamer.png
%else
  rm -fv %{buildroot}%{_qt4_plugindir}/phonon_backend/*_gstreamer.so
  rm -fv %{buildroot}%{_datadir}/kde4/services/phononbackends/gstreamer.desktop
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans devel
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun devel
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%post x11
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans x11
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun x11
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%if 0%{?phonon_backend_packaged}
%post -n phonon-backend-gstreamer
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans -n phonon-backend-gstreamer
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%postun -n phonon-backend-gstreamer
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
fi

%files -n phonon-backend-gstreamer
%defattr(-,root,root,-)
%{_qt4_plugindir}/phonon_backend/*_gstreamer.so
%{_datadir}/kde4/services/phononbackends/gstreamer.desktop
%{_datadir}/icons/hicolor/*/apps/phonon-gstreamer.*
%endif

%files
%defattr(-,root,root,-)
%doc README LGPL_EXCEPTION.txt LICENSE.LGPL LICENSE.GPL3
%dir %{_qt4_prefix}
%dir %{_qt4_bindir}
%dir %{_datadir}/qt46
%if 0%{?docs}
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/qch/
%endif
%config(noreplace) %{_qt4_sysconfdir}/Trolltech.conf
%{_qt4_datadir}/phrasebooks/
%{_qt4_libdir}/libQtCore.so.4*
%if 0%{?dbus:1}
%{_bindir}/qdbus
%{_qt4_bindir}/qdbus
%{_qt4_libdir}/libQtDBus.so.4*
%endif
%{_qt4_libdir}/libQtNetwork.so.4*
%{_qt4_libdir}/libQtScript.so.4*
%{_qt4_libdir}/libQtSql.so.4*
%{_qt4_libdir}/libQtTest.so.4*
%{_qt4_libdir}/libQtXml.so.4*
%{_qt4_libdir}/libQtXmlPatterns.so.4*
%dir %{_qt4_plugindir}
%dir %{_qt4_plugindir}/sqldrivers/
%{_qt4_translationdir}/

%if 0%{?demos}
%files demos
%defattr(-,root,root,-)
%{_qt4_bindir}/qt*demo*
%{_bindir}/qt*demo*
%{_datadir}/applications/*qtdemo.desktop
%{_qt4_demosdir}/
%endif

%files devel
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.*
%{_qt4_bindir}/lconvert
%{_qt4_bindir}/lrelease*
%{_qt4_bindir}/lupdate*
%{_qt4_bindir}/moc*
%{_qt4_bindir}/pixeltool*
%{_qt4_bindir}/qdoc3*
%{_qt4_bindir}/qmake*
%{_qt4_bindir}/qt3to4
%{_qt4_bindir}/qttracereplay
%{_qt4_bindir}/rcc*
%{_qt4_bindir}/uic*
%{_qt4_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_qt4_bindir}/qdbuscpp2xml
%{_qt4_bindir}/qdbusxml2cpp
%endif
%{_qt4_bindir}/qhelpconverter
%{_qt4_bindir}/qhelpgenerator
%{_qt4_bindir}/xmlpatterns
%{_qt4_bindir}/xmlpatternsvalidator
%{_bindir}/lconvert
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/pixeltool*
%{_bindir}/moc*
%{_bindir}/qdoc3
%{_bindir}/qmake*
%{_bindir}/qt3to4
%{_bindir}/qttracereplay
%{_bindir}/rcc*
%{_bindir}/uic*
%{_bindir}/designer*
%{_bindir}/linguist*
%{_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_bindir}/qdbuscpp2xml
%{_bindir}/qdbusxml2cpp
%endif
%{_bindir}/qhelpconverter
%{_bindir}/qhelpgenerator
%{_bindir}/xmlpatterns
%{_bindir}/xmlpatternsvalidator
%if 0%{?phonon:1}
%{_qt4_libdir}/libphonon.prl
%endif
%if 0%{?phonon_internal}
%{_qt4_libdir}/libphonon.so
%endif
%{_qt4_libdir}/libQt*.so
%{_qt4_libdir}/libQtUiTools*.a
%{_qt4_libdir}/libQt*.prl
# Qt designer
%{_qt4_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*
%{?docs:%{_qt4_docdir}/qch/designer.qch}
# Qt Linguist
%{_qt4_bindir}/linguist*
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*
%{?docs:%{_qt4_docdir}/qch/linguist.qch}
%defattr(644,root,root,755)
%{_qt4_headerdir}/*
%{_qt4_datadir}/mkspecs/
%{_libdir}/pkgconfig/*.pc
%{_qt4_datadir}/q3porting.xml


%if 0%{?docs}
%files doc
%defattr(644,root,root,755)
%{_qt4_docdir}/html
%{_qt4_docdir}/qch/*.qch
%exclude %{_qt4_docdir}/qch/designer.qch
%exclude %{_qt4_docdir}/qch/linguist.qch
%{_qt4_docdir}/src/
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*
%endif

%if 0%{?examples}
%files examples
%defattr(-,root,root,755)
%{_qt4_examplesdir}/
%endif

%if "%{?mysql}" == "-plugin-sql-mysql"
%files mysql
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlmysql*
%endif

%if "%{?odbc}" == "-plugin-sql-odbc"
%files odbc 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlodbc*
%endif

%if "%{?psql}" == "-plugin-sql-psql"
%files postgresql 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlpsql*
%endif

%if "%{?sqlite}" == "-plugin-sql-sqlite"
%files sqlite
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlite*
%endif

%files x11 
%defattr(-,root,root,-)
%if 0%{?phonon_internal}
%{_qt4_libdir}/libphonon.so.4*
%dir %{_datadir}/kde4/services/phononbackends/
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%endif
%{_qt4_libdir}/libQt3Support.so.4*
%{_qt4_libdir}/libQtAssistantClient.so.4*
%{_qt4_libdir}/libQtCLucene.so.4*
%{_qt4_libdir}/libQtDesigner.so.4*
%{_qt4_libdir}/libQtDesignerComponents.so.4*
%{_qt4_libdir}/libQtGui.so.4*
%{_qt4_libdir}/libQtHelp.so.4*
%{_qt4_libdir}/libQtMultimedia.so.4*
%{_qt4_libdir}/libQtOpenGL.so.4*
%{_qt4_libdir}/libQtScriptTools.so.4*
%{_qt4_libdir}/libQtSvg.so.4*
%{?webkit:%{_qt4_libdir}/libQtWebKit.so.4*}
%{_qt4_plugindir}/*
%exclude %{_qt4_plugindir}/sqldrivers
%if 0%{?phonon_backend_packaged}
%exclude %{_qt4_plugindir}/phonon_backend/*_gstreamer.so
%endif
%{_bindir}/assistant*
%{?dbus:%{_bindir}/qdbusviewer}
%{_bindir}/qt*config*
%{_qt4_bindir}/assistant*
%{?dbus:%{_qt4_bindir}/qdbusviewer}
%{_qt4_bindir}/qt*config*
%{_datadir}/applications/*qtconfig.desktop
%{_datadir}/icons/hicolor/*/apps/qt4-logo.*


%changelog
* Tue Sep 13 2011 Jaroslav Reznik <jreznik@redhat.com> - 1:4.6.2-20
- Resolves: #rhbz737813
   fix multiple flaws in Qt
   CVE-2011-3193, CVE-2011-3194

* Wed Jul 13 2011 Than Ngo <than@redhat.com> - 1:4.6.2-19
- Resolves: rhbz#679759, missing executable bit in qt-examples binaries
- Resolves: rhbz#716694, move macros.qt4 to -devel
- Resolves: rhbz#680088, rpmdiff failure

* Mon Jul 11 2011 Than Ngo <than@redhat.com> - 1:4.6.2-18
- Resolves: rhbz#562132, Malayalam rakar is not getting reordered 

* Wed Jan 26 2011 Than Ngo <than@redhat.com> - 1:4.6.2-17
- Resolves: rhbz#562049, rhbz#562060, rhbz#562058, rhbz#631732, rhbz#636399

* Tue Jun 01 2010 Than Ngo <than@redhat.com> - 4.6.2-16
- Resolves: bz#597271, drop WebKit support in Qt

* Thu May 06 2010 Than Ngo <than@redhat.com> - 4.6.2-15
- Resolves: bz#589165
   fix multiple flaws in webkit
   CVE-2010-0047, CVE-2010-0648, CVE-2010-0656

* Sat May 01 2010 Than Ngo <than@redhat.com> - 4.6.2-14
- fix issue in duplex printing

* Fri Apr 16 2010 Than Ngo <than@redhat.com> - 4.6.2-13
- backport frpm 4.6 branch to get the printDialog to check
  for default paperSize via CUPS

* Mon Mar 29 2010 Than Ngo <than@redhat.com> - 4.6.2-12
- backport from 4.6 branch to fix s390(x) atomic ops crashes

* Sun Mar 28 2010 Than Ngo <than@redhat.com> - 4.6.2-11
- fix a crash in thread on s390(x)

* Wed Mar 24 2010 Than Ngo <than@redhat.com> 4.6.2-10
- fix remove symlinks issue which breaks qt update

* Wed Mar 24 2010 Than Ngo <than@redhat.com> - 4.6.2-9
- Resolves: bz#575248, rebase to 4.6.2
- fix build issue in webkit on s390x
- fix a crash when reparenting an item in QGraphicsView, QTBUG-6932

* Wed Mar 17 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.6.2-8
- WebKit security update:
  CVE-2010-0046, CVE-2010-0049, CVE-2010-0050, CVE-2010-0051,
  CVE-2010-0052, CVE-2010-0054

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-7
- BR alsa-lib-devel (for QtMultimedia)

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-6
- Provides: qt-assistant-adp(-devel)

* Fri Mar 05 2010 Than Ngo <than@redhat.com> - 4.6.2-5
- Make tablet detection work with new wacom drivers (#569132)

* Mon Mar 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-4
- fix 64bit platform logic, use linux-g++-64 everywhere except x86_64 (#569542)

* Sun Feb 28 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.2-3
- fix CUPS patch not to crash if currentPPD is NULL (#566304)

* Tue Feb 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-2
- macros.qt4: s/qt45/qt46/

* Mon Feb 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.2-1
- 4.6.2

* Fri Feb 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-3
- improve cups support (#523846, kde#180051#c22)

* Tue Jan 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.1-2
- drop bitmap_font_speed patch, rejected upstream

* Tue Jan 19 2010 Than Ngo <than@redhat.com> - 4.6.1-1
- 4.6.1

* Mon Jan 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-5
- bitmap_font_speed patch (QTBUG-7255)

* Sat Jan 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-4
- Fix crash when QGraphicsItem destructor deletes other QGraphicsItem (kde-qt cec34b01)
- Fix a crash in KDE/Plasma with QGraphicsView. TopLevel list of items (kde-qt 63839f0c)

* Wed Dec 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-3
- disable QtWebKit JavaScript JIT again, incompatible with SELinux (#549994)

* Sat Dec 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-2
- own %%{_qt4_plugindir}/gui_platform

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.6.0-1
- 4.6.0

* Tue Nov 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.6.rc1
- qt-4.6.0-rc1

* Sat Nov 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.5.beta1 
- -tds: Add package with TDS sqldriver (#537586)
- add arch'd provides for sql drivers

* Sun Nov 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.4.beta1
- -x11: Requires: %%{name}-sqlite%{?_isa}

* Mon Oct 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.3.beta1
- kde-qt patches (as of 20091026)

* Fri Oct 16 2009 Than Ngo <than@redhat.com> - 4.6.0-0.2.beta1 
- subpackage sqlite plugin, add Require on qt-sqlite in qt-x11
  for assistant
- build/install qdoc3 again

* Wed Oct 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-0.1.beta1
- qt-4.6.0-beta1
- no kde-qt patches (yet)

* Sat Oct 10 2009 Than Ngo <than@redhat.com> - 4.5.3-4
- fix translation build issue
- rhel cleanup

* Tue Oct 06 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.5.3-3
- disable JavaScriptCore JIT, SE Linux crashes (#527079)

* Fri Oct 02 2009 Than Ngo <than@redhat.com> - 4.5.3-2
- cleanup patches
- if ! phonon_internal, exclude more/all phonon headers
- qt-devel must Requires: phonon-devel (#520323)

* Thu Oct 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.3-1
- qt-4.5.3

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-21
- switch to external/kde phonon

* Mon Sep 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-20
- use internal Qt Assistant/Designer icons
- -devel: move designer.qch,linguist.qch here
- move ownership of %%_qt4_docdir, %%_qt4_docdir/qch to main pkg

* Sun Sep 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-19
- Missing Qt Designer icon (#476605)

* Fri Sep 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-18
- drop gcc -fno-var-tracking-assignments hack (#522576)

* Fri Sep 11 2009 Than Ngo <than@redhat.com> - 4.5.2-17
- drop useless check for ossl patch, the patch works fine with old ossl

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 4.5.2-16
- add a correct system_ca_certificates patch

* Tue Sep 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-15
- use system ca-certificates (#521911)

* Tue Sep 01 2009 Than Ngo <than@redhat.com> - 4.5.2-14
- drop fedora < 9 support
- only apply ossl patch for fedora > 11

* Mon Aug 31 2009 Than Ngo <than@redhat.com> - 4.5.2-13
- fix for CVE-2009-2700

* Thu Aug 27 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-12
- use platform linux-g++ everywhere (ie, drop linux-g++-64 on 64 bit),
  avoids plugin/linker weirdness (bug #478481)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1:4.5.2-11
- rebuilt with new openssl

* Thu Aug 20 2009 Than Ngo <than@redhat.com> - 4.5.2-10
- switch to kde-qt branch

* Tue Aug 18 2009 Than Ngo <than@redhat.com> - 4.5.2-9
- security fix for CVE-2009-1725 (bz#513813)

* Sun Aug 16 2009 Than Ngo <than@redhat.com> - 4.5.2-8
- fix phonon-backend-gstreamer for using pulsaudio (#513421)

* Sat Aug 14 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-7
- kde-qt: 287-qmenu-respect-minwidth
- kde-qt: 0288-more-x-keycodes (#475247)

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-6
- use linker scripts for _debug targets (#510246)
- tighten deps using %%{?_isa}
- -x11: Requires(post,postun): /sbin/ldconfig

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.5.2-5
- apply upstream patch to fix issue in Copy and paste

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Than Ngo <than@redhat.com> - 4.5.2-3
- pregenerate PNG, drop BR on GraphicsMagick (bz#509244)

* Fri Jun 26 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.2-2
- take current qt-copy-patches snapshot (20090626)
- disable patches which are already in 4.5.2
- fix the qt-copy patch 0274-shm-native-image-fix.diff to apply against 4.5.2

* Thu Jun 25 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.5.2-1
- Qt 4.5.2

* Sun Jun 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-18
- phonon-backend-gstreamer pkg, with icons
- optimize (icon-mostly) scriptlets

* Sun Jun 07 2009 Than Ngo <than@redhat.com> - 4.5.1-17
- drop the hack, apply patch to install Global header, gstreamer.desktop
  and dbus services file

* Sat Jun 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-16
- install awol Phonon/Global header

* Fri Jun 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.1-15
- apply Phonon PulseAudio patch (needed for the xine-lib backend)

* Fri Jun 05 2009 Than Ngo <than@redhat.com> - 4.5.1-14
- enable phonon and gstreamer-backend

* Sat May 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-13
- -doc: Obsoletes: qt-doc < 1:4.5.1-4 (workaround bug #502401)

* Sat May 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-12
- +phonon_internal macro to toggle packaging of qt's phonon (default off)

* Fri May 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-11
- qt-copy-patches-20090522

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10.2
- full (non-bootstrap) build

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10.1
- allow for minimal bootstrap build (*cough* arm *cough*)

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-10
- improved kde4_plugins patch, skip expensive/unneeded canonicalPath

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-9
- include kde4 plugin path by default (#498809)

* Mon May 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-8
- fix invalid assumptions about mysql_config --libs (bug #440673)
- fix %%files breakage from 4.5.1-5

* Wed Apr 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-7
- -devel: Provides: qt4-devel%%{?_isa} ...

* Mon Apr 27 2009 Than Ngo <than@redhat.com> - 4.5.1-6
- drop useless hunk of qt-x11-opensource-src-4.5.1-enable_ft_lcdfilter.patch

* Mon Apr 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-5
- -devel: Provides: *-static for libQtUiTools.a

* Fri Apr 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-4
- qt-doc noarch
- qt-demos, qt-examples (split from -doc)
- (cosmetic) re-order subpkgs in alphabetical order
- drop unused profile.d bits

* Fri Apr 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-3
- enable FT_LCD_FILTER (uses freetype subpixel filters if available at runtime)

* Fri Apr 24 2009 Than Ngo <than@redhat.com> - 4.5.1-2
- apply upstream patch to fix the svg rendering regression

* Thu Apr 23 2009 Than Ngo <than@redhat.com> - 4.5.1-1
- 4.5.1

* Tue Apr 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-14
- fix vrgb/vgbr corruption, disable QT_USE_FREETYPE_LCDFILTER (#490377)

* Fri Apr 10 2009 Than Ngo <than@redhat.com> - 4.5.0-13
- unneeded executable permissions for profile.d scripts

* Wed Apr 01 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.0-12
- fix inline asm in qatomic (de)ref (i386/x86_64), should fix Kolourpaint crash

* Mon Mar 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-11
- qt fails to build on ia64 (#492174)

* Fri Mar 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-10
- qt-copy-patches-20090325

* Tue Mar 24 2009 Than Ngo <than@redhat.com> - 4.5.0-9
- lrelease only shows warning when duplicate messages found in *.ts( #491514)

* Fri Mar 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-8
- qt-copy-patches-20090319

* Thu Mar 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-7
- include more phonon bits, attempt to fix/provide phonon bindings
  for qtscriptgenerator, PyQt, ...

* Tue Mar 17 2009 Than Ngo <than@redhat.com> - 4.5.0-6
- fix lupdate segfault (#486866)

* Sat Mar 14 2009 Dennis Gilmore <dennis@ausil.us> - 4.5.0-5
- add patch for sparc64. 
- _Atomic_word is not always an int

* Tue Mar 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-4
- macros.qt4: %%_qt45
- cleanup more phonon-related left-overs 

* Wed Mar 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-3
- -no-phonon-backend
- include qdoc3
- move designer plugins to runtime (#487622)

* Tue Mar 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-2
- License: LGPLv2 with exceptions or GPLv3 with exceptions
- BR: gstreamer-devel
- drop qgtkstyle patch (no longer needed)
- -x11: move libQtScriptTools here (linked with libQtGui)

* Tue Mar 03 2009 Than Ngo <than@redhat.com> - 4.5.0-1
- 4.5.0

* Fri Feb 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:4.5.0-0.8.20090224
- 20090224 snapshot
- adjust pkgconfig hackery

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.0-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.5.rc1
- revert license, change won't land until official 4.5.0 release
- workaround broken qhostaddress.h (#485677)
- Provides: qgtkstyle = 0.1

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.4.rc1
- saner versioned Obsoletes
- -gtkstyle, Obsoletes: qgtkstyle < 0.1
- enable phonon support and associated hackery

* Mon Feb 16 2009 Than Ngo <than@redhat.com> 4.5.0-0.3.rc1
- fix callgrindChildExitCode is uninitialzed

* Sun Feb 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-0.2.rc1
- qt-copy-patches-20090215
- License: +LGPLv2

* Wed Feb 11 2009 Than Ngo <than@redhat.com> - 4.5.0-0.rc1.0
- 4.5.0 rc1

* Thu Feb 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-16
- track branches/qt-copy/4.4, and backout previous trunk(qt45) ones

* Mon Feb 02 2009 Than Ngo <than@redhat.com> 4.4.3-15
- disable 0269,0270,0271 patches, it causes issue in systray

* Thu Jan 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-14
- qt-copy-patches-20090129

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-13
- Provides: qt4%%{?_isa} = %%version-%%release
- add %%_qt4 to macros.qt4

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-12 
- respin (mysql)

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.4.3-11
- rebuild for new OpenSSL

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-10
- drop qt-x11-opensource-src-4.3.4-no-hardcoded-font-aliases.patch (#447298),
  in favor of qt-copy's 0263-fix-fontconfig-handling.diff

* Mon Jan 12 2009 Than Ngo <than@redhat.com> - 4.4.3-9
- qt-copy-patches-20090112

* Tue Dec 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-8
- qt-copy-patches-20081225

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-7
- rebuild for pkgconfig deps

* Wed Nov 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-6
- qt-copy-patches-20081112

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 4.4.3-5
- drop 0256-fix-recursive-backingstore-sync-crash.diff, it's
  included in qt-copy-pathes-20081110

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-4
- qt-copy-patches-20081110

* Mon Nov 10 2008 Than Ngo <than@redhat.com> 4.4.3-3
- apply 0256-fix-recursive-backingstore-sync-crash.diff

* Thu Nov 06 2008 Than Ngo <than@redhat.com> 4.4.3-2
- bz#468814, immodule selection behavior is unpredictable without QT_IM_MODULE,
  patch from Peng Wu
- backport fix from 4.5

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-1
- 4.4.3

* Wed Sep 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.2-2
- omit systray patch (for now)

* Sat Sep 20 2008 Than Ngo <than@redhat.com> 4.4.2-1
- 4.4.2

* Mon Sep 08 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-3
- apply QMAKEPATH portion of multilib patch only if needed
- qt-copy-patches-20080908

* Wed Aug 06 2008 Than Ngo <than@redhat.com> -  4.4.1-2
- fix license tag
- fix Obsoletes: qt-sqlite (missing epoch)

* Tue Aug 05 2008 Than Ngo <than@redhat.com> -  4.4.1-1
- 4.4.1

* Tue Aug 05 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-17
- fold -sqlite subpkg into main (#454930)

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-16
- qt-copy-patches-20080723 (kde#162793)
- omit deprecated phonon bits

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-15
- fix/workaround spec syntax 

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-14
- macros.qt4: fix %%_qt4_datadir, %%_qt4_translationdir

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-13
- (re)fix qconfig-multilib.h for sparc64

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-12
- qt-copy-patches-20080711

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-11
- fix dbus conditional (#452487)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-10
- strip -lsqlite3 from .pc files (#451490)

* Sat Jun 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-9
- restore -qt4 suffixes

* Fri Jun 13 2008 Than Ngo <than@redhat.com> 4.4.0-8
- drop qt wrapper, make symlinks to /usr/bin

* Tue Jun 10 2008 Than Ngo <than@redhat.com> 4.4.0-7
- fix #450310, multilib issue 

* Fri Jun 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-6
- qt-copy-patches-20080606
- drop BR: libungif-devel (not used)
- move libQtXmlPatters, -x11 -> main
- move qdbuscpp2xml, qdbusxml2cpp, xmlpatters, -x11 -> -devel

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-5
- under GNOME, default to QGtkStyle if available

* Mon May 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-4
- don't hardcode incorrect font substitutions (#447298)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-3
- qt-copy-patches-20080516

* Tue May 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-2
- revert _qt4_bindir change for now, needs more work (#446167)

* Tue May 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-1
- qt-4.4.0

* Tue Apr 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.6.rc1
- -webkit (include in -x11 subpkg), drop separate -webkit-devel
- omit qt4-wrapper.sh deps (since it's not used atm)
- qt-copy-patches-20080429
- Obsoletes/Provides: WebKit-qt(-devel) <|= 1.0.0-1  (#442200)

* Thu Apr 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.5.rc1
- strip -lssl -lcrypto from *.pc files too

* Tue Apr 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-0.4.rc1
- updated patch for #437440 ([as-IN] Consonant combination issue) by Pravin Satpute
- port the patch to Qt 4.4 (the code moved to harfbuzz) and reenable it

* Fri Apr 04 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.3.rc1
- qt-4.4.0-rc1
- -xmlpatterns (and drop -no-exceptions)
- -reduce-relocations, -dbus-linked, -openssl-linked
- -no-nas
- -no-phonon (-no-gstreamer), -no-webkit (for now, at least until
  conflicts with WebKit-qt and kdelibs4 are sorted out)
- %%_qt4_bindir -> %%_bindir, avoid qt4-wrapper hackage (#277581, #422291)
- qtconfig.desktop: NoDisplay=true (#244879)

* Wed Apr 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-10
- look for OpenSSL using versioned sonames (#432271)

* Wed Mar 26 2008 Than Ngo <than@redhat.com> 4.3.4-9
- apply patch bz#437440 to fix [as-IN] Consonant combination issue, thanks to Pravin Satpute

* Sun Mar 23 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-8
- -x11: add missing Provides: qt4-assistant when building as qt

* Thu Mar 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-7
- fix Requires of main package to include Epoch (thanks to Christopher Aillon)

* Wed Mar 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-6
- rename to qt on Fedora >= 9

* Mon Mar 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.4-5
- -x11: move qdbusviewer here

* Wed Mar 05 2008 Than Ngo <than@redhat.com> 4.3.4-4
- upstream patch to fix 4.3 regression

* Fri Feb 29 2008 Than Ngo <than@redhat.com> 4.3.4-3
- respin aliasing.patch, it's safer

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.3.4-2
- fix aliasing violations that caused qmake crash

* Fri Feb 22 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.4-1
- qt-4.3.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.3.3-9
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-8
- qt-copy patches 20080219
- drop -optimized-qmake, for now, to avoid qmake segfaults (gcc43 issue?) 

* Fri Feb 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-7
- %%qt_datadir: %%_datadir/qt4 -> %%_libdir/qt4

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-6
- qt-copy 20080130 patch set (helps address previous 0180-window-role BIC)
- Trolltech.conf: (default) fontsize=10
- License: GPLv2 with exceptions or QPL

* Thu Jan 24 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-5
- License: GPLv2 or QPL
- qt-copy patches

* Thu Jan 17 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-4
- Qt.pc: fix typo for demosdir (use %%_qt4_demosdir)

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 4.3.3-3
- apply patch from Dirk Müller to fix strict aliasing violations in tool classes

* Fri Dec 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-2
- -doc: Requires: %%name-assistant, omit assistant bin, 
  -x11: Provides: %%name-assistant (#147948)

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-1
- qt-4.3.3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-7
- move assistant to -x11, leave .desktop in -doc (#147948)

* Sun Dec 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-6
- move qdbus to main pkg (#407861)

* Mon Oct 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-5
- -optimized-qmake

* Fri Oct 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-4
- slowdown with 4.3.2 (#334281)

* Tue Oct 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-2
- create/own %%_qt4_plugindir/styles

* Thu Oct 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-1
- qt-4.3.2
- (re)fix ppc64 segfaults, ppc64 fix upstreamed (previous patch was 
  inadvertantly not applied) (#246324)

* Fri Sep 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-8
- -x11: Req: redhat-rpm-config rpm, app-wrapper/multilib fun (#277581)

* Thu Sep 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-7
- include qt4-logo icon, used by qtdemo/qtconfig (#241452)
- linguist.desktop: use new linguist4 icons
- -devel,-x11: %%post/%%postun scriptlets (icons, mimetypes)

* Thu Sep 13 2007 Than Ngo <than@redhat.com> -  4.3.1-4
- fixed bz241452, add qtdemo/qtconfig icons
- fixed bz249242, designer4 - segmentation fault on s390x

* Wed Aug 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-3
- ppc64 patch (#246324)

* Fri Aug 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-2
- License: GPLv2 (see also GPL_EXCEPTIONS*.txt)
- omit needless %%check
- (re)add package review comment/reference

* Thu Aug 09 2007 Than Ngo <than@redhat.com> -  4.3.1-1
- update to 4.3.1

* Wed Aug 08 2007 Than Ngo <than@redhat.com> 4.3.0-11
- add %%_qt4_version

* Tue Aug 07 2007 Than Ngo <than@redhat.com> 4.3.0-10
- cleanup

* Sun Jul 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-9
- multilib broken: qconfig.h (#248768)
- +%%_qt4_demosdir,%%_qt4_examplesdir
- + Qt.pc, provide pkgconfig access to qt4 macros/variables

* Thu Jul 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-8
- fix %%_qt4_prefix/doc symlink

* Thu Jun 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-7
- prepare for possible rename qt4 -> qt (+Provides: qt4)
- make _qt4_* macro usage consistent (with %%check's)

* Sat Jun 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-5
- fix rpm macros, (%%_qt_plugindir, %%_qt4_translationdir}

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-4
- .desktop Category cleanup

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-3
- cleanup qconfig.h/multilib bits, add s390x/s390

* Wed May 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-2
- ExclusiveArch: %%ix86 -> i386 (for koji)

* Wed May 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-1
- qt-4.3.0(final)

* Fri May 04 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.0-0.5.rc1
- update to 4.3.0 RC1
- drop LD_RUN_PATH hack

* Fri May 04 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.0-0.3.snapshot20070423
- update to qt-4.3.0-snapshot-20070423
- build with SSL support (BR openssl-devel)
- drop upstreamed mysql_config.patch

* Wed May 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-0.2.beta
- qt-4.3.0beta
- -system-libtiff, BR: libtiff-devel

* Wed May 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-8
- QFileDialog file wrapping patch (qt#153635, rh#236908)
- License: GPL, dropping LICENSE.QPL (#237702)

* Thu Mar 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-7
- CVE-2007-0242, utf8-bug-qt4-2.diff

* Thu Mar 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-6
- -system-sqlite, BR: sqlite-devel
- drop mysql_config hackery

* Wed Mar 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-5
- strip (all) glib2 libs from .pc files
- prepend _ to rpm macros
- drop Obsoletes: qt4-debug

* Thu Mar 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-3
- make /etc/rpm/macros.qt4 owned only by qt4-devel

* Thu Mar 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-2
- fix mkspecs/common availability (#232392)

* Tue Mar 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-1
- qt-4.2.3
- multilib: move all arch-specific mkspecs bits to %%qt4_prefix/mkspecs (#223663)
- +%%_sysconfdir/rpm/macros.qt4
- +%%config %%qt4_sysconfdir/Trolltech.conf

* Tue Mar 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-8
- multilib: qconfig.pri, /etc/profile.d/* (#223663)

* Mon Mar 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-7
- fixup qconfig-multilib.h for powerpc/powerpc64 (#223663)
- include qt-copy's 0154-qdbuscpp2xml-moc_path.diff (#230875)

* Wed Feb 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-5
- fixup qconfig-multilib.h (#223663)
- qt4.(sh|csh): define QMAKESPEC (#223663)
- null'ify QMAKE_LIBDIR_QT, leave QMAKE_INCDIR_QT alone for now. (#230224)

* Tue Feb 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-3
- drop ./configure -no-reduce-exports (ie, support visibility) 
- multilib issues (#223663)

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net. 4.2.2-2
- respin for postgresql

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.2-1
- qt-4.2.2 (#218575)

* Wed Nov 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-3
- move libQtDesigner to -x11

* Mon Oct 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-2
- use respun upstream 4.2.1 tarball
- fix pre-modular-X libGL/libGLU deps (#211898)

* Sun Oct 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-1
- qt-4.2.1

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-1
- qt-4.2.0(final)

* Thu Sep 28 2006 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.0-0.9.20060927
- update to qt-4.2.0-snapshot-20060927
- update QDBus executable names
- -x11: exclude plugins/designer (which belong to -devel)
- BuildConflicts: qt4-devel
- drop -fno-strict-aliasing hack (fc5+)

* Wed Sep 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.8.rc1
- qtconfig.desktop: Categories=+AdvancedSettings;Settings

* Fri Sep 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.7.rc1
- 4.2.0-rc1

* Fri Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.6.20060821
- update to 4.2.0-snapshot-20060821 (same as today's qt-copy)
- -no-separate-debug-info
- - ./configure -xfixes, BR: libXfixes-devel

* Mon Aug 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.5.tp1
- fix empty -debuginfo
- use $RPM_OPT_FLAGS

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.4.tp1
- strip -laudio, -ldbus-1, -lglib-2.0 from .pc files

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.3.tp1
- -no-reduce-exports (for now)
- -fno-strict-aliasing (fc5+)

* Fri Jul 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.2.tp1
- -system-nas-sound, BR: nas-devel (bug # 197937)
- -qdbus (fc6+, BR: dbus-devel >= 0.62)
- -glib (BR: glib2-devel)

* Fri Jun 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.1.tp1
- 4.2.0-tp1 (technology preview 1)

* Thu Jun 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-5
- make FHS-friendly (bug #196901)
- cleanup %%_bindir symlinks, (consistently) use qt4 postfix

* Wed Jun 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-4
- x11: split-out gui(x11) from non-gui bits (bug #196899)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-3
- -debug: drop, adds nothing over -debuginfo, make lib..._debug 
  symlinks instead (bug #196513)
- assistant.desktop: fix tooltip (bug #197039)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-2
- -devel: include -debug libs (bug #196513)
- -devel: move libQtDesigner here
- -config: mash into main pkg, should be multilib friendly now

* Fri Jun 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-1
- 4.1.4

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-9
- make each sql plugin optional

* Fri Jun 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-8
- qmake.conf: undefine QMAKE_STRIP to get useful -debuginfo (bug #193602)
- move (not symlink) .pc files into %%_libdir/pkgconfig

* Thu Jun 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-7
- *really* fix qt4-wrapper.sh for good this time.

* Mon May 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-6
- make qt4-wrapper.sh use rpm when pkg-config/qt4-devel isn't
  installed (#193369)

* Fri May 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-5
- strip -lXi from .pc files (#193258)
- simplify sql plugin builds via %%buildSQL macro
- -libdir %%qt_libdir 

* Wed May 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-4
- move (most) %%dir ownership (back) to main pkg

* Sun May 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-3
- fix %%mysql_libs macro

* Sat May 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-2
- -mysql: use mysql_config for setting cflags/ldflags.
- -mysql: BR: mysql-devel > 4.0

* Sat May 20 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org>
- Fix the last reference to %{qtdir}/lib: use %{_lib} instead of "lib".
- Fix the ownership of subpackages: they need to own parents of directories they install files in.

* Fri May 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-1
- 4.1.3
- %%qtdir/lib/*.pc -> %%qtdir/%%_lib/*.pc 
  (hopefully, the last hardcoded reference to %%qtdir/lib)

* Fri May 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-20
- fix some unowned dirs
- try harder to purge %%builddir from .pc,.prl files
- -docdir %%_docdir/%%name-doc-%%version, since we use %%doc macro in main pkg
- -doc: own %%qt_docdir
- use qt4-wrapper.sh to ensure launch of qt4 versions of apps that
  (may) overlap with those from qt3 
- use %%qtdir/%%_lib in ld.so.conf.d/*.conf files too

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-19
- drop libQtAssistantClient,libQtUiTools shlib patches

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-18
- %%_bindir symlinks: qtconfig4 -> qt4config, qtdemo4 -> qt4demo
- -libdir %%qtdir/%%_lib, simplifies %%_lib != lib case
- -docdir %%_docdir/%%name-%%version
- build shared versions of libQtAssistantClient,libQtUiTools too
- strip extraneous -L paths, libs from *.prl files too

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-17
- .desktop: Qt -> Qt4, and Comment= (where missing)
- -devel: include -designer here, Obsoletes/Provides: %%name-designer.
   It's small, simplifies things... one less subpkg to worry about.
- -doc: include %%qtdir/doc symlink here
- -docdir %%_docdir/%%name-doc-%%version

* Mon May 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-16
- set/use RPM_OPT_FLAGS only for our platform
- (really) don't give %%_bindir symlink for qt3to4 another "4" suffix
- don't add 4 suffix to uic3, rcc (they don't conflict with qt(3)-devel)
- -devel: add  linguist.desktop
- -doc: move assistant here, Provides: %%{name}-assistant, add assistant.desktop
- -doc: add qtdemo.desktop
- -doc: Requires qt4 (instead of qt4-devel)
- assistant4.patch: search for assistant4 instead of (qt3's) assistant in $PATH 
- -qtconfig: add qtconfig.desktop
- updated %%sumaries to mention where (some) tools are, including assistant, linguist,
  qtdemo

* Mon May 15 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 4.1.2-15
- Rename -docs to -doc.
- Files in the -doc subpackage are no longer in %%doc.
- Move qtdemo to the subpackage -doc.
- Fix symlinks in %%{_bindir}.
- Only modify mkspecs/linux-g++*/qmake.conf, instead of all mkspecs/*/qmake.conf.

* Sun May 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-14
- remove MapNotify from .desktop file(s).
- install -m644 LICENSE.*
- -docs: don't mark examples as %doc
- drop unused %%debug macro

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-13
- include unpackaged pkgconfig files

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-12
- fix typos so it actually builds.

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-11
- drop optional ld.so.conf.d usage, make mandatory
- make %%_bindir symlinks to all %%qtdir/bin stuff (even qt3to4)
- pkgconfig files: hardlinks -> relative symlinks, strip -L%{_libdir}/mysql
  and -L%%{_builddir}/qt-x11-opensource-src-%%version/lib
- cleanup/simplify Summary/%%description entries
- $RPM_BUILD_ROOT -> %%buildroot, $RPM_BUILD_DIR -> %%_builddir

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-10
- cleanup/simplify license bits, include LICENSE.QPL
- drop unused -styles/-Xt subpkg reference
- drop unused motif extention bits
- drop initialpreference from .desktop files

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-9
- drop reference to non-existent config.test/unix/checkavail

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-8
- simplify build* macros
- lower-case all subpkgs (ie, -MySQL -> -mysql )
- drop BR: perl, sed

* Thu May 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-7
- rework %%post/%%postun, mostly to placate rpmlint
- drop Prefix:
- drop use of qt4.(sh|csh), they're empty atm anyway
- use Source'd designer.desktop (instead of inline cat/echo)
- symlinks to %%_bindir: qmake4, designer4, qtconfig4
- drop qtrc, qt4 doesn't use it.
- -docs subpkg for API html docs, demos, examples.
- BR: libXcursor-devel libXi-devel (fc5+)

* Thu Apr 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-6
- devel: Requires: pkgconfig

* Sat Apr 15 2006 Simon Perreault <nomis80@nomis80.org> 4.1.2-5
- Disable C++ exceptions.

* Mon Apr 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-4
- qt4.(sh|csh): place-holders only, don't define QTDIR (and QTLIB)
  as that (potentially) conflicts with qt-3.x.

* Thu Apr 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-2
- -devel: Drop (artificial) Conflicts: qt-devel
- fix %%ld_so_conf_d usage
- %%qtdir/%%_lib symlink

* Wed Apr 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-1
- drop Epoch
- cleanup (a lot!)

* Tue Dec 20 2005 Than Ngo <than@redhat.com> 1:4.1.0-0.1
- update to 4.1.0

* Fri Sep 09 2005 Than Ngo <than@redhat.com> 1:4.0.1-0.1
- update to 4.0.1

