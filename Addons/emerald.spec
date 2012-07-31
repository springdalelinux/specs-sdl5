Name:           emerald
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Themeable window decorator and compositing manager for Beryl
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}

BuildRequires:  beryl-core-devel >= %{version}
BuildRequires:  libwnck-devel, gtk2-devel
BuildRequires:  intltool, desktop-file-utils
BuildRequires:  perl(XML::Parser), gettext-devel


%description
Emerald is themeable window decorator and compositing 
manager for Beryl. Launch Theme Manager from
beryl-manager to change themes.


%package devel
Summary: Development files for emerald
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The emerald-devel package provides development files
for emerald, the themeable window decorator for beryl.


%prep
%setup -q
# Should only have one Exec line in a desktop file...
perl -pi -e 's|Exec=emerald-theme-manager -i||g' misc/emerald-theme-manager.desktop
# Death to rpaths...
perl -pi -e 's|hardcode_into_libs=.*|hardcode_into_libs=no|g' configure
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' configure
perl -pi -e 's|runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' configure


%build
%configure --enable-librsvg --disable-mime-update
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f
desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  $RPM_BUILD_ROOT%{_datadir}/applications/emerald-theme-manager.desktop
# Fix up xy_XY to just xy
for lang in tr_TR
do
  dest=$(echo ${lang} | cut -d_ -f1)
  mv $RPM_BUILD_ROOT%{_datadir}/locale/${lang} \
    $RPM_BUILD_ROOT%{_datadir}/locale/${dest}
done
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
update-mime-database %{_datadir}/mime &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun
/sbin/ldconfig
update-mime-database %{_datadir}/mime &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/*
%{_datadir}/pixmaps/*
%dir %{_libdir}/emerald
%{_libdir}/emerald/*
%{_libdir}/libemeraldengine.so.*
%dir %{_datadir}/emerald
%dir %{_datadir}/emerald/theme
%{_datadir}/emerald/theme/*
%{_datadir}/emerald/settings.ini
%{_datadir}/applications/*
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*
%{_datadir}/icons/hicolor/48x48/mimetypes/*
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libemeraldengine.so

%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0
- beryl 0.2.0

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-2
- Add necessary BR for freshly-added translations

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-4
- Trim BR:

* Wed Nov 15 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Kill rpaths

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Use upstream tarball, now that there is one

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- New upstream release

* Tue Oct 31 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-2
- Add missing BR: libtool, gettext-devel, libwnck-devel,
  libXdamage, libXcomposite

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-1
- New upstream release
- Require beryl-core of at least the same version
- Move autoreconf bits to prep section

* Thu Oct 05 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-3
- Really fix the duplicate menu entries this time

* Thu Oct 05 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-2
- Fix duplicate menu entries

* Tue Oct 03 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-1
- Initial Fedora build
