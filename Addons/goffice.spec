Name:           goffice         
Version:        0.2.2
Release:        1%{?dist}
Summary:        Goffice support libraries
Group:          System Environment/Libraries
License:        GPL  
URL:            http://freshmeat.net/projects/goffice/
Source0:        ftp://ftp.gnome.org/pub/gnome/sources/%{name}/0.2/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libgsf-devel           >= 1.13.3
BuildRequires:  libgnomeprint22-devel  >= 2.8.2
BuildRequires:  libgnomeui-devel       >= 2.0.0
BuildRequires:  intltool gettext

%description
Support libraries for gnome office


%package devel
Summary:        Libraries and include files for goffice
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       libgsf-devel           >= 1.13.3
Requires:       libgnomeprint22-devel  >= 2.8.2
Requires:       libgnomeui-devel       >= 2.0.0

%description devel
Development libraries for goffice


%prep
%setup -q


%build
%configure --disable-dependency-tracking
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang goffice
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}/%{version}/plugins/*/*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files -f goffice.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*
%{_libdir}/goffice/
%{_datadir}/goffice/
%{_datadir}/pixmaps/goffice/

%files devel
%{_includedir}/libgoffice-1/
%{_libdir}/pkgconfig/libgoffice-1.pc
%{_libdir}/*.so


%changelog
* Thu Mar  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-1
- New upstream release 0.2.2
- Fix rpath usage on x86_64

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.1-2
- FE6 Rebuild

* Tue May  2 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.1-1
- new upstream version: 0.2.1

* Tue Mar 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.0-2
- rebuild for new libgsf

* Thu Feb 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.0-1
- New upstream version
- Remove .la files from plugin dirs
- Add BuildRequires: intltool gettext

* Mon Feb 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-4
- Bump release and rebuild for new gcc4.1 and glibc.
- add %%{?dist} for consistency with my other packages

* Thu Dec  8 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-3
-Switch to core version of libgsf now Core has 1.13 instead of using special
 Extras libgsf113 version.

* Mon Nov 28 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-2
-Make Source0 a full URL
-Better URL tag
-Fix not owning /usr/lib(64)/goffice and /usr/share/goffice

* Fri Nov 25 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-1
-change name to goffice as that is the upstream tarbal name.
-bump to 0.1.2 this is the minimal version supported by gnumeric-1.6
-use extras libgsf113 package since core libgsf is to old
-use locale macros
-don't ship .la files
-remove some redundant (already included in other) (Build)Requires

* Sat Nov 05 2005 Michael Wise <micwise at gmail.com> - 0.0.4-1
- Initial spec file