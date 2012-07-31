Summary: A MathML rendering library
Name: gtkmathview
Version: 0.7.6
Release: 5%{?dist}
Group: System Environment/Libraries
License: GPL
Source: http://helm.cs.unibo.it/mml-widget/sources/gtkmathview-%{version}.tar.gz
URL: http://helm.cs.unibo.it/mml-widget/
BuildRequires: glib2-devel >= 2.2
BuildRequires: gtk2-devel >= 2.2
BuildRequires: libxml2-devel >= 2.6.7
BuildRequires: libxslt >= 1.0.32
BuildRequires: popt >= 1.7 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GtkMathView is a C++ rendering engine for MathML documents. 
It provides an interactive view that can be used for browsing 
and editing MathML markup.

%package devel
Summary: Support files necessary to compile applications using gtkmathview
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= 2.2.1
Requires: gtk2-devel >= 2.2.1
Requires: libxml2-devel >= 2.6.7
Requires: popt >= 1.7.0 
Requires: pkgconfig

%description devel
Libraries, headers, and support files needed for using gtkmathview.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/mathml2ps.1
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/mathmlviewer.1

%files
%defattr(-,root,root)
%doc COPYING README AUTHORS CONTRIBUTORS BUGS LICENSE
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_sysconfdir}/gtkmathview/
%{_datadir}/gtkmathview/

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/mathview-core.pc
%{_libdir}/pkgconfig/mathview-frontend-libxml2.pc
%{_libdir}/pkgconfig/gtkmathview-custom-reader.pc
%{_libdir}/pkgconfig/gtkmathview-libxml2-reader.pc
%{_libdir}/pkgconfig/gtkmathview-libxml2.pc
%{_libdir}/pkgconfig/mathview-frontend-libxml2-reader.pc
%{_libdir}/pkgconfig/mathview-frontend-custom-reader.pc
%{_libdir}/pkgconfig/mathview-backend-svg.pc
%{_libdir}/pkgconfig/mathview-backend-gtk.pc
%{_includedir}/gtkmathview

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Thu Oct 12 2006 Marc Maurer <uwog@abisource.com> 0.7.6-5.fc6
- Add pkgconfig to the -devel requires (bug 206451)

* Mon Sep 16 2006 Marc Maurer <uwog@abisource.com> 0.7.6-4.fc6
- Rebuild for FC 6

* Thu Feb 16 2006 Marc Maurer <uwog@abisource.com> 0.7.6-3.fc5
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Marc Maurer <uwog@abisource.com> - 0.7.6-2.fc5
- Use %%{?dist} in the release name
- Omit static libs (part of bug 171971)
- s/gtkmathview/%%{name} (part of bug 171971)

* Sun Dec 11 2005 Marc Maurer <uwog@abisource.com> - 0.7.6-1
- Update to 0.7.6

* Sun Sep 25 2005 Marc Maurer <uwog@abisource.com> - 0.7.5-1
- Update to 0.7.5

* Mon Sep 12 2005 Marc Maurer <uwog@abisource.com> - 0.7.4-1
- Update to 0.7.4

* Tue Aug 30 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-5
- Drop more unneeded Requires

* Tue Aug 30 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-4
- Drop the explicit Requires

* Mon Aug 29 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-3
- Use smaller lines in the Description field
- Remove the --disable-gmetadom and --without-t1lib flags
- Add a '/' to directories in the files section
- Remove the mathmlviewer man page

* Tue Aug 23 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-2
- Add the proper Requires and Buildrequires
- Make the description field more descriptive
- Add CONTRIBUTORS BUGS LICENSE to the doc section
- Disable gmetadom and t1lib
- Remove the mathml2ps man page

* Sun Aug 14 2005 Marc Maurer <uwog@abisource.com> - 0.7.3-1
- Initial version
