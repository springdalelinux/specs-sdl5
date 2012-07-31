Name: 		ots
Summary: 	A text summarizer
Version: 	0.4.2
Release: 	10%{?dist}
License: 	GPL
URL:		http://libots.sourceforge.net/
Group: 		System Environment/Libraries
Source0: 	http://prdownloads.sourceforge.net/libots/ots-%{version}.tar.gz
Patch0: 	ots-0.4.2-gcc4.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: 	glib2 >= 2.0
BuildRequires: 	glib2-devel >= 2.0, libxml2-devel >= 2.4.23, pkgconfig >= 0.8

%description
The open text summarizer is an open source tool for summarizing texts.
The program reads a text and decides which sentences are important and
which are not.
 
%package devel
Summary: 	Libraries and include files for developing with libots.
Group: 		Development/Libraries
Requires: 	%{name} = %{version}
Requires: 	pkgconfig >= 0.8, glib2 >= 2.0, glib2-devel >= 2.0

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with libots.

%prep
%setup -q 
%patch0 -p1 -b .gcc4

%build

%configure --disable-gtk-doc \
	--with-html-dir=%{buildroot}%{_datadir}/gtk-doc/html/ots
make

%install
rm -rf %{buildroot}
%makeinstall
# Currently, ots generates empty API docs.
rm -rf %{buildroot}/%{_datadir}/gtk-doc
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/ots
%{_libdir}/*.so.*
%{_mandir}/*/*
%{_datadir}/ots

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/libots-1
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-10
- Rebuild for FC6

* Sun May 21 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-9
- rebuild and spec tidy

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.4.2-7
- rebuild on all arches

* Wed Mar 16 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.2-5
- Reenable man page.
- Disable rebuilding documentation via configure switch instead of an automake
  requiring patch.
- Remove the API documentation for now as it is just a placeholder.

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> - 0.4.2-4
- rebuild with gcc4
- small lvalue assign patch

* Wed Feb 09 2005 Caolan McNamara <caolanm@redhat.com> - 0.4.2-3
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Jeremy Katz <katzj@redhat.com> - 0.4.2-1
- 0.4.2

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Jeremy Katz <katzj@redhat.com> 
- add some buildrequires (#111158)

* Mon Sep 15 2003 Jeremy Katz <katzj@redhat.com> 0.4.1-1
- 0.4.1

* Mon Aug  4 2003 Jeremy Katz <katzj@redhat.com> 0.4.0-1
- 0.4.0

* Tue Jul 22 2003 Jeremy Katz <katzj@redhat.com> 0.3.0-1
- update to 0.3.0

* Sat Jul 12 2003 Jeremy Katz <katzj@redhat.com> 0.2.0-2
- forcibly disable gtk-doc (openjade is busted on s390)

* Mon Jul  7 2003 Jeremy Katz <katzj@redhat.com> 0.2.0-1
- update to 0.2.0
- ldconfig in %%post/%%postun
- libtoolize
- clean up spec file a little, build gtk-doc
- fix libtool versioning 

* Thu Jun 05 2003 Rui Miguel Silva Seabra <rms@1407.org>
- fix spec
- disable gtk-doc (it's not building in RH 9,
  maybe it's broken for some reason)

* Fri May 02 2003 Rui Miguel Silva Seabra <rms@1407.org>
- define a longer description from the README file
- explicitly set file permissions

* Wed Apr 30 2003 Dom Lachowicz <cinamod@hotmail.com>
- created this thing
