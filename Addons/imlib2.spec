Summary:        Image loading, saving, rendering, and manipulation library
Name:           imlib2
Version:        1.3.0
Release:        3%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            http://www.enlightenment.org/Libraries/Imlib2/
Source0:        http://download.sf.net/enlightenment/%{name}-%{version}.tar.gz
Patch0:         imlib2-1.2.1-X11-path.patch
Patch1:         imlib2-1.3.0-multilib.patch
Patch2:         imlib2-1.3.0-loader_overflows.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  libjpeg-devel libpng-devel libtiff-devel
BuildRequires:  giflib-devel freetype-devel >= 2.1.9-4 libtool bzip2-devel
BuildRequires:  libX11-devel libXext-devel libid3tag-devel pkgconfig

%package devel
Summary:        Development package for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel libXext-devel freetype-devel >= 2.1.9-4 pkgconfig


%description
Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.

%description devel
This package contains development files for %{name}.

Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.


%prep
%setup -q
%patch0 -p1 -b .x11-path
%patch1 -p1 -b .multilib
%patch2 -p1 -b .overflow
# sigh stop autoxxx from rerunning because of our patches above.
touch aclocal.m4
touch configure
touch config.h.in
touch `find -name Makefile.in`


%build
asmopts="--disable-mmx --disable-amd64"
%ifarch %{ix86} ia64
asmopts="--enable-mmx --disable-amd64"
%endif
%ifarch x86_64
asmopts="--disable-mmx --enable-amd64"
%endif

# Note: --disable-static doesn't work as of 1.2.1.
%configure --disable-dependency-tracking --with-pic $asmopts

make %{?_smp_mflags} LIBTOOL=/usr/bin/libtool


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBTOOL=/usr/bin/libtool

rm -f \
  $RPM_BUILD_ROOT%{_libdir}/imlib2/{loaders,filters}/*.a \
  $RPM_BUILD_ROOT%{_bindir}/imlib2_test

# ship .la files due to a bug in kdelibs (bugzilla.fedora.us #2284):
#  $RPM_BUILD_ROOT%{_libdir}/libImlib2.la \


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README ChangeLog TODO
%{_bindir}/imlib2_*
%{_libdir}/libImlib2.so.*
%dir %{_datadir}/imlib2/
%{_datadir}/imlib2/data/
%dir %{_libdir}/imlib2/
%dir %{_libdir}/imlib2/filters/
%{_libdir}/imlib2/filters/*.so
%{_libdir}/imlib2/filters/*.la
%dir %{_libdir}/imlib2/loaders/
%{_libdir}/imlib2/loaders/*.so
%{_libdir}/imlib2/loaders/*.la

%files devel
%defattr(-,root,root,-)
%doc doc/*.gif doc/*.html
%{_bindir}/imlib2-config
%{_includedir}/Imlib2.h
%{_libdir}/libImlib2.a
%{_libdir}/libImlib2.la
%{_libdir}/libImlib2.so
%{_libdir}/pkgconfig/imlib2.pc


%changelog
* Thu Nov  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-3
- Fix CVE-2006-4806, CVE-2006-4807, CVE-2006-4808, CVE-2006-4809, thanks to
  Ubuntu for the patch (bug 214676)

* Thu Oct 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-2
- Multilib devel goodness (make -devel i386 and x86_64 parallel installable)
- Fix bug 212469
- Add libid3tag-devel to the BR's so id3tag support gets build in

* Tue Oct 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3.0-1
- New upstream release 1.3.0

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-2
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-1
- New upstream release 1.2.2

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-6
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5 (bug 185871)

* Thu Nov 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-5
- Make XPM loader use /usr/share/X11/rgb.txt.
- Drop no longer needed multilib configure options.

* Sun Nov 13 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-4
- Adapt to modular X.Org (#172613).

* Wed Sep 21 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.1-3
- Make XPM loader use /usr/lib/X11/rgb.txt instead of /usr/X11R6/...

* Sun Aug 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.1-2
- 1.2.1, patches applied/obsoleted upstream.
- Improve summary and description, fix URL.
- Move HTML docs to -devel.
- Build with dependency tracking disabled.
- Drop x86_64 freetype rpath hack, require a fixed freetype-devel.

* Mon May  9 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-8.fc4
- Fix segfault in XPM loader (#156058).

* Tue Apr  5 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-7.fc4
- Fix broken pkgconfig file.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-6
- Include imlib2 directory in datadir and libdir.

* Wed Feb  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-5
- Link loaders with the main lib, fixes load/save problems with some apps.

* Tue Jan 18 2005 Michael Schwendt <mschwendt[AT[users.sf.net> - 0:1.2.0-4
- Really include libtool archives to fix fedora.us bug #2284.

* Fri Jan 14 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-3
- Move filters and loaders back into main package where they belong

* Mon Jan 10 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-2
- Don't ship *.?.a in {_libdir}/imlib/filters/ and loaders/

* Sun Jan 09 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.2.0-1
- Ship .la files ue to a bug in kdelibs; see
  https://bugzilla.fedora.us/show_bug.cgi?id=2284
  http://bugzilla.redhat.com/bugzilla/142244
  http://bugs.kde.org/93359
- Use make param LIBTOOL=/usr/bin/libtool - fixes hardcoded rpath on x86_64
- fix hardcoded rpath im Makefiles on x86_64 due to freetype-config --libs
  returning "-L/usr/lib64 -Wl,--rpath -Wl,/usr/lib64 -lfreetype -lz"
- Update to 1.2.0 -- fixes several security issues
- remove explicit libdir=_libdir - 1.2.9 does not need it anymore
- removeddemo compile/install;
- use configure param --x-libraries={_prefix}/X11R6/{_lib} and patch to fix
  "cannot find -lX11"

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.1.2-2
- Disable mmx on x86_64 (fixes Build error)
- Add explicit libdir=_libdir to make calls to avoid install errors on x86_64
- Add --with-pic configure option (taken from Matthias Saou's package)

* Sat Sep 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.1
- Update to 1.1.2, fixes CAN-2004-0802.
- Enable MMX on all ix86, x86_64 and ia64, it seems runtime-detected.
- Update URL.

* Tue Nov 18 2003 Dams <anvil[AT]livna.org> 0:1.0.6-0.fdr.3
- s#_prefix/lib#_libdir#

* Tue Nov 18 2003 Dams <anvil[AT]livna.org> 0:1.0.6-0.fdr.2
- Moved some binaries and loaders into main package
- Added missing Requires and BuildRequires

* Sun Oct 26 2003 Dams <anvil[AT]livna.org>
- Initial build.
