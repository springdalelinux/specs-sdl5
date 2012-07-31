%define name         w32codec
%define version      20060611
%define release      2%{?dist}

%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define __os_install_post %{nil}

Name:           %name
Summary:        Win32-Codecs
License:        unknown
Group:          Misc
URL:            http://mplayerhq.hu/MPlayer/releases/codecs/
Version:        %{version}
Release:        %{release}

Source0:        all-%{version}.tar.bz2

Packager:       Manfred Tremmel <Manfred.Tremmel@iiv.de>
Vendor:         Packman
BuildRoot:      /var/tmp/%{name}-%{version}-%{release}
Prefix:         %{_prefix}
Obsoletes:      win32-codecs, win32codecs
Provides:       win32-codecs, win32codecs

%description
Win32 DLLs for decompression of AVI- and also Quicktime-movies.
Contains the dlls from the "all" package.

%prep

#%setup -n win32codecs-%{version} -q -a 1 -a 2
%setup -n all-%{version}

%build

%install
[ "$RPM_BUILD_ROOT" = "/var/tmp/%{name}-%{version}-%{release}" ] && rm -rf $RPM_BUILD_ROOT;
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/codecs
cp *.* $RPM_BUILD_ROOT%{prefix}/lib/codecs
#cd qt63dlls-%{version}
#cp *.* $RPM_BUILD_ROOT%{prefix}/lib/win32/
#cd ../qtextras-%{version}
#cp *.* $RPM_BUILD_ROOT%{prefix}/lib/win32/
cd $RPM_BUILD_ROOT%{prefix}/lib
ln -s codecs win32

%clean
[ "$RPM_BUILD_ROOT" = "/var/tmp/%{name}-%{version}-%{release}" ] && rm -rf $RPM_BUILD_ROOT;

%files
%defattr(644, root, root,755)
%{prefix}/lib/win32
%dir %{prefix}/lib/codecs
%{prefix}/lib/codecs/*

%changelog
* Mon Nov 08 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- update to the latest codecs (20041107)
* Fri Sep 17 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- update to the latest codecs (20040916)
* Thu Jul 07 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- update to the latest codecs (20040706)
* Sun Jul 04 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- update to the latest codecs (20040704)
- switched to "all" package, makes it easier ;-)
* Sun Jun 27 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- update to the latest codecs
- new versions, using the package date
* Wed Jun 02 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- removed rp9 (it's not used by MPlayer or xine)
- update to the latest codecs
* Sat Apr 12 2003 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- added packman build header
* Fri Feb 07 2003 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- Updated of the DLL-Packages
* Wed Dec 25 2002 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- Updated version to 0.90
* Sun May 05 2002 Henne Vogelsang <henne@links2linux.de>
- Updated version to 0.60
* Sat Nov 10 2001 Waldemar Brodkorb <waldemar@links2linux.de>
- fixed permissions of some codecs
* Sun Oct 28 2001 Waldemar Brodkorb <waldemar@links2linux.de>
- more dll's found on mplayer-homepage
* Sun Oct 14 2001 Waldemar Brodkorb <waldemar@links2linux.de>
- minor spec enhancements
* Wed Jan 31 2001 Waldemar Brodkorb <waldemar@links2linux.de>
- new upstream, more codecs
* Tue Jan 23 2001 Waldemar Brodkorb <waldemar@links2linux.de>
- first release
