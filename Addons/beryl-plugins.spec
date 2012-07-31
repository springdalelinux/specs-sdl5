Name:           beryl-plugins
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Beryl OpenGL window and compositing manager plug-ins
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
Source1:        fedora-cubecaps.png
Source2:        http://releases.beryl-project.org/%{version}/%{name}-unsupported-%{version}.tar.bz2

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}

BuildRequires:  beryl-core-devel >= %{version}
BuildRequires:  desktop-file-utils, librsvg2-devel
BuildRequires:  perl(XML::Parser), gettext-devel, libjpeg-devel

Obsoletes:      beryl-dbus <= %{version}-%{release}
Provides:       beryl-dbus = %{version}-%{release}

%description
Beryl is a combined window manager and compositing
manager that runs on top of Xgl or AIGLX using OpenGL
to provide effects accelerated by a 3D graphics card
on the desktop. Beryl is a community-driven fork of
Compiz.

Beryl has a flexible plug-in system, which the
contents of this package take advantage of.


%package unsupported
Summary: Unsupported beryl plugins
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description unsupported
Beryl plugins that are either:
* unstable
* only modestly maintained
* or completely unmaintained

Use at your own risk.


%prep
%setup -q -a 2

%build
%configure
make %{?_smp_mflags}
# unsupported plugins
pushd %{name}-unsupported-%{version}
%configure
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT%{_datadir}/beryl/cubecaps.png $RPM_BUILD_ROOT%{_datadir}/beryl/cubecaps-beryl.png
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/beryl/cubecaps.png
%find_lang %{name}
# hack to figure out which plugins are supported
(cd $RPM_BUILD_ROOT%{_libdir}/beryl/; ls *.so) > supported-plugins
# unsupported plugins
pushd %{name}-unsupported-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
# even uglier hack to figure out unsupported plugins
(find . -name "*.la" | xargs grep dlname | cut -f2 -d"'") > ../unsupported-plugins
popd
%find_lang %{name}-extra
# more hacks for supported/unsupported auto-splitting
for p in $(cat supported-plugins)
do
  echo %{_libdir}/beryl/$p >> %{name}.lang
done
for p in $(cat unsupported-plugins)
do
  echo %{_libdir}/beryl/$p >> %{name}-extra.lang
done
# nuke static libs and libtool archives
find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_datadir}/beryl/*.png

%files unsupported -f %{name}-extra.lang
%defattr(-,root,root,-)


%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0
- beryl 0.2.0

* Fri Feb 23 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-2
- Drop unnecessary dep on fedora-logos (#229793)
- Ugh, fine. Build the unsupported plugins (#227539)

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Tue Jan 30 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-3
- Forgot to Provides: beryl-dbus

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-2
- Add BR: libjpeg-devel

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-2
- Don't provide beryl lib dir, beryl-core should

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-2
- Add BR for freshly added translations

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Trim BR:

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Switch to upstream tarball, now that there is one

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- New upstream release

* Mon Nov 06 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-3
- Fedora-branded cube caps (Chitlesh Goorah)

* Tue Oct 31 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-2
- Add missing BR: libtool, gettext-devel

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-1
- New upstream release
- Require beryl-core of at least the same version
- Move autoreconf bits to prep section

* Tue Oct 03 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-1
- Initial Fedora build
