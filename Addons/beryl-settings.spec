Name:           beryl-settings
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Beryl OpenGL window and compositing manager GUI config utility
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
Source1:        http://releases.beryl-project.org/%{version}/%{name}-bindings-%{version}.tar.bz2
Source2:        http://releases.beryl-project.org/%{version}/%{name}-simple-%{version}.tar.bz2

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}, beryl-plugins >= %{version}

BuildRequires:  beryl-core-devel >= %{version}
BuildRequires:  gtk2-devel >= 2.8.0, gettext-devel
BuildRequires:  pygtk2-devel, Pyrex, python-devel >= 2.3
BuildRequires:  perl(XML::Parser), desktop-file-utils

%{!?python_sitearch: %define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')}

%description
Beryl is a combined window manager and compositing
manager that runs on top of Xgl or AIGLX using OpenGL
to provide effects accelerated by a 3D graphics card
on the desktop. Beryl is a community-driven fork of
Compiz.

This package contains a graphical configuration tool
to configure Beryl's plugins and the composite window
manager.


%package simple
Summary:        Simplified beryl settings GUI
Group:          User Interface/Desktops
Requires:       %{name} = %{version}-%{release}


%description simple
A beryl settings configuration utility that takes
a minimal, simplified approach to configuring beryl.


%prep
%setup -q -a 1 -a 2

%build
# beryl-settings-bindings
pushd beryl-settings-bindings-%{version}
%configure
make %{?_smp_mflags}
popd
# beryl-settings
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:$RPM_BUILD_DIR/%{name}-%{version}/%{name}-bindings-%{version}/
%configure
make %{?_smp_mflags}
# beryl-settings-simple
pushd beryl-settings-simple-%{version}
%configure
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
# beryl-settings-bindings
pushd beryl-settings-bindings-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
popd
# beryl-settings
make DESTDIR=$RPM_BUILD_ROOT install
desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
# beryl-settings-simple
pushd beryl-settings-simple-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-simple.desktop
popd
find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f
%find_lang %{name}
%find_lang %{name}-simple


%clean
rm -rf $RPM_BUILD_ROOT


%post
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :


%postun
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/beryl-settings
%{python_sitearch}/berylsettings.so
%{_libdir}/pkgconfig/beryl-settings-bindings.pc
%dir %{_datadir}/bsm
%dir %{_datadir}/bsm/images
%{_datadir}/bsm/images/*.svg
%{_datadir}/icons/hicolor/scalable/apps/beryl-settings.svg
%{_datadir}/applications/*beryl-settings.desktop
# Man page went awol in 0.1.99.2...
#{_mandir}/man1/beryl-settings.1.gz


%files simple -f %{name}-simple.lang
%defattr(-,root,root,-)
%{_bindir}/beryl-settings-simple
%dir %{_datadir}/beryl-settings-simple
%{_datadir}/beryl-settings-simple/*.svg
%{_datadir}/beryl-settings-simple/*.png
%{_datadir}/beryl-settings-simple/*.Profile
%{_datadir}/applications/*beryl-settings-simple.desktop


%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0
- beryl 0.2.0

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Wed Feb 07 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-4
- Fix image path in beryl-settings-simple

* Tue Feb 06 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-3
- Get rid of duplicate desktop entries

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-2
- Fix pkg-config path so this actually builds
- Reshuffle build section a bit

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)
- put beryl-settings-simple in its own package
- R: beryl-plugins, or there's nothing to configure

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Trim BR:

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Use upstream tarball, now that there is one

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- New upstream release

* Mon Nov 06 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-3
- Fix desktop file to point to proper icon file

* Tue Oct 31 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-2
- Add missing BR: libtool, gtk2-devel >= 2.8.0, gettext-devel,
  libXcomposite-devel, libXdamage-devel

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-1
- New upstream release
- Require beryl-core of at least the same version
- Move autoreconf bits to prep section

* Thu Oct 05 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-3
- Really fix duplicate menu entries this time

* Thu Oct 05 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-2
- Fix duplicate menu entries
- Add proper post/postun

* Tue Oct 03 2006 - Jarod Wilson <jwilson@redhat.com> 0.1.0-1
- Initial Fedora build
