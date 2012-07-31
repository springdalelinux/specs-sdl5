# $Id: libdvdcss.spec,v 1.9 2003/03/11 11:15:58 dude Exp $

Summary: A portable abstraction library for DVD decryption.
Name: libdvdcss
Version: 1.2.9
Release: 3%{?dist}
Epoch: 1
License: GPL
Group: System Environment/Libraries
Source: http://www.videolan.org/pub/videolan/libdvdcss/%{version}/libdvdcss-%{version}.tar.bz2
URL: http://www.videolan.org/libdvdcss/
BuildRoot: %{_tmppath}/%{name}-root

%description
This is a portable abstraction library for DVD decryption which is used by
the VideoLAN project, a full MPEG2 client/server solution.  You will need
to install this package in order to have encrypted DVD playback with the
VideoLAN client and the Xine navigation plugin.


%package devel
Summary: Development files from the libdvdcss DVD decryption library.
Group: Development/Libraries
Requires: %{name} = 1:%{version}

%description devel
This is a portable abstraction library for DVD decryption which is used by
the VideoLAN project, a full MPEG2 client/server solution.  You will need
to install this package in order to have encrypted DVD playback with the
VideoLAN client and the Xine navigation plugin.

You will need to install these development files if you intend to rebuild
any of the above programs.


%prep
%setup -q

%build
./bootstrap
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
mkdir %{buildroot}%{_bindir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README NEWS
%{_libdir}/%{name}.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/dvdcss
%exclude %{_libdir}/%{name}.la
%{_libdir}/%{name}.so

%changelog
* Sun Apr 1 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for 5 and drop static lib

* Fri May 16 2003 Josko Plazonic <plazonic@math.princeton.edu>
- repackaged it without network support

* Wed Apr 2 2003 Miguel Freitas <miguel@cetuc.puc-rio.br>
- fixed location of dvdcss_server

* Fri Mar 28 2003 Miguel Freitas <miguel@cetuc.puc-rio.br>
- added network patch (can play dvds across the network)
  server: dvdcss_server <dvd_device> <port>
  client: player dvd:/<server_address>:<port>/

* Tue Mar 11 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.6.

* Mon Feb  3 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.5.

* Fri Nov 15 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.4.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.3.

* Thu Sep 26 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 8.0.

* Mon Aug 12 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.2.

* Mon Jun  3 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.1.

* Fri May 24 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.0.

* Thu May  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Mon Apr  8 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.1.1.

* Sun Nov  4 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Changed to the Ogle patched version of the lib.

* Mon Oct 22 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
- Decided to put libdvdcss in a separate package since both videolan and the
  xine DVD menu plugin use it.

