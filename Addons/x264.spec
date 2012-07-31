# $Id: x264.spec 5214 2007-02-26 15:22:36Z dag $
# Authority: matthias

%{?dist: %{expand: %%define %dist 1}}
%{?fedora: %{expand: %%define fc%{fedora} 1}}

%{!?dist:%define _with_modxorg 1}
%{?el5:  %define _with_modxorg 1}
%{?fc6:  %define _with_modxorg 1}
%{?fc5:  %define _with_modxorg 1}

%{?fc1:%define _without_glibc232 1}

%{?el3:%define _without_glibc232 1}

%{?rh9:%define _without_glibc232 1}

%{?rh7:%define _without_glibc232 1}

%{?el2:%define _without_glibc232 1}

%define date 2090331

Summary: Library for encoding and decoding H264/AVC video streams
Name: x264
Version: 0.67.1134
Release: 0.3%{?dist}
License: GPL
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html
Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/
Source: http://downloads.videolan.org/pub/videolan/x264/snapshots/x264.tar.bz2
Patch0: x264-snapshot-20061214-2245-glibc232.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: nasm, yasm, gettext
%{?_with_visualize:%{?_with_modxorg:BuildRequires: libXt-devel}}
%{?_with_visualize:%{!?_with_modxorg:BuildRequires: XFree86-devel}}
# version.sh requires svnversion
BuildRequires: subversion
# no more there, drop them
Obsoletes: x264-gtk x264-gtk-devel

%description
Utility and library for encoding H264/AVC video streams.


%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
This package contains the files required to develop programs that will encode
H264/AVC video streams using the x264 library.

%prep
%setup -n %{name}
# configure hardcodes X11 lib path
%{__perl} -pi -e 's|/usr/X11R6/lib |/usr/X11R6/%{_lib} |g' configure

### Required for glibc < 2.3.2 (http://article.gmane.org/gmane.comp.video.x264.devel/1696)
%if %{?_without_glibc232:1}0
%patch0 -p0
%endif

%build
# Force PIC as applications fail to recompile against the lib on x86_64 without
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --enable-pthread \
    --enable-debug \
    %{?_with_visualize:--enable-visualize} \
    --enable-pic \
    --enable-shared \
    --extra-cflags="%{optflags}"
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING
%{_bindir}/x264
%{_libdir}/libx264.so.*

%files devel
%defattr(-, root, root, 0755)
%doc doc/*.txt
%{_includedir}/x264.h
%{_libdir}/pkgconfig/x264.pc
%{_libdir}/libx264.a
%{_libdir}/libx264.so

%changelog
* Fri Dec 15 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.3.20061214 - 5214/dag
- Update to 20061214 snapshot (same soname, no rebuilds required).

* Tue Oct 24 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.3.20061023
- Update to 20061023 snapshot, the last was too old for MPlayer 1.0rc1.
- Remove no longer needed gtk patch.

* Mon Sep 18 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.2.20060731
- Update to 20060917 snapshot.

* Tue Aug  1 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.2.20060731
- Update to 20060731 snapshot.
- Require the main package from the devel since we have a shared lib now.
- Remove no longer needed symlink patch.
- Enable gtk, include patch to have it build, and split off sub-packages.

* Thu Jun  8 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.2.20060607
- Switch to using the official snapshots.
- Remove no longer needed UTF-8 AUTHORS file conversion.
- Simplify xorg build requirement.
- Switch from full %%configure to ./configure with options since no autotools.
- Enable shared library at last.
- Add our %%{optflags} to the build.
- Include patch to make the *.so symlink relative.

* Thu Mar 16 2006 Matthias Saou <http://freshrpms.net/> 0.0.0-0.1.svn468
- Update to svn 468.
- Lower version from 0.0.svn to 0.0.0 since one day 0.0.1 might come out,
  this shouldn't be much of a problem since the lib is only statically linked,
  thus few people should have it installed, and build systems which aren't
  concerned about upgrade paths should get the latest available package.

* Thu Feb 23 2006 Matthias Saou <http://freshrpms.net/> 0.0.439-1
- Update to svn 439.

* Thu Jan 12 2006 Matthias Saou <http://freshrpms.net/> 0.0.396-2
- Enable modular xorg conditional build.

* Mon Jan  9 2006 Matthias Saou <http://freshrpms.net/> 0.0.396-1
- Update to svn 396.

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.0.380-2
- Also force PIC for the yasm bits, thanks to Anssi Hannula.

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.0.380-1
- Update to svn 380.
- Force PIC as apps fail to recompile against the lib on x86_64 without.
- Include new pkgconfig file.

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.

