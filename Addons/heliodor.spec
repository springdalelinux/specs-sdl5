Name:           heliodor
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Beryl window decorator with Metacity theme support
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}

BuildRequires:  beryl-core-devel >= %{version}, gnome-desktop-devel
BuildRequires:  metacity, control-center-devel
BuildRequires:  libtool, gettext-devel
BuildRequires:  libwnck-devel

Obsoletes:      heliodor-devel <= %{version}-%{release}

%description
Beryl is a combined window manager and compositing
manager that runs on top of Xgl or AIGLX using OpenGL
to provide effects accelerated by a 3D graphics card
on the desktop. Beryl is a community-driven fork of
Compiz.

Heliodor is a gtk-window-decorator for use with beryl
that supports using Metacity themes.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/window-manager-settings/libberyl.so
%{_bindir}/heliodor
%{_datadir}/gnome/wm-properties/beryl.desktop


%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0
- beryl 0.2.0

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-2
- Drop unnecessary Metacity 2.17+ patch

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Mon Nov 20 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-4
- Remove some R:, let auto lib deps pull them in

* Fri Nov 17 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Fix for Metacity 2.17+ changes

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Trim BR:

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- Initial build
