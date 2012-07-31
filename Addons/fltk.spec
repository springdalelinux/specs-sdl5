
%define snap    r5555
#define _disable_static --disable-static

Summary:	C++ user interface toolkit
Name:		fltk
Version:	1.1.7
Release:	8.%{snap}%{?dist}

License:	LGPL with exceptions
Group:		System Environment/Libraries
URL:		http://www.fltk.org/
%if "%{?snap:1}" == "1"
Source0:        ftp://ftp.easysw.com/pub/fltk/snapshots/fltk-1.1.x-%{snap}.tar.bz2
%else
Source0:        http://ftp.easysw.com/pub/fltk/%{version}/%{name}-%{version}-source.tar.bz2
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# See http://bugzilla.redhat.com/199656
Patch1:         fltk-1.1.7-config.patch
Patch2:         fltk-1.1.7-test.patch

%if 0%{?rhel} > 4 || 0%{?fedora} > 4
BuildRequires:  libICE-devel libSM-devel
BuildRequires:	libXext-devel libXft-devel libXt-devel libX11-devel
BuildRequires:  xorg-x11-proto-devel 
%else
BuildRequires:  xorg-x11-devel
%endif
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libGL-devel libGLU-devel 
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:	man

%description
FLTK (pronounced "fulltick") is a cross-platform C++ GUI toolkit.
It provides modern GUI functionality without the bloat, and supports
3D graphics via OpenGL and its built-in GLUT emulation.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:       libGL-devel libGLU-devel
%if 0%{?rhel} > 4 || 0%{?fedora} > 4
Requires:       libXft-devel libXext-devel
Requires:       libX11-devel libSM-devel libICE-devel
%else
Requires:       xorg-x11-devel
%endif
%description devel
%{summary}.

%package fluid
Summary:	Fast Light User Interface Designer
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}
%description fluid
%{summary}, an interactive GUI designer for %{name}. 


%prep
%if "%{?snap:1}" == "1"
%setup -q -n fltk-1.1.x-%{snap}
%else
%setup -q 
%endif

%if "%{?snap:1}" != "1"
%patch1 -p1 -b .199656
%endif
%patch2 -p1 -b .test


%build
export CPPFLAGS="$(pkg-config xft --cflags)"
export LDFLAGS="$(pkg-config xft --libs)"

%configure \
  %{?_disable_static} \
  --enable-shared \
  --enable-threads \
  --enable-xdbe \
  --enable-xft

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT 

# Makefile hack for 64bitness
%if "%{_lib}" != "lib"
mkdir -p $RPM_BUILD_ROOT%{_libdir}
pushd $RPM_BUILD_ROOT%{_libdir}/..
ln -s %{_lib} lib
popd
%endif

make install install-desktop DESTDIR=$RPM_BUILD_ROOT 

# Makefile hack for 64bitness
%if "%{_lib}" != "lib"
rm -f  $RPM_BUILD_ROOT%{_libdir}/../lib
%endif

desktop-file-install --vendor=%{name} \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category="Development" \
  --add-category="GUIDesigner" \
  --delete-original \
    $RPM_BUILD_ROOT%{_datadir}/applnk/Development/*.desktop

# docs
rm -rf __docs
mv $RPM_BUILD_ROOT%{_docdir}/fltk __docs

## unpackaged files
# errant docs
rm -rf $RPM_BUILD_ROOT%{_mandir}/cat*
%if "%{?_disable_static:1}" == "1"
# static libs
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.a
%endif
# omit examples/games: 
make -C test uninstall-linux DESTDIR=$RPM_BUILD_ROOT
rm -f  $RPM_BUILD_ROOT%{_mandir}/man?/{blocks,checkers,sudoku}*


%check
make test ||:


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post fluid
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:

%postun fluid
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:


%files
%defattr(-,root,root,-)
%doc ANNOUNCEMENT CHANGES COPYING CREDITS README
%{_libdir}/libfltk.so.*
%{_libdir}/libfltk_forms.so.*
%{_libdir}/libfltk_gl.so.*
%{_libdir}/libfltk_images.so.*

%files devel
%defattr(-,root,root,-)
%doc __docs/*
%{_bindir}/fltk-config
%{_includedir}/FL/
%{_includedir}/Fl
%{_libdir}/libfltk.so
%{_libdir}/libfltk_forms.so
%{_libdir}/libfltk_gl.so
%{_libdir}/libfltk_images.so
%if "%{?_disable_static:1}" != "1"
%{_libdir}/libfltk.a
%{_libdir}/libfltk_forms.a
%{_libdir}/libfltk_gl.a
%{_libdir}/libfltk_images.a
%endif
%{_mandir}/man1/fltk-config.1*
%{_mandir}/man3/fltk.3*

%files fluid
%defattr(-,root,root,-)
%{_bindir}/fluid
%{_mandir}/man1/fluid.1*
%{_datadir}/applications/*fluid.desktop
# FIXME
%{_datadir}/mimelnk/*/*.desktop
%{_datadir}/icons/hicolor/*/*/*


%changelog
* Wed Dec 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-8.r5555
- more 64bit hackage to workaround broken Makefile logic (#219348)

* Wed Dec 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-7.r5555
- fltk-1.1.x-r5555 snapshot, for 64bit issues (#219348)
- restore static libs (they're tightly coupled with fltk-config)
- cleanup %%description's

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-6
- move tests to %%check section

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-5
- use included icon/.desktop files
- fix up fltk-config (#199656)

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.7-3
- follow icon spec
- omit static libs

* Wed Sep 06 2006 Michael J. Knox <michael[AT]knox.net.nz> - 1.1.7-2
- rebuild for FC6

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.7-1
- Upstream update

* Thu Nov 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-4
- Fixed BR and -devel Requires for modular X

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-3
- Update BuildRequires as well

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-2
- Update Requires for -devel

* Thu Oct 27 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.6-1
- Upstream update

* Thu Aug 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.4-10
- Fixed BR/Requires for x86_64

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Nov 20 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.8
- Hopefully fixed Xft flags for rh80

* Thu Nov 20 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.7
- Fixed typo

* Thu Nov 20 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.6
- Added xft.pc build dependency
- Added BuildReq:man

* Sun Nov  9 2003 Ville Skyttä <ville.skytta@iki.fi> 0:1.1.4-0.fdr.4
- Spec file cleanup
- Enabled xft and threads

* Tue Oct 28 2003 Dams <anvil[AT]livna.org> - 0:1.1.4-0.fdr.3
- Added missing symlink in includedir

* Wed Oct  1 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.2
- Removed comment after scriptlets

* Wed Oct  1 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.1
- Updated to final 1.1.4

* Wed Sep 24 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.0.4.rc1
- Fixed documentation path in configure

* Fri Aug 29 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.0.3.rc1
- Fixed typo in desktop entry
- Added missing BuildRequires ImageMagick and desktop-file-utils

* Fri Aug 29 2003 Dams <anvil[AT]livna.org> 0:1.1.4-0.fdr.0.2.rc1
- Moved fluid to its own package
- Added missing Requires for devel package

* Sat Aug 16 2003 Dams <anvil[AT]livna.org>
- Initial build.
