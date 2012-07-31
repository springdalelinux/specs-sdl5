Name:           beryl-core
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Beryl OpenGL window and compositing manager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
Source1:        http://releases.beryl-project.org/0.1.99.2/beryl-mesa-0.1.99.2.tar.bz2
Patch0:         mesa-6.4.1-x86_64-fixes-1.patch

# libdrm is not avaliable on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       mesa-libGL >= 6.5-9
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  libX11-devel, libdrm-devel, libwnck-devel
BuildRequires:  libXfixes-devel, libXrandr-devel, libXrender-devel
BuildRequires:  libXcomposite-devel >= 0.3, libXdamage-devel, libXext-devel
BuildRequires:  libXt-devel, libXmu-devel, libICE-devel, libSM-devel
BuildRequires:  libXinerama-devel, mesa-libGL-devel >= 6.5-9
BuildRequires:  startup-notification-devel >= 0.7
BuildRequires:  gettext-devel, libtool, intltool
BuildRequires:  avahi-compat-libdns_sd-devel, freeglut-devel
BuildRequires:  dbus-glib, dbus-devel, librsvg2-devel

%description
Beryl is a combined window manager and compositing
manager that runs on top of Xgl or AIGLX using OpenGL
to provide effects accelerated by a 3D graphics card
on the desktop. Beryl is a community-driven fork of
Compiz.


%package devel
Summary: Development packages for beryl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
# These Requires: are things (most) beryl sub-packages
# need to build, so they can minimally BR: beryl-core-devel
Requires: libX11-devel, libXfixes-devel, libXrender-devel
Requires: libXdamage-devel, libXcomposite-devel >= 0.3
Requires: libXext-devel, libXinerama-devel, libXrandr-devel
Requires: libSM-devel, libpng-devel, startup-notification-devel
Requires: mesa-libGL-devel >= 6.5-9

%description devel
The beryl-core-devel package includes the header
and library files for the beryl-core
package.

%package -n beryl
Summary: Beryl meta-package to install all beryl components
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: beryl-gnome = %{version}-%{release}
Requires: beryl-kde = %{version}-%{release}
Requires: bdock >= %{version}

%description -n beryl
This is a meta-package, which depends on all available beryl bits,
making it easy for users to get all things beryl installed.

%package -n beryl-gnome
Summary: Beryl meta-package to install all beryl components for Gnome
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: beryl-settings >= %{version}, beryl-settings-simple >= %{version}
Requires: beryl-manager >=  %{version}, beryl-plugins >= %{version}
#Requires: beryl-vidcap >= %{version}
Requires: emerald >= %{version}, emerald-themes >= %{version}
Requires: heliodor >= %{version}

%description -n beryl-gnome
This is a meta-package, which depends on all available beryl bits
relevant to the Gnome desktop environment, making it easy for
users to install all the beryl bits for Gnome.

%package -n beryl-kde
Summary: Beryl meta-package to install all beryl components for KDE
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: beryl-settings >= %{version}, beryl-settings-simple >= %{version}
Requires: beryl-manager >=  %{version}, beryl-plugins >= %{version}
#Requires: beryl-vidcap >= %{version}
Requires: emerald >= %{version}, emerald-themes >= %{version}
Requires: aquamarine >= %{version}

%description -n beryl-kde
This is a meta-package, which depends on all available beryl bits
relevant to the KDE desktop environment, making it easy for
users to install all the beryl bits for KDE.

%prep
%setup -q -a 1


%build
pushd beryl-mesa/src
make %{?_smp_mflags}
popd
%configure --enable-xgl \
    --with-berylmesadir=./beryl-mesa \
    --x-includes=%{_includedir}/X11/ \
    --x-libraries=%{_libdir}/X11/
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# Kill static and libtool libs
find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/beryl*
%dir %{_datadir}/beryl
%dir %{_libdir}/beryl
%dir %{_libdir}/beryl/backends
%{_datadir}/beryl/*.png
%{_mandir}/man1/beryl*
%{_libdir}/libberylsettings.so.0
%{_libdir}/libberylsettings.so.0.0.0
%{_libdir}/libberyldecoration.so.0
%{_libdir}/libberyldecoration.so.0.0.0
%{_libdir}/beryl/backends/*.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libberylsettings.so
%{_libdir}/libberyldecoration.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/beryl
%{_includedir}/beryl/*.h
%{_mandir}/man3/beryl*

%files -n beryl
%defattr(-,root,root,-)

%files -n beryl-gnome
%defattr(-,root,root,-)

%files -n beryl-kde
%defattr(-,root,root,-)

%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0-1
- beryl 0.2.0

* Fri Feb 23 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-2
- Nuke rpaths (resolves #229778, #226719)

* Fri Feb 16 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Thu Feb 08 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-3
- Upstream changed how to turn on beryl-xgl build, respin to
  turn it back on again (#227844)

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-2
- Add R: on beryl-settings-simple to meta-packages

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Tue Jan 30 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-2
- Un-require beryl-dbus, since its part of beryl-plugins now

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-2
- Provide beryl libdir

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-2
- Turn beryl-xgl bits back on (#219566)

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Tue Nov 21 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-6
- Dump R: beryl-vidcap until its into FE
- Fix up GL library linking to resolve some undefined symbols

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-5
- Add BR: libXinerama-devel
- Fix up R: for beryl-core-devel

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-4
- Don't Provides: beryl, instead create meta-packages
- Minimize config flags, the build figures it out itself
- Fix for hosed-up release tarball including .o files...

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Put man3 in -devel, remove dead libsvg-cairo-devel BR

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Use upstream tarballs, now that they finally exist
- Add proper ldconfig bits

* Thu Nov 09 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- New upstream release

* Mon Nov 06 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-3
- Trim Requires: down a bit

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-2
- BR cleanups, should allow building on FC5 - devel

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-1
- New upstream release
- Move autoreconf bits to prep section

* Tue Oct 03 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-1
- Initial Fedora build
