
# cvsadmin: http://bugzilla.redhat.com/418271

Name:       taglib	
Version:    1.5
Release:    2%{?dist}
Summary:    Audio Meta-Data Library

Group: 	    System Environment/Libraries
License:    LGPLv2
URL:        http://developer.kde.org/~wheeler/taglib.html
Source0:    http://developer.kde.org/~wheeler/files/src/taglib-%{version}.tar.gz
#Source0:    taglib-%{svn}.tar.gz
# The svn tarball is generated with the following script
Source1:    taglib-svn.sh
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# http://bugzilla.redhat.com/343241
# try 1, use pkg-config
Patch1:     taglib-1.5b1-multilib.patch 
# try 2, kiss omit -L%_libdir
Patch2:     taglib-1.5rc1-multilib.patch

## upstream patches
Patch100: taglib-1.5-kde#161721.patch

BuildRequires: cmake
BuildRequires: zlib-devel

%description
TagLib is a library for reading and editing the meta-data of several
popular audio formats. Currently it supports both ID3v1 and ID3v2 for
MP3 files, Ogg Vorbis comments and ID3 tags and Vorbis comments in
FLAC files.

%package devel
Summary: Development files for %{name} 
Group:	 Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
%{summary}.


%prep
%setup -q -n taglib-%{version}%{?beta}

%patch2 -p1 -b .multilib

%patch100 -p1 -b .kde#161721.patch


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} -C %{_target_platform}

rm -fr examples/.deps
rm -fr examples/Makefile*
rm -f %{buildroot}%{_libdir}/lib*.la


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LGPL
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples
%{_bindir}/*-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Oct 06 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-2
- Encrypted frames taglib/Amarok crash (kde#161721)

* Wed Feb 20 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-1
- taglib-1.5

* Wed Feb 13 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-0.9.rc1
- taglib-1.5rc1
- omit taglib-1.4_wchar.diff (for now)

* Mon Feb 04 2008 Rex Dieter <rdieter@fedoraproject.org> 1.5-0.8.b1
- taglib-1.5b1

* Wed Jan 16 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.7.20080116svn
- svn20080116 snapshot
- multiarch conflicts (#343241)

* Sun Nov 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.6.20071111svn
- svn20071111 snapshot (#376241)

* Thu Sep 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.5.20070924svn
- -BR: automake 
- +BR: zlib-devel

* Thu Sep 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.5-0.4.20070924svn
- use cmake, fixes "taglib_export.h not included" (#272361#c7)

* Mon Sep 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.5-0.3.20070924svn
- rebuild

* Mon Sep 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.5-0.2.20070924svn
- BR: automake

* Mon Sep 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.5-0.1.20070924svn
- update to svn version

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.4-6
- fix license tag
- rebuild for BuildID

* Thu Dec 14 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4-5
- add patch for multi-language support

* Thu Sep 14 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4-4
- have the devel package require pkgconfig (#206443)

* Thu Aug 31 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4-3
- rebuild

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.4-2
- rebuild for FC5

* Mon Aug 01 2005 Aurelien Bompard <gauret[AT]free.fr> 1.4-1
- version 1.4

* Fri Mar 25 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.3.1-2
- rebuild with g++4

* Mon Jan 10 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.3.1-1
- version 1.3.1
- drop patch0
- don't nuke every .la files, only the useless ones
- spec improvements thanks to Rex Dieter

* Thu Nov 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.3-0.fdr.2
- add apeitem.h to the include files in -devel

* Mon Oct 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.3-0.fdr.1
- version 1.3

* Sun Jun 06 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.5
- Changed license to LGPL
- include examples only in -devel
- remove Makefile* from examples
- remove *.la files

* Fri Jun 04 2004 Mihai Maties <mihai[AT]xcyb.org> 0:1.1-0.fdr.4
- included .la files as well
- compiled doc and included in -devel
- included examples in -devel

* Thu Jun 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.3
- provide the libtool files in the -devel subpackage
- include exemples in doc

* Thu Jun 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.2
- remove empty README
- add Requires(post,postun): /sbin/ldconfig
- remove --disable-static, it was useless anyway

* Tue Jun 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1-0.fdr.1
- Fedora submission (shamelessly borrowed from Rex -- kde-redhat.sf.net)

* Sun Apr 04 2004 Rex Dieter <rexdieter at sf.net> 0:1.1-0.fdr.1
- 1.1

* Thu Feb 12 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.1
- fix for rh73

* Fri Feb 06 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.0
- first try
