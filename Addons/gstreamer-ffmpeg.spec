Name:           gstreamer-ffmpeg
Version:        0.10.6
Release:        4%{?dist}
Summary:        GStreamer FFmpeg-based plug-ins
Group:          Applications/Multimedia
License:        LGPL
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg-%{version}.tar.bz2
Patch0:         gst-ffmpeg-0.10.1-syslibs.patch
Patch1:		gst-ffmpeg-compilefixes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gstreamer-devel >= 0.10.0
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:  ffmpeg-devel liboil-devel libtool bzip2-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

This package provides FFmpeg-based GStreamer plug-ins.


%prep
%setup -q -n gst-ffmpeg-%{version}
#patch0 -p1 -z .syslibs
#patch1 -p1 -b .compilefixes
#rm -fr gst-libs
perl -pi -e 's|0.10.22|0.10.20|' configure configure.ac


%build
# according to ChangeLog -O2 breaks some asm code so use -O1
export CFLAGS="`echo $RPM_OPT_FLAGS|sed s/-O2/-O1/` \
  -Wno-deprecated-declarations -Wno-pointer-sign"
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/libgst*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/gstreamer-0.10/libgstffmpeg.so
%{_libdir}/gstreamer-0.10/libgstpostproc.so
%{_libdir}/gstreamer-0.10/libgstffmpegscale.so


%changelog
* Thu Mar 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-2
- Rebuild so that the demuxers get build too (livna bz 1464)

* Fri Jan 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-1
- Official upstream 0.10.2 release

* Mon Dec 18 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.4.20061108
- Rebuild for new ffmpeg

* Wed Nov 22 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.3.20061108
- link libgstpostproc.so with -lpostproc (bug #1288)

* Thu Nov  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.2.20061108
- Add missing liboil-devel BR

* Wed Nov  8 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.1.20061108
- New release based on CVS snapshot as upstream hasn't made a new release
  in a while, this fixes bug lvn1235

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.10.1-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-3
- Rebuild for FC-6

* Sun Aug 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-2
- Fix compilation with newer ffmpeg
- drop unnecesarry gcc-c++ BR

* Sun Jul 30 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-1
- Minor specfile cleanups for livna submission.
- Add a patch to use the system ffmpeg instead of the included one

* Fri Mar 31 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.1-0.gst.1
- update for new release

* Wed Mar 29 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0.2-0.gst.1
- update for new prerelease

* Fri Mar 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.3
- allow "gstreamer" define to be overridden

* Wed Dec 14 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.2
- rebuild against glib 2.8

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release with 0.10 major/minor

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-0.gst.1
- new upstream release

* Wed Oct 26 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- new upstream release

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new upstream release

* Sat Sep 17 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.6-0.gst.1 new upstream release

* Tue Jun 21 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5-0.gst.1: for our repo

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5-0.lvn.1: new release

* Fri Mar 11 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.4-0.lvn.1: new release

* Fri Dec 31 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3-0.lvn.1: new release

* Fri Dec 24 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.2.2-0.lvn.1: new prerelease

* Tue Oct 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.2-0.lvn.1: new upstream release

* Fri Jul 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-0.lvn.1: new upstream release

* Fri May 21 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.lvn.2: update for FC2 and SDL-devel not requiring alsa-lib-devel

* Tue Mar 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.lvn.1: new source release, changed base name to gstreamer

* Fri Mar 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.1-0.lvn.2: sync with FreshRPMS

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.1-0.lvn.1: First package for rpm.livna.org
