Name:           bdock
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Beryl project's replacement windowmaker dock
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Source only available via svn right now
# svn://svn.beryl-project.org/beryl/tags/release-%{version}/%{name}
Source0:        %{name}-%{version}.tar.bz2

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}

BuildRequires:  beryl-core-devel >= %{version}
BuildRequires:  libtool, gettext-devel
BuildRequires:  libwnck-devel, gtk2-devel >= 2.8.0


%description
Beryl is a combined window manager and compositing
manager that runs on top of Xgl or AIGLX using OpenGL
to provide effects accelerated by a 3D graphics card
on the desktop. Beryl is a community-driven fork of
Compiz.

Bdock is a replacement for the windowmaker dock.


%prep
%setup -q
autoreconf -v --install

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
%doc AUTHORS COPYING
%{_bindir}/bdock
%dir %{_datadir}/bdock
%{_datadir}/bdock/*
%{_mandir}/man1/bdock.1*

%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0-1
- beryl 0.2.0 -- though outside of the VERSION file, bdock
  hasn't actually changed in like five months and the project
  doesn't roll tarballs of it...

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Mon Nov 20 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-4
- Make pixmaps install where binary expects them

* Thu Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Trim BR:

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Remove zero-length doc files (note to self, don't forget
  to re-include them if/when they have content...)

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- Initial build
