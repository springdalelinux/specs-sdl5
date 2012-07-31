Name: 		aiksaurus
Version: 	1.2.1
Release: 	15%{?dist}
Summary: 	An English-language thesaurus library
Vendor:         Red Hat, Inc.

Epoch: 		1
Group: 		System Environment/Libraries
License: 	GPL
URL: 		http://aiksaurus.sourceforge.net/
Source0: 	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.png
Source2: 	%{name}.desktop
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: 	gtk2-devel
BuildRequires:	desktop-file-utils

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils


%description
Aiksaurus is an English-language thesaurus library that can be 
embedded in word processors, email composers, and other authoring
software to provide thesaurus capabilities.  A basic command line 
thesaurus program is also included.


%package devel
Requires: 	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary: 	Files for developing with aiksaurus
Group: 		Development/Libraries
 
                                                                               
%description devel
Includes and definitions for developing with aiksaurus.


%package gtk
Requires: 	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary: 	A GTK+ frontend to aiksaurus
Group: 		System Environment/Libraries


%description gtk
AiksaurusGTK is a GTK+ interface to the Aiksaurus library.  
It provides an attractive thesaurus interface, and can be embedded
in GTK+ projects, notably AbiWord.  A standalone thesaurus program
is also provided.


%package gtk-devel
Requires: 	%{name}-gtk = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: 	gtk2-devel
Summary: 	Files for developing with aiksaurus-gtk
Group: 		Development/Libraries
 
                                                                               
%description gtk-devel
gtk includes and definitions for developing with aiksaurus.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# Add the desktop icon.
%{__install} -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png

# Add desktop file.
desktop-file-install --vendor fedora                    \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --add-category X-Fedora                         \
        %{SOURCE2}

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%post gtk
/sbin/ldconfig
update-desktop-database &> /dev/null ||:


%postun gtk
/sbin/ldconfig
update-desktop-database &> /dev/null ||:


%files
%defattr(-, root, root)
%doc ChangeLog README COPYING AUTHORS
%{_bindir}/%{name}
%{_bindir}/caiksaurus
%{_libdir}/*Aiksaurus-*.so.*
%{_datadir}/%{name}/


%files devel
%defattr(-, root, root)
%dir %{_includedir}/Aiksaurus
%{_includedir}/Aiksaurus/Aiksaurus.h
%{_includedir}/Aiksaurus/AiksaurusC.h
%{_libdir}/*Aiksaurus.so
%{_libdir}/pkgconfig/%{name}-1.0.pc


%files gtk
%defattr(-, root, root)
%{_bindir}/gaiksaurus
%{_libdir}/*GTK*.so.*
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


%files gtk-devel
%defattr(-, root, root)
%{_includedir}/Aiksaurus/AiksaurusGTK*.h
%{_libdir}/*GTK*.so
%{_libdir}/pkgconfig/gaiksaurus-1.0.pc


%changelog
* Mon Sep 11 2006 Marc Maurer <uwog@uwog.net> - 1:1.2.1-15.fc6
- Add dist to the release version

* Tue Mar 28 2006 Marc Maurer <uwog@uwog.net> - 1:1.2.1-14
- Add Red Hat, Inc. as vendor

* Fri Feb 17 2006 Marc Maurer <uwog@uwog.net> - 1:1.2.1-13
- Fix buildrequires for aiksaurus-gtk-devel too

* Fri Feb 17 2006 Marc Maurer <uwog@uwog.net> - 1:1.2.1-12
- Fix buildrequires for aiksaurus-gtk and -devel

* Tue Jan 24 2006 Brian Pepple <bdpepple@ameritech.net> - 1:1.2.1-11
- Add desktop icon.
- Remove those pesky periods from the summaries.
- Add smp_mflag.
- Correct desktop file to meet FE requirements.
- Correct ownership of datadir.
- Correct sub-packages dependencies.
- Drop PreReq (depreciated), and use requires.
- Use preferred FE build root.

* Wed Aug 17 2005 Marc Maurer <uwog@abisource.com> 1:1.2.1-10
- Rebuild against new libcairo

* Fri Jul 8 2005 Marc Maurer <uwog@abisource.com> 1:1.2.1-9
- Add URL

* Sat Jun 25 2005 Colin Charles <colin@fedoraproject.org> 1:1.2.1-8
- Fix download URL

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1:1.2.1-7
- rebuild on all arches

* Thu Mar 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.2.1-6
- add dep gtk2-devel for pkgconfig in -gtk-devel sub-package 
- include %%{_includedir}/Aiksaurus dir in -devel sub-package
- remove redundant deps "gtk2" and "aiksaurus" in -gtk sub-package

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 1.2.1-5
- rebuild with gcc4

* Mon Jan 24 2005 Caolan McNamara <caolanm@redhat.com> 1.2.1-4
- RH#145922# wrong location

* Mon Jan 24 2005 Caolan McNamara <caolanm@redhat.com> 1.2.1-3
- RH#145922# make a .desktop for gaiksaurus

* Wed Oct 10 2004 Caolan McNamara <caolanm@redhat.com> 1.2.1-2
- #rh134808# BuildRequires gtk2-devel

* Tue Aug 10 2004 Caolan McNamara <caolanm@redhat.com>
- initially import 1.2.1 and tweak .spec
