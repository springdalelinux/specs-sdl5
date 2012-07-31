Name:           openal
Version:        0.0.9
Release:        0.9.20060204cvs%{?dist}
Summary:        Open Audio Library

Group:          System Environment/Libraries
License:        LGPL
URL:            http://www.openal.org/
# source from cvs
#cvs -d:pserver:guest@opensource.creative.com:/usr/local/cvs-repository login
#(use password "guest")
#cvs -d:pserver:guest@opensource.creative.com:/usr/local/cvs-repository co MODULE 
Source0:        openal-cvs-20060204.tar.bz2
Source1:        openalrc
Patch0:         openal-arch.patch
Patch1:         openal-no-undefined.patch
Patch2:         openal-pkgconfig.patch
Patch3:         openal-pause.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel
BuildRequires:  arts-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  esound-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  SDL-devel
BuildRequires:  texinfo
Obsoletes:      %{name}-test < 0.0.8
BuildRequires:  libtool

%description
OpenAL is an audio library designed in the spirit of OpenGL--machine
independent, cross platform, and data format neutral, with a clean,
simple C-based API.


%package        devel
Summary:        Development files for openal library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains development files for the openal library.

OpenAL is an audio library designed in the spirit of OpenGL - machine
independent, cross platform, and data format neutral, with a clean,
simple C-based API.


%prep
%setup -q -n portable
%patch1
%patch2
%patch3 -p1
./autogen.sh
%patch0 -p1

%build
%configure --enable-arts                   \
           --enable-alsa                   \
           --enable-esd                    \
           --enable-vorbis                 \
           --enable-sdl                    \
           --disable-smpeg                 \
           --enable-capture

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT}

rm -f $RPM_BUILD_ROOT%{_libdir}/libopenal.{l,}a

install -Dpm 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/openalrc
rm -rf common/specification/CVS

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NOTES README TODO
%config(noreplace) %{_sysconfdir}/openalrc
%{_libdir}/libopenal.so.*

