Summary: LIVE.COM Streaming Media
Name: live
Version: 2007.08.03a
Release: 10%{?dist}
URL: http://www.live555.com/liveMedia/
Source0: http://live555.com/liveMedia/public/live.%{version}.tar.gz
Patch0: live-2003.01.17-opt.patch
License: LGPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: gcc-c++

%description
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP and RTSP).

%package devel
Summary: LIVE.COM Streaming Media Development Tools
Group: Development/Libraries

%description devel
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP and RTSP).

This rpm contains development tools for the LIVE.COM Streaming 
Media libraries.

%package utils
Summary: LIVE.COM Streaming Media Utilities
Group: Development/Libraries

%description utils
A set of test programs for the LIVE.COM Streaming Media libraries.

%prep
%setup0 -q -n live
#patch0
#find . -type f | xargs perl -pi -e's,strstream.h,strstream,'
sed -i -e's| -O2 | %{optflags} -fPIC |' config.linux

%build
./genMakefiles linux
make

%install
rm -rf %{buildroot}

for f in liveMedia UsageEnvironment groupsock BasicUsageEnvironment
do
	mkdir -p %{buildroot}%{_libdir}/live/$f/include
	cp $f/lib$f.a %{buildroot}%{_libdir}/live/$f
	cp $f/include/*.h* %{buildroot}%{_libdir}/live/$f/include
done

mkdir -p %{buildroot}%{_bindir}

for file in testMP3Streamer testMP3Receiver testRelay testMPEG1or2Splitter \
  testMPEG1or2VideoStreamer testMPEG1or2VideoReceiver testMPEG1or2AudioVideoStreamer \
  testMPEG4VideoStreamer testWAVAudioStreamer testAMRAudioStreamer \
  testOnDemandRTSPServer vobStreamer openRTSP playSIP sapWatch
do
  install -p testProgs/$file %{buildroot}%{_bindir}/
done

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/live

%files utils
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/*

%changelog
* Thu Oct 11 2007 Josko Plazonic <plazonic@math.princeton.edu>
- update to 2007.08.03a

* Mon Mar 19 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2007.02.20-10
- Update to 2007.02.20.

* Sun Jan  8 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 2006.01.05.

* Fri Oct  1 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 2004.09.30.

* Sun Apr 11 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Updated to 2004.04.09.

* Tue Oct  7 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Updated to 2003.10.07.

* Mon Apr  7 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Rebuilt for Red Hat 9.

* Thu Jan 23 2003 Jeffrey C. Ollie <jcollie@pc04771.dmacc.cc.ia.us>
- Updated to 2003.01.17
- Added test utilities
- Reorganized and formed into subpackages
- Patched to remove deprecated header warnings
- Patched makefiles to use RPM optimization flags

* Mon Aug 12 2002 Jeffrey C. Ollie <jcollie@pc04771.dmacc.cc.ia.us>
- Initial build.
