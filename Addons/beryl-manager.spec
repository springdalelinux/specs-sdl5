Name:           beryl-manager
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Beryl window decorator and theme management utility
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
Patch0:         beryl-manager-0.1.4-pidof.patch

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}

BuildRequires:  beryl-core-devel >= %{version}, gtk2-devel >= 2.8.0
BuildRequires:  perl(XML::Parser), gettext-devel, desktop-file-utils


%description
Beryl is a combined window manager and compositing
manager that runs on top of Xgl or AIGLX using OpenGL
to provide effects accelerated by a 3D graphics card
on the desktop. Beryl is a community-driven fork of
Compiz.

Beryl-manager is a tray application to keep beryl
up and running, switch window managers, decorators,
launch beryl-settings and the beryl theme tool.


%prep
%setup -q
# Use absolute path to pidof, not in most users' $PATH
%patch0 -p1 -b .pidof


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
# Fix up xy_XY to just xy
for lang in ar_AR gl_GL my_MY sk_SK tr_TR
do
  dest=$(echo ${lang} | cut -d_ -f1)
  mv $RPM_BUILD_ROOT%{_datadir}/locale/${lang} \
    $RPM_BUILD_ROOT%{_datadir}/locale/${dest} 2>&1 > /dev/null
done 
%find_lang %{name}


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
%doc COPYING
%{_bindir}/beryl-manager
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/hicolor/*/apps/beryl-manager.png
%{_datadir}/icons/hicolor/scalable/apps/beryl-manager.svg
%{_datadir}/applications/*.desktop
%{_mandir}/man1/beryl-manager.1.gz


%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0-1
- beryl 0.2.0

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Tue Feb 06 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-2
- Remove duplicate desktop file

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release
- Fix up a bunch of locale files (others should get added
  to filesystem package in due course)

* Wed Nov 22 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-4
- Add new missing BR: desktop-file-utils

* Wed Nov 22 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Add desktop file
- Trim BR:

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Use upstream tarball, now that there is one

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- New upstream release

* Tue Oct 31 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-2
- Add missing BR: libtool, gettext-devel

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-1
- New upstream release
- Require beryl-core of at least the same version
- Move autoreconf bits to prep section

* Thu Oct 05 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-2
- Fix for pidof not in users' $PATH

* Tue Oct 03 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-1
- Initial Fedora build
