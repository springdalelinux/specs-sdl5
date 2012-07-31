Name:           autotrace
Version:        0.31.1
Release:        25%{?dist}

Summary:        Utility for converting bitmaps to vector graphics

Group:          Applications/Multimedia
License:        GPLv2+ and LGPLv2+
URL:            http://autotrace.sourceforge.net/
Source0:        http://dl.sf.net/autotrace/autotrace-0.31.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ImageMagick-devel
BuildRequires:  libpng-devel > 2:1.2
BuildRequires:  libexif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  bzip2-devel
BuildRequires:  freetype-devel
#BuildRequires:  pstoedit-devel
BuildConflicts: pstoedit-devel

Patch0:         autotrace-0.31.1-GetOnePixel.patch
Patch1:         autotrace-aclocal18.patch

%description
AutoTrace is a program for converting bitmaps to vector graphics.

Supported input formats include BMP, TGA, PNM, PPM, and any format
supported by ImageMagick, whereas output can be produced in
Postscript, SVG, xfig, SWF, and others.

%package devel
Summary:        Header files and static libraries for autotrace
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ImageMagick-devel
#Requires:       pstoedit-devel


%description devel
This package contains header files and static libraries for autotrace.


%prep
%setup -q
%patch0 -p1 -b .GetOnePixel
%patch1 -p0 -b .aclocal18

%build
%configure

# Remove RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB ChangeLog FAQ NEWS README THANKS TODO
%{_bindir}/autotrace
%{_libdir}/*.so.*
%{_mandir}/man[^3]/*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_bindir}/autotrace-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/autotrace/
%{_datadir}/aclocal/*.m4


%changelog
* Mon May 17 2010 Radek Vokal <rvokal@redhat.com> - 0.31.1-25
- fix the description
- Resolves: #591669

* Thu Feb 25 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 0.31.1-24
- Fixed rpmlint RPATH warning

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.31.1-23.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-23
- Removed static libraries from -devel
- Changed %%makeinstall to "make install DESTDIR=blablabla"
- Fixed rhbz# 477980

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Hans de Goede <hdegoede@redhat.com> - 0.31.1-21
- Rebuild for new ImageMagick

* Mon Mar 02 2009 Caolán McNamara <caolanm@redhat.com> - 0.31.1-20
- Modify GetOnePixel usage to build against current ImageMagick api

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.31.1-18
- fix license tag

* Mon May 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.31.1-17
- Rebuild for new ImageMagick.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.31.1-16
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Quentin Spencer <qspencer@users.sourceforge.net> - 0.31.1-15
- Rebuild for F8.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.31.1-14
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Quentin Spencer <qspencer@users.sourceforge.net> - 0.31.1-13
- Rebuild for FC6.

* Mon Feb 13 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-12
- Rebuild for Fedora Extras 5

* Sat Jan 28 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-11
- rebuild

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-10
- add BuildRequires on freetype-devel

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-9
- remove BuildRequires on XFree86-devel

* Mon Jan 16 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-8
- add %%{?dist} tag
- add a BuildRequires on bzip2-devel
- add ldconfig to %%post and %%postun

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-7
- and more buildrequires

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-6
- BR libtiff-devel

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-5
- rebuild

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Aug 21 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.31.1-3
- Temporarily changed buildreq pstoedit-devel to buildconflicts.

* Thu Apr 22 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.31.1-0.fdr.2
- Added new BuildReq pstoedit-devel.
- Added missing BuildReq libexif-devel.
- Added missing -devel requires pkgconfig, ImageMagick-devel.
- Converted spec file to UTF-8.

* Mon Sep 29 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:0.31.1-0.fdr.1
- Initial RPM release.

