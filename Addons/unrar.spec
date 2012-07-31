# $Id: unrar.spec 5224 2007-03-07 15:21:36Z thias $
# Authority: matthias
# Upstream: <dev$rarlab,com>

Summary: Extract, test and view RAR archives
Name: unrar
Version: 3.7.8
Release: 1%{?dist}
License: Freeware
Group: Applications/Archiving
URL: http://www.rarlab.com/
Source0: http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz
Source1: unrar.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++

%description
The unRAR utility is a freeware program, distributed with source code
and developed for extracting, testing and viewing the contents of
archives created with the RAR archiver version 1.50 and above.


%prep
%setup -n %{name}
# Remove stripping to get useful debuginfo package
%{__perl} -pi -e 's|^STRIP=.*|STRIP=true|g' makefile.unix


%build
%{__make} %{?_smp_mflags} -f makefile.unix CXXFLAGS="%{optflags}"


%install
%{__rm} -rf %{buildroot}
%{__install} -D -m755 unrar %{buildroot}%{_bindir}/unrar
%{__install} -D -p -m644 %{SOURCE1} %{buildroot}%{_mandir}/man1/unrar.1


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc *.txt
%{_bindir}/unrar
%{_mandir}/man1/unrar.1*


%changelog
* Wed Mar  7 2007 Matthias Saou <http://freshrpms.net/> 3.7.4-1
- Update to 3.7.4.

* Thu Sep 14 2006 Matthias Saou <http://freshrpms.net/> 3.6.8-1
- Update to 3.6.8.

* Wed Apr 19 2006 Matthias Saou <http://freshrpms.net/> 3.6.2-1
- Update to 3.6.2.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 3.5.4-2
- Release bump to drop the disttag number in FC5 build.

* Fri Oct 14 2005 Matthias Saou <http://freshrpms.net/> 3.5.4-1
- Update to 3.5.4.

* Sun Jun  5 2005 Matthias Saou <http://freshrpms.net/> 3.5.2-1
- Update to 3.5.2.
- Disable stripping to get useful debuginfo package.

* Mon Apr  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.1-1
- Update to 3.5.1.

* Tue Nov  2 2004 Matthias Saou <http://freshrpms.net/> 3.4.3-1
- Update to 3.4.3.

* Thu Feb 26 2004 Matthias Saou <http://freshrpms.net/> 3.3.6-1
- Update to 3.3.6.

* Mon Jan 19 2004 Matthias Saou <http://freshrpms.net/> 3.3.4-1
- Update to 3.3.4.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 3.2.3-1
- Update to 3.2.3.
- Rebuild for Fedora Core 1.

* Wed May 14 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.2.1.
- Added missing URL.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.2.0.
- Rebuilt for Red Hat Linux 9.

* Mon Jan 13 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.1.3.

* Thu Oct 10 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup.

* Sat Oct  5 2002 Ville Skyttä <ville.skytta at iki.fi> 3.00-2cr
- Rebuild for Red Hat 8.0, using the compat GCC.

* Tue Sep 17 2002 Ville Skyttä <ville.skytta at iki.fi> 3.00-1cr
- RedHatified PLD version.

