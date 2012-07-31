%bcond_with static

%define	xmms_plugdir %(xmms-config --general-plugin-dir 2>/dev/null)

Name:           xosd
Version:        2.2.14
Release:        9%{?dist}
Summary:        On-screen display library for X

Group:          System Environment/Libraries
License:        GPL
URL:            http://www.ignavus.net/software.html
Source:         http://ftp.debian.org/debian/pool/main/x/xosd/%{name}_%{version}.orig.tar.gz
Patch0:         %{name}-aclocal18.patch
Patch1:         %{name}-defaults.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
# As of 2.2.14, the default font *must* be found, even if not used (#183971)
Requires:       xorg-x11-fonts-base

%description
XOSD displays text on your screen, sounds simple right? The difference
is it is unmanaged and shaped, so it appears transparent. This gives
the effect of an On Screen Display, like your TV/VCR etc.. The package
also includes an xmms plugin, which automatically displays various
interesting things as they change (song name, volume etc...)

%package        devel
Summary:        Development files for the XOSD on-screen display library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXinerama-devel

%description    devel
The xosd-devel package contains static libraries, header files and
documentation for developing applications that use the XOSD on-screen
display.

%package     -n xmms-%{name}
Summary:        XMMS plugin for on-screen display using the XOSD library
Group:          Applications/Multimedia
BuildRequires:  gtk+-devel >= 1:1.2.2
BuildRequires:  gdk-pixbuf-devel >= 1:0.22.0
BuildRequires:  xmms-devel
Requires:       %{name} = %{version}-%{release}
Requires:       xmms
Obsoletes:      %{name}-xmms <= 2.2.12

%description -n xmms-%{name}
X MultiMedia System plugin to display information on-screen through
the XOSD library, similarly to TV OSD.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
for f in ChangeLog man/xosd_{create,destroy,display,is_onscreen,set_bar_length}.3 ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done


%build
%configure --disable-dependency-tracking %{!?with_static:--disable-static}
make %{?_smp_mflags}
%{__perl} -pi -e "s|$RPM_OPT_FLAGS\\s*|| ; s|\\s*-Wall||" script/xosd-config


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT{%{_libdir},%{xmms_plugdir}}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/osd_cat
%{_libdir}/libxosd.so.*
%{_datadir}/xosd/
%{_mandir}/man1/osd_cat.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/xosd-config
%{_includedir}/xosd.h
%{_libdir}/libxosd.so
%if %{with static}
%{_libdir}/libxosd.a
%endif
%{_datadir}/aclocal/libxosd.m4
%{_mandir}/man1/xosd-config.1*
%{_mandir}/man3/xosd*.3*

%files -n xmms-%{name}
%defattr(-,root,root,-)
%{xmms_plugdir}/libxmms_osd.so

%changelog
* Tue Feb 27 2007 Kevin Fenzi <kevin@tummy.com> - 2.2.14-9
- Remove bmp subpackage, as bmp is no longer shipped. 

* Sun Aug 27 2006 Kevin Fenzi <kevin@tummy.com> - 2.2.14-8
- Rebuild for fc6

* Fri Jun 16 2006 Kevin Fenzi <kevin@tummy.com> - 2.2.14-7
- Rebuild against new libgdk_pixbuf

* Wed Apr 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.2.14-6
- Revert to upstream default font, require xorg-x11-fonts-base (#183971).

* Sun Mar 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.2.14-5
- Convert docs to UTF-8.

* Thu Nov 17 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2.14-4
- Adapt to modular X packaging.
- Don't ship static libraries by default.
- Specfile cleanups.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2.14-3
- Rebuild.

* Thu Mar 17 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.2.14-2
- Add Beep Media Player plugin subpackage.
- Improve default font and plugin OSD placement.

* Mon Nov 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 2.2.14-1
- Update to 2.2.14 (from Debian).
- Drop pre-FC1 gdk-pixbuf compatibility kludges.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.2.12-2
- Bump release to provide Extras upgrade path.
- Remove zero epochs.

* Tue Sep 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.12-0.fdr.1
- Update to 2.2.12.
- Disable dependency tracking to speed up the build.
- Include TODO in docs.

* Sun Sep 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.11-0.fdr.1
- Update to 2.2.11 (from Debian).
- While at it, borrow patches from Debian's 2.2.11-2.

* Sat Aug 28 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.10-0.fdr.1
- Update to 2.2.10.
- Patch to eliminate aclocal >= 1.8 warnings from libxosd.m4.

* Mon Jul  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.8-0.fdr.1
- Update to 2.2.8.

* Tue May 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.7-0.fdr.1
- Update to 2.2.7.

* Wed May 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.5-0.fdr.2
- Clean up "xosd-config --cflags".

* Sat Sep 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.5-0.fdr.1
- Update to 2.2.5.

* Mon Jun 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.2-0.fdr.1
- Update to 2.2.2.

* Sat Apr 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.1-0.fdr.1
- Update to 2.2.1.
- Disable gdk-pixbuf test, XOSD says it requires >= 0.22.0, but 0.18.0
  seems to work just fine.

* Sun Apr 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.0-0.fdr.1
- Update to 2.2.0.
- Rename XMMS plugin package to xmms-xosd, and obsolete xosd-xmms.

* Mon Apr  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1.3-0.fdr.3
- Require XFree86-devel in -devel (xosd-config --libs).

* Sat Apr  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1.3-0.fdr.2
- Add epoch to devel and xmms Requires (#30 comment 4).
- Don't include *.la in xmms package.
- Save .spec in UTF-8.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.1.3-0.fdr.1
- Update to 2.1.3 and current Fedora guidelines.
- Don't include %%{_libdir}/*.la.

* Wed Feb 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 2.1.2-1.fedora.1
- Update to 2.1.2.
- Use %%post(un) -p /sbin/ldconfig.

* Sat Feb  8 2003 Ville Skyttä <ville.skytta at iki.fi> - 2.1.0-1.fedora.1
- First Fedora release, based on Matthias Saou's work.

* Wed Feb  5 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 2.1.0.
- Spec file updates to reflect upstream changes.

* Wed Jan  8 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 2.0.1.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.1.1.

* Sun Sep 29 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.0.4.
- Rebuilt for Red Hat Linux 8.0.

* Fri Aug 30 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.0.3.

* Wed Aug 28 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.0.2.
- Fixed %%defattr for xmms plugin sub-package.

* Mon Jul 22 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.0.0.
- Spec file cleanup (near rewrite), added devel and xmms sub-packages.

* Wed Aug  1 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.7.0 and spec file cleanup.
- Changed the plugin path.
- Added ldconfig execution since I also changed the lib filename.

* Sat Feb  3 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.

