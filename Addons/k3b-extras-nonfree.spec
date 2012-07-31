%define k3bmajor 0.12

Name:           k3b-extras-nonfree
Version:        0.12.17
Release:        5%{?dist}
Summary:        Additional codec plugins for the k3b CD/DVD burning application

Group:          Applications/Multimedia
License:        GPL
URL:            http://www.k3b.org
Source0:        http://mesh.dl.sourceforge.net/sourceforge/k3b/k3b-0.12.17.tar.bz2
#Source0:        http://dl.sf.net/k3b/k3b-0.12.17.tar.bz2
# Patch touches globals, better include this.
Patch0:         k3b-0.12.17-statfs.patch
Patch1:         k3b-0.11.24-no-bad-gcc.patch
Patch2:		k3b-compilefixes.patch
Patch3:		k3b-ffmpegfixes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

ExcludeArch:    s390 s390x

BuildRequires:  k3b >= %{k3bmajor}
# Some of these are only to make the configure script happy.
BuildRequires:  kdelibs-devel libart_lgpl-devel arts-devel
BuildRequires:  zlib-devel libpng-devel libjpeg-devel
BuildRequires:  libmad-devel taglib-devel lame-devel
BuildRequires:  ffmpeg-devel libmusicbrainz-devel
BuildRequires:  gettext
# KDE >= 3.2
BuildRequires:  libmng-devel fam-devel glib2-devel alsa-lib-devel esound-devel

Requires:       k3b >= %{k3bmajor}

Obsoletes:      k3b-mp3 < %{version}-%{release}
Provides:       k3b-mp3 = %{version}-%{release}

%description
Additional decoder/encoder plugins for k3b, a feature-rich and easy to
handle CD/DVD burning application.


%prep
%setup -q -n k3b-%{version}
%patch0 -p1 -b .statfs
%patch1 -p1 -b .no-bad-gcc
%patch2 -p1 -b .compilefixes
%patch3 -p1 -b .ffmpegfixes


%build
unset QTDIR
[ -z "$QTDIR" ] && . /etc/profile.d/qt.sh
%configure --disable-rpath \
	--with-external-libsamplerate=no \
	--without-oggvorbis \
	--without-flac \
	--without-sndfile \
	--without-hal \
	--without-musepack \
	--with-k3bsetup=no \
	--with-qt-libraries=$QTDIR/lib \
	--with-extra-includes=/usr/include/ffmpeg

# We need just a few k3b core libs.
make %{?_smp_mflags} -C libk3bdevice
make %{?_smp_mflags} -C libk3b
# Now build individual plugins.
make %{?_smp_mflags} -C plugins/decoder/mp3
make %{?_smp_mflags} -C plugins/decoder/ffmpeg
make %{?_smp_mflags} -C plugins/encoder/lame


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT -C plugins/decoder/mp3
make install DESTDIR=$RPM_BUILD_ROOT -C plugins/decoder/ffmpeg
make install DESTDIR=$RPM_BUILD_ROOT -C plugins/encoder/lame


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,755)
#%exclude %{_libdir}/kde3/*.la
%{_libdir}/kde3/libk3bmaddecoder.*
%{_libdir}/kde3/libk3bffmpegdecoder.*
%{_libdir}/kde3/libk3blameencoder.*
%{_datadir}/apps/k3b/plugins/k3bmaddecoder.plugin
%{_datadir}/apps/k3b/plugins/k3bffmpegdecoder.plugin
%{_datadir}/apps/k3b/plugins/k3blameencoder.plugin


%changelog
* Mon Dec 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.12.17-3
- respin for new ffmpeg

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.12.17-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12.17-1
- Update to 0.12.17.

* Fri Mar 31 2006 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.14-2
- Don't build libsndfile plugin anymore, since it moves to k3b-extras.

* Wed Mar 15 2006 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.14-1
- Update to 0.12.14.
- The oh-so-clever build speed-up trick cannot be used anymore,
  since libtool archives have been dropped from FC k3b package.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sat Dec 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.10-0.lvn.1
- Update to 0.12.10.
- Rename package to k3b-extras-nonfree.

* Sun Jul 17 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.12.2-0.lvn.1
- Update to 0.12.2 (for FC Development).
- Rename package to k3b-extras.
- Add plugins: ffmpeg decoder, libsndfile decoder, lame encoder.
- Use BR k3b to speed up build.
- Drop explicit Epoch 0.

* Fri May 20 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0:0.11.24-0.lvn.2
- Use configure-parm "--with-qt-libraries=$QTDIR/lib" to fix FC4-x86_64 build

* Wed May 11 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.24-0.lvn.1
- Update to 0.11.24 (advertised as handling mp3 errors better).
- Remove GCC version check which blacklists FC4's GCC (d'oh!).
- Explicity disable external libsamplerate, which is in FE and
  hence FC's k3b doesn't use it either.
- Merge statfs patch from FC's k3b package.

* Thu Mar 24 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.22-0.lvn.1
- Update to 0.11.22 (MAD decoder update).
- Use new switches to disable OggVorbis and FLAC explicitly.

* Wed Jan 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.19-0.lvn.1
- Update to 0.11.19 (for another mp3 detection fix).

* Tue Aug 10 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.14-0.lvn.1
- Update to 0.11.14 (which obsoletes patches again).

* Tue Aug 10 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.11.13-0.lvn.1
- Add patch from CVS to fix mp3 decoder.

* Sat Aug  7 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.13-0.lvn.1
- Updated to 0.11.13 (includes new mp3 backport).
- Patch for k3bdiskinfo.cpp is obsolete.
- Now k3bdevice.cpp needs patch for Qt 3.1.
- Remove a few more unneeded BR.

* Thu May 27 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.10-0.lvn.1
- Update to 0.11.10 (includes mp3 fixes).
- Fix k3bdiskinfo.cpp for Qt 3.1.
- Remove redundant BR qt-devel.
- Disable RPATH (seems to work now).
- Rename package to k3b-mp3, build just the plugin and all depending targets.
- Delete old changelog entries which are no longer relevant to this package.

* Mon Mar 29 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.9-0.fdr.1
- Update to 0.11.9.

* Mon Mar 29 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.11.8-0.fdr.1
- Update to 0.11.8.

* Sun Mar 28 2004 Michael Schwendt <mschwendt[AT]users.sf.net>
- Rewrite the conditional code sections, although they work fine in
  normal build environments and the fedora.us build system. But 'mach'
  makes some weird assumptions about build requirements in spec files
  and causes unexpected results.