%files devel
%defattr(-,root,root,-)
%doc common/specification/*
%{_bindir}/openal-config
%{_includedir}/AL/
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc


%changelog
* Sat Nov 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.9.20060204
- fix #190438

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.8.20060204
- FE6 rebuild

* Mon Aug 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.7.20060204
- apply patch from Hans de Goede (#202260)

* Tue Aug 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.6.20060204
- fix #200439

* Mon Feb 27 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.5.20060204
- revert back to old cvs snapshot to avoid soname change for now...
- fix openal-config and pkg-config in a better fashion

* Sun Feb 26 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.4.20060226
- fix #181989

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.3.20060204
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.2.20060204
- pkgconfig should include pthread

* Sat Feb 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.9-0.1.20060204
- switch to cvs again (suggested by upstream)


* Thu Jan 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0.8-2
- switch to non cvs sources
- major cleanups

* Sat Oct  8 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.8-1
- 0.0.8, patches applied upstream.
- Mark /etc/openalrc as noreplace.
- Don't ship static library.
- Drop test subpackage.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.0-0.4.20040726
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.0-0.3.20040726
- rebuilt

* Thu Apr 08 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.0-0.2.fdr.0.20040726
- Clean up spec/Bump release

* Thu Apr 08 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.1.fdr.0.20040726
- cvs snapshot.
- Changed naming of release. (#1469)
- Dropped Requires(foo,bar) notation.

* Thu Apr 08 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.fdr.0.6.20040407
- cvs snapshot.
- --enable-alsa.
- BuildReq alsa-lib-devel.

* Fri Oct 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.fdr.0.5.20031006
- Fixed file attributes.

* Tue Oct 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.fdr.0.4.20031006
- Updated from cvs.
- Remove smpeg support.

* Tue Sep 02 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.fdr.0.3.20030902
- Updated from cvs.
- snapshot made with export now.
- Added %%{?_smp_mflags}.

* Wed Aug 13 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.fdr.0.2.20030813
- Corrected file permissions in tarball.
- Removed unneeded files from tarball (windows,mac,etc).

* Wed Aug 13 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.0-0.fdr.0.1.20030813
- Updated to cvs.
- modified versioning to avoid future epoch issues.

* Tue Aug 12 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 20030131-0.fdr.2
- BuildReq automake.
- BuildReq autoconf.
- Remove --enable-arch-asm.
- Remove --enable-optimization.
- new subpackage: test.
- Commented out alsa support in openalrc.

* Thu Jul 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 20030131-0.fdr.1
- Fedorafied

* Mon Feb 10 2003 - sbrabec@suse.cz
- Use %%install_info (bug #23445).

* Mon Feb 10 2003 - sbrabec@suse.cz
- Updated to 20030131 CVS snapshot.

* Wed Oct 30 2002 - sbrabec@suse.cz
- Updated to actual CVS version.
- Fixed compiler warnings.

* Fri Aug 30 2002 - pmladek@suse.cz
- fixed dependency of the devel subpackage on the main package (used %%version)

* Fri Jul 05 2002 - kukuk@suse.de
- Use %%ix86 macro

* Mon Apr 08 2002 - pmladek@suse.cz
- arch specific assembler is only for i386
- fixed includes for ia64

* Wed Apr 03 2002 - pmladek@suse.cz
- used some pieces from old patches
- fixed to compile with autoconf-2.53:
- fixed acinclude.m4, used aclocal
- some fixes in configure.in
- cleaned up spec file
- removed boom.mp3 to avoid potential license problems

* Wed Feb 20 2002 - ro@suse.de
- removed kdelibs3-artsd from neededforbuild
  (artsd is there anyway)

* Sat Feb 16 2002 - sndirsch@suse.de
- enabled optimization and arch specific assembler

* Fri Feb 15 2002 - sndirsch@suse.de
- added SMPEG/SDL support to get MP3 playback support (required
  by VegaStrike)

* Fri Feb 15 2002 - ro@suse.de
- changed neededforbuild <kdelibs3-artsd> to <arts arts-devel>

* Fri Feb 08 2002 - bk@suse.de
- (re)enable optimisations and move prepare stuff to %%prep

* Thu Feb 07 2002 - sndirsch@suse.de
- added Ogg/Vorbis and Capture support
- removed compiler flags "-Werror -pedantic-errors"

* Thu Feb 07 2002 - sndirsch@suse.de
- added support for aRTs and esound daemon
- added global config file + a small patch to read this one

* Wed Feb 06 2002 - tiwai@suse.de
- added ALSA 0.9.0 support.  see README.alsa.
- clean up spec file, using %%_libdir.
- removed SDL.

* Fri Feb 01 2002 - sndirsch@suse.de
- updated to CVS sources of 20020201 (required for vegastrike)
- disabled patches (not required any more)

* Fri Jan 11 2002 - pmladek@suse.cz
- devel package created
- used macro %%{_librdir} to fix for lib64

* Wed Aug 08 2001 - ro@suse.de
- changed neededforbuild <sdl> to <SDL>
- changed neededforbuild <sdl-devel> to <SDL-devel>

* Tue May 22 2001 - pmladek@suse.cz
- fixed include files on ia64
- fixed preprocessor warnigs by patch for alpha

* Tue May 08 2001 - mfabian@suse.de
- bzip2 sources

* Thu Apr 19 2001 - pmladek@suse.cz
- fixed to compile on axp

* Wed Apr 04 2001 - schwab@suse.de
- Pass -relax to linker on ia64.
- Fix makefile to use LDFLAGS.
- Remove -fPIC when building non-library object.

* Mon Mar 26 2001 - ro@suse.de
- changed neededforbuild <sdl> to <sdl sdl-devel>

* Thu Nov 30 2000 - ro@suse.de
- added suse-update-config

* Mon Nov 06 2000 - ro@suse.de
- fixed neededforbuild

* Thu Jun 08 2000 - cihlar@suse.cz
- uncommented %%clean

* Tue May 09 2000 - smid@suse.cz
- buildroot added
- upgrade to version from 08.05.2000

* Tue Apr 11 2000 - sndirsch@suse.de
- removed '-Werror' and '-pedantic-erros' compiler flags

* Mon Mar 27 2000 - uli@suse.de
- renamed dif for easier maintenance
- __linux -> __linux__
- now uses RPM_OPT_FLAGS
  Wed Mar 15 19:31:35 CET 2000
- added test demos

* Thu Mar 09 2000 - sndirsch@suse.de
- created package
