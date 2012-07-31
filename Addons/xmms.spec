Name:           xmms
Version:        1.2.10
Release:        29.1%{?dist}
Epoch:          1
Summary:        The X MultiMedia System, a media player

Group:          Applications/Multimedia
License:        GPL
URL:            http://www.xmms.org/
# http://www.xmms.org/download.php, to recreate the tarball:
# $ wget http://www.xmms.org/files/1.2.x/xmms-1.2.10.tar.bz2
# $ tar jx --exclude "mpg123*" -f xmms-1.2.10.tar.bz2
# $ tar jcf xmms-1.2.10.patched.tar.bz2 xmms-1.2.10
Source0:        %{name}-%{version}.patched.tar.bz2
Source1:        xmms.sh
Source2:        xmms.xpm
Source3:        rh_mp3.c
# http://cvs.xmms.org/cvsweb.cgi/xmms/General/joystick/joy.c.diff?r1=1.8&r2=1.9
Patch0:         %{name}-1.2.10-joycrash.patch
Patch1:         %{name}-1.2.6-audio.patch
Patch2:         %{name}-1.2.6-lazy.patch
Patch3:         %{name}-1.2.8-default-skin.patch
Patch4:         %{name}-1.2.9-nomp3.patch
Patch5:         %{name}-1.2.8-arts.patch
Patch6:         %{name}-1.2.8-alsalib.patch
Patch7:         %{name}-cd-mountpoint.patch
# Patch8 on top of patch4
Patch8:         %{name}-1.2.10-multidevel.patch
Patch9:         %{name}-underquoted.patch
Patch10:        %{name}-alsa-backport.patch
Patch11:        %{name}-1.2.10-gcc4.patch
Patch12:        %{name}-1.2.10-crossfade-0.3.9.patch
Patch13:        %{name}-1.2.10-pls-188603.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk+-devel
BuildRequires:  esound-devel
BuildRequires:  arts-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  mikmod-devel
BuildRequires:  gettext-devel
BuildRequires:  zlib-devel
BuildRequires:  libGL-devel
BuildRequires:  libXt-devel
BuildRequires:  libSM-devel
BuildRequires:  libXxf86vm-devel

Requires:       unzip
Requires:       %{_datadir}/desktop-menu-patches/redhat-audio-player.desktop
Requires(post): desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

%description
XMMS is a multimedia (Ogg Vorbis, CDs) player for the X Window System
with an interface similar to Winamp's.  XMMS supports playlists and
streaming content and has a configurable interface.

%package        libs
Summary:        XMMS engine and core plugins
Group:          System Environment/Libraries

%description    libs
The X MultiMedia System player engine and core plugins.

%package        esd
Summary:        EsounD output plugin for XMMS
Group:          System Environment/Libraries
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}

%description    esd
EsounD output plugin for the X MultiMedia System.

%package        devel
Summary:        Files required for XMMS plug-in development
Group:          Development/Libraries
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
Requires:       gtk+-devel
Requires:       pkgconfig

%description    devel
Files needed for building plug-ins for the X MultiMedia System.


%prep
%setup -q
# Fix joystick plugin crashes
%patch0 -p1 -b .joycrash
# Set default output plugin to ALSA
%patch1 -p1 -b .audio
# Use RTLD_LAZY, not RTLD_NOW
%patch2 -p1 -b .lazy
# Change the default skin
%patch3 -p1 -b .default-skin
# Don't build MP3 support, support bits for MP3 placeholder
%patch4 -p1 -b .nomp3
# Link arts dynamically and detect its presence for choosing output plugin
%patch5 -p1 -b .arts
# Don't link *everything* against alsa-lib
%patch6 -p1 -b .alsalib
# Use something that's more likely to work as the default cdrom mountpoint
%patch7 -p0 -b .cd-mountpoint
# Avoid multilib devel conflicts
%patch8 -p1 -b .multidevel
# Fix m4 underquoted warning
%patch9 -p1 -b .underquoted
# Backport for recent ALSA
%patch10 -p0 -b .alsa-backport
# Fix compilation with gcc4
%patch11 -p1 -b .gcc4
# Fix for crossfade >= 0.3.9 to work properly
%patch12 -p1 -b .crossfade
# Randomize playlists better
%patch13 -p1 -b .pls
# Avoid standard paths on lib64 archs, --disable-rpath doesn't do it
sed -i -e 's|"/lib /usr/lib"|"/%{_lib} %{_libdir}"|' configure
sed -i -e 's|"/lib /usr/lib /usr/local/lib"|"/%{_lib} %{_libdir} /usr/local/lib"|' configure

