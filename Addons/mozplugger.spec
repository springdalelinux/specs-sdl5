Summary: A generic mozilla plug-in
Name: mozplugger
Version: 1.8.0
Release: 3.2%{?dist}
License: GPL
Group: Applications/Internet
Url: http://mozplugger.mozdev.org/

Source0: http://mozplugger.mozdev.org/mozplugger/%{name}-%{version}.tar.gz
Patch1: mozplugger-1.5.0-lib64.patch
Patch2: mozplugger-1.8.0-config.patch

Requires: sox
BuildPrereq: libX11-devel
BuildPrereq: libXt-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: plugger

%description
MozPlugger is a generic Mozilla plug-in that allows the use of standard Linux
programs as plug-ins for media types on the Internet.

%prep
%setup -q
%patch1 -p1 -b .lib64
%patch2 -p1 -b .config

%build
make linux lib=%{_lib}

%install
rm -rf %{buildroot}
make install lib=%{_lib} root=%{buildroot}

file=%{buildroot}%{_mandir}/man7/mozplugger.7
#bunzip2 "$file.bz2"
iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
mv "${file}_" "$file"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COPYING
%config /etc/mozpluggerrc
%{_bindir}/*
%{_libdir}/mozilla
%{_mandir}/man7/mozplugger.7*

%changelog
* Mon Apr  9 2007 Josko Plazonic <plazonic@math.princeton.edu>
- drop default support for various multimedia things and pdf,
  we have other plugins to handle those

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7.3-3.1
- rebuild

* Tue May 16 2006 Than Ngo <than@redhat.com> 1.7.3-3 
- fix #191969, Missing BuildRequire on libXt-devel
- adjust mozpluggerc for FC
 
* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.7.3-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.7.3-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 08 2005 Than Ngo <than@redhat.com> 1.7.3-2 
- get rid of xorg-x11-devel, fix for modular X

* Fri Oct 14 2005 Florian La Roche <laroche@redhat.com>
- update to 1.7.3

* Mon Apr  4 2005 Elliot Lee <sopwith@redhat.com> - 1.7.1-4
- Remove mikmod dep

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 1.7.1-3
- rebuild

* Thu Feb 03 2005 Than Ngo <than@redhat.com> 1.7.1-2
- drop xloadimage dependency

* Thu Jan 20 2005 Than Ngo <than@redhat.com> 1.7.1-1
- update to 1.7.1
- remove mozplugger-1.6-2-ia64.patch, it's included in new upstream

* Mon Dec 06 2004 Than Ngo <than@redhat.com> 1.6.2-4
- add fix for ia64
- enable s390 s390x build

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> - 1.6.2-3
- Convert man page to UTF-8

* Fri Oct 29 2004 Than Ngo <than@redhat.com> 1.6.2-2
- add missing Buildprereq on XFree86-devel #137564

* Tue Sep 28 2004 Than Ngo <than@redhat.com> 1.6.2-1
- update to 1.6.2
- get rid of requires mozilla

* Tue Aug 31 2004 Than Ngo <than@redhat.com> 1.6.1-1
- update to 1.6.1

* Sun Jul 25 2004 Than Ngo <than@redhat.com> 1.6.0-1
- update to 1.6.0
- fix broken deps 

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 07 2004 Than Ngo <than@redhat.com> 1.5.2-1
- update to 1.5.2, fix #117424
- remove mozplugger-1.5.0.patch that included in upstream

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Than Ngo <than@redhat.com> 1.5.0-3 
- drop mozplugger-1.1.3-redhat.patch, it's included in new upstream
- add patch file to fix swallow issue, thanks to Louis Bavoil

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 16 2004 Than Ngo <than@redhat.com> 1.5.0-1
- 1.5.0

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1.3.2-1
- 1.3.2

* Thu Sep 04 2003 Than Ngo <than@redhat.com> 1.3.1-1
- 1.3.1

* Wed May  7 2003 Than Ngo <than@redhat.com> 1.1.3-1
- initial build
