%if %{?el5}0
%define with_libvoikko  %{?_with_libvoikko:    1} %{?!_with_libvoikko:    0}
%define with_hunspell   %{?_with_hunspell:     1} %{?!_with_hunspell:     0}
%else
%define with_libvoikko  %{?_without_libvoikko: 0} %{?!_without_libvoikko: 1}
%define with_hunspell   %{?_without_hunspell:  0} %{?!_without_hunspell:  1}
%endif

Summary: An Enchanting Spell Checking Library
Name: enchant
Version: 1.4.2
Release: 4%{?dist}.1
Epoch: 1
Group: System Environment/Libraries
License: LGPLv2+
Source: http://www.abisource.com/downloads/enchant/%{version}/enchant-%{version}.tar.gz
URL: http://www.abisource.com/
BuildRequires: glib2-devel >= 2.6.0
BuildRequires: aspell-devel
# BuildRequires: hspell-devel
%if %{with_hunspell}
BuildRequires: hunspell-devel
%endif
%if %{with_libvoikko}
BuildRequires: libvoikko-devel
%endif
BuildRequires: automake, libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
A library that wraps other spell checking backends.

%package aspell
Summary: Integration with aspell for libenchant
Group: System Environment/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}

%description aspell
Libraries necessary to integrate applications using libenchant with aspell.

%if %{with_libvoikko}
%package voikko
Summary: Integration with voikko for libenchant
Group: System Environment/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}

%description voikko
Libraries necessary to integrate applications using libenchant with voikko.
%endif


%package devel
Summary: Support files necessary to compile applications with libenchant.
Group: Development/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}
Requires: glib2-devel

%description devel
Libraries, headers, and support files necessary to compile applications using libenchant.

%prep
%setup -q

%build
%configure --disable-ispell --with-myspell-dir=/usr/share/myspell --disable-hspell --disable-static \
  --disable-zemberek \
%if ! %{with_hunspell}
  --disable-hunspell \
%endif
%if ! %{with_libvoikko}
  --disable-libvoikko \
%endif
  --
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/enchant/*.la

%files
%defattr(-,root,root)
%doc AUTHORS COPYING.LIB README
%{_bindir}/*
%{_libdir}/lib*.so.*
%dir %{_libdir}/enchant
# %{_libdir}/enchant/lib*hspell.so*
%{_libdir}/enchant/lib*myspell.so*
%{_mandir}/man1/enchant.1.gz
%{_datadir}/enchant

%files aspell
%{_libdir}/enchant/lib*aspell.so*

%if %{with_libvoikko}
%files voikko
%defattr(-,root,root)
%{_libdir}/enchant/lib*_voikko.so*
%endif

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/enchant.pc
%{_includedir}/enchant

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Fri Oct 3 2008 Lubomir Rintel <lkundrak@v3.sk> 1:1.4.2-4.1
- Make libvoikko and hunspell support optional and disabled for el5

* Sat Jul 26 2008 Michael Schwendt <mschwendt@fedoraproject.org> 1:1.4.2-4
- Rebuild for ABI-incompatible hunspell-1.2.4.2-2.fc10

* Thu Jul 10 2008 Marc Maurer <uwog@abisource.com> 1:1.4.2-3
- Fix 426712: don't build static libs (patch from Michael Schwendt)

* Wed May 21 2008 Marc Maurer <uwog@abisource.com> 1:1.4.2-2
- Rebuild

* Wed May 21 2008 Marc Maurer <uwog@abisource.com> 1:1.4.2-1
- New upstream release
- Add voikko support in an enchant-voikko package
- Bump glib-devel BR to 2.6.0

* Fri Feb 08 2008 Caolan McNamara <caolanm@redhat.com> 1:1.3.0-4.fc9
- minor cockup

* Sat Jan 26 2008 Caolan McNamara <caolanm@redhat.com> 1:1.3.0-3.fc9
- Resolves: rhbz#426402 use system hunspell not internal one and 
  split out aspell backend.
- See: rhbz#430354 hspell backend disabled until pic issue fixed

* Wed Dec 19 2007 Caolan McNamara <caolanm@redhat.com> 1:1.3.0-2.fc9
- tell enchant where the myspell dictionaries are

* Thu Oct 12 2006 Marc Maurer <uwog@abisource.com> 1:1.3.0-1.fc6
- Update to 1.3.0

* Mon Sep 11 2006 Marc Maurer <uwog@abisource.com> 1:1.2.5-3.fc6
- Rebuild for FC6

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 1:1.2.5-2.fc6
- Rebuild

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 1:1.2.5-1.fc6
- Package the data dir as well (bug 188516)
- New upstream version
- Add hspell requirement/support

* Tue Feb 14 2006 Marc Maurer <uwog@abisource.com> 1:1.2.2-2.fc5
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Marc Maurer <uwog@abisource.com> 1:1.2.2-1.fc5
- Update to 1.2.2

* Mon Jan 30 2006 Marc Maurer <uwog@abisource.com> 1:1.2.1-1.fc5
- Update to 1.2.1
- Drop glib Require

* Sat Oct 22 2005 Marc Maurer <uwog@abisource.com> 1:1.2.0-1.fc5
- Update to 1.2.0

* Wed Oct  5 2005 Marc Maurer <uwog@abisource.com> 1:1.1.6-4.fc5
- Add dist flag to the release number

* Mon Apr  4 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1:1.1.6-3
- make in %%build
- disable bad buildroot rpaths in libs, don't use %%makeinstall
- require %%{epoch} of main package in -devel package (Fridrich Strba)

* Thu Mar 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1:1.1.6-2
- add dep glib2-devel for pkgconfig in -devel package
- include %%{_libdir}/enchant dir in main package
- make -devel package require exact VR of main package
- use -p /sbin/ldconfig in scriptlets

* Mon Mar 28 2005 Marc Maurer <uwog@abisource.com> 1:1.1.6-1
- update to 1.1.6
- drop the manpage patch (RH#145010#)
- fix version numbers in the spec changelog

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.1.5-3
- rebuild with gcc4

* Fri Jan 14 2005 Caolan McNamara <caolanm@redhat.com> 1:1.1.5-2
- RH#145010# misformatted manpage

* Mon Dec 20 2004 Caolan McNamara <caolanm@redhat.com> 1:1.1.5-1
- initial fedora import

* Sun Aug 24 2003 Rui Miguel Seabra <rms@1407.org>
- update spec to current stat of affairs
- building from source rpm is now aware of --with and --without flags:
- --without aspell --without ispell --without myspell --with uspell

* Wed Jul 16 2003 Rui Miguel Seabra <rms@1407.org>
- take advantage of environment rpm macros

* Sun Jul 13 2003 Dom Lachowicz <cinamod@hotmail.com>
- Initial version