for f in AUTHORS ChangeLog README ; do
    iconv -f iso-8859-1 -t utf-8 -o $f.utf8 $f ; mv $f.utf8 $f
done

%build
%configure \
    --disable-dependency-tracking \
    --enable-kanji \
    --enable-texthack \
    --enable-ipv6 \
    --with-pic \
    --disable-static
#find . -name Makefile | xargs sed -i -e s/-lpthread//g # old libtool, x86_64
make %{?_smp_mflags}

%{__cc} $RPM_OPT_FLAGS -fPIC -shared -Wl,-soname -Wl,librh_mp3.so \
    -o librh_mp3.so -I. $(gtk-config --cflags gtk) %{SOURCE3}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -pm 755 librh_mp3.so $RPM_BUILD_ROOT%{_libdir}/xmms/Input
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/xmms/Skins
find $RPM_BUILD_ROOT -name "*.la" | xargs rm -f

# On FC5 x86_64, some get created even though we pass --disable-static
rm -f $RPM_BUILD_ROOT%{_libdir}/xmms/*/*.a

# https://bugzilla.redhat.com/213172
for bin in xmms wmxmms ; do
    install -Dpm 755 $RPM_BUILD_ROOT%{_bindir}/$bin \
        $RPM_BUILD_ROOT%{_libexecdir}/$bin
    sed -e "s|/usr/libexec/xmms|%{_libexecdir}/$bin|" %{SOURCE1} > \
        $RPM_BUILD_ROOT%{_bindir}/$bin
    chmod 755 $RPM_BUILD_ROOT%{_bindir}/$bin
done

# Link to the desktop menu entry included in redhat-menus
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/applications
ln -s ../desktop-menu-patches/redhat-audio-player.desktop \
    $RPM_BUILD_ROOT%{_datadir}/applications
install -Dpm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/xmms.xpm

install -Dpm 644 xmms.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/xmms.pc

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database -q || :

%post libs -p /sbin/ldconfig

%postun
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database -q || :

%postun libs -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS TODO README
%{_bindir}/xmms
%{_bindir}/wmxmms
%{_libexecdir}/xmms
%{_libexecdir}/wmxmms
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/xmms.xpm
%{_datadir}/xmms/
%{_mandir}/man1/*xmms.1*

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libxmms.so.*
%dir %{_libdir}/xmms/
%{_libdir}/xmms/Effect/
%{_libdir}/xmms/General/
%{_libdir}/xmms/Input/
%dir %{_libdir}/xmms/Output/
%{_libdir}/xmms/Output/libALSA.so
%{_libdir}/xmms/Output/libOSS.so
%{_libdir}/xmms/Output/libdisk_writer.so
%{_libdir}/xmms/Visualization/

%files esd
%defattr(-,root,root,-)
%{_libdir}/xmms/Output/libesdout.so

%files devel
%defattr(-,root,root,-)
%{_bindir}/xmms-config
%{_includedir}/xmms/
%{_libdir}/libxmms.so
%{_libdir}/pkgconfig/xmms.pc
%{_datadir}/aclocal/xmms.m4


%changelog
* Mon Nov  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-29
- Work around incompatibilities with the Composite X extension (#213172).
- Apply upstream playlist randomization improvements (#188603).

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-28
- Rebuild.

* Wed Jun 21 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-27
- Split EsounD output plugin into -esd subpackage, don't filter dependencies.
- Make menu entry symlink relative.
- Re-enable parallel make.

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1:1.2.10-26
- don't use parallel make to try to stop the build hang

* Thu May 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-25
- Avoid multilib conflicts in -devel, introducing xmms.pc.
- Include license text in -libs.

* Tue May 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-24
- Apply upstream fix for joystick plugin crashes.

* Thu Apr  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-23
- Split library and plugins to xmms-libs (#184606).
- ALSA is ubiquitous, don't filter dependencies to it.
- Avoid standard rpaths on lib64 archs.
- Tighten versioned -devel dependency to -libs.
- Drop no longer needed Obsoletes.
- Install icon to %%{_datadir}/icons.
- Convert docs to UTF-8.
- Specfile rewrite/cleanup.
- Drop bogus Source0 URL.
- Don't use %%exclude.

* Thu Mar  2 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-22
- Remove /usr/lib64/xmms/General/libsong_change.a (fix for FC5 x86_64...).

* Mon Feb 13 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-21
- Remove gtk libs from xmms-config output, as they are only really needed for
  static linking, which we no longer support (#182267).
- Disable static in %%configure instead of excluding the built file.
- Add conditional modular X build requirements.

* Mon Feb 13 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-20
- Spec file cleanup.
- Include crossfade 0.3.9 patch.
- Remove very old x11amp obsoletes.
- Exclude static libraries, update devel summary and description for it.
- List all plugins directories in order to be aware of breakage if the
  libtool problem ever happens again.
- Fix post/postun scriplets.
- Remove xmms_logo.xpm and xmms_mini.xpm, they should be unused.
- Add libXt-devel to fullfill the "checking for X..." configure check.
- Add gettext-devel to make more configure checks happy.

* Wed Dec 28 2005 Hans de Goede <j.w.r.degoede@hhs.nl>  1:1.2.10-19
- Remove -lpthread from all LDFLAGS as this confuses the old libtool
  used by xmms on x86_64 (FE-bug #175493)
- Add missing modular Xorg BuildReqs, this (re)enables session managment
  support and the openGL plugins.

* Tue Dec 20 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-18.1
- Update gcc4 patch to include fix for xmms.org bug #1730, fixes FC5 build.

* Sat May 28 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-18
- Build with explicit --with-pic to fix compilation of flac plugin on
  x86_64.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-17
- Don't have scriplets fail if update-desktop-database returns an error.

* Sat Apr 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-16
- Use /media/cdrecorder as the default CDROM mountpoint for the CD audio
  plugin, it's more likely to work nowadays than /mnt/cdrom.
- Drop no longer needed skins tarball.
- Build with dependency tracking disabled.

* Fri Apr 15 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-15
- Change main icon from xpm to png (smaller, more consistent).
- Split off the aRts plugin.
- Split off the skins at last, as noarch (#65614).
- Remove generic INSTALL instructions.
- Remove autoconf and automake build reqs, as they're no longer called.
- Remove unneeded glib2-devel build req.

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-14
- put back conflict

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-13
- clean up spec file a bit.
- remove everything except for the last 2 yrs of changelog entries.
- make things match Fedora Extras Packaging Guidelines more

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-12
- Apply patch from David Hill RH bz: 152138

* Thu Mar 24 2005 David Hill <djh[at]ii.net> 1:1.2.10-12
- Add gcc4 patch

* Wed Jan 05 2005 Colin Walters <walters@redhat.com> 1:1.2.10-11
- Change BR on mikmod to mikmod-devel (138057)

* Tue Nov 23 2004 Colin Walters <walters@redhat.com> 1:1.2.10-10
- Add xmms-alsa-backport.patch (bug 140565, John Haxby)

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 1:1.2.10-9
- Correct update-desktop-database correction for postun

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 1:1.2.10-8
- Call update-desktop-database on correct directory

* Mon Oct 04 2004 Colin Walters <walters@redhat.com> 1:1.2.10-7
- PreReq desktop-file-utils 0.9
- Run update-desktop-database

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-6
- Fixed another underquoted m4 definition.

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-5
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 31 2004 Warren Togami <wtogami@redhat.com> 1:1.2.10-3.p
- #124701 -devel req gtk+-devel

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 1:1.2.10-2.p
- update to 1.2.10
- fix buildreqs (#114857)
- switch default output plugin to ALSA

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Than Ngo <than@redhat.com> 1:1.2.9-5.p
- enable arts plugin, it should work with arts-1.2.0-1.5 or newer.

* Sat Feb 14 2004 Than Ngo <than@redhat.com> 1:1.2.9-4.p
- disable xmms-1.2.8-arts.patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1:1.2.9-2.p
- enable ipv6 (#105774)

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1:1.2.9-1.p
- update to 1.2.9

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-4.p
- rebuild, pick up alsa plugin

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-3.p
- fix dependency blacklisting (corollary of #100917)

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 1:1.2.8-2.p
- workaround to fix arts crash

* Mon Sep  8 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-1.p
- update to 1.2.8
- clean out now-upstream stuff (Welsh po file, other patches)
- switch to Håvard's arts plugin, tweak it's default buffer size
- don't explicitly require trademarked skin name (#84554)

* Mon Jun 30 2003 Bill Nottingham <notting@redhat.com> 1:1.2.7-23.p
- add welsh po file (#98244)

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:1.2.7-22.1.p
- built for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.
