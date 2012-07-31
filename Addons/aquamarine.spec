Name:           aquamarine
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Themeable window decorator and compositing manager for Beryl
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2
Patch0:         aquamarine-0.1.9999.2-fixes.patch

# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Requires:       beryl-core >= %{version}, kdelibs, kdebase

BuildRequires:  beryl-core-devel >= %{version}
BuildRequires:  qt-devel, kdelibs-devel, kdebase-devel
BuildRequires:  libtool, perl(XML::Parser), gettext-devel


%description
Aquamarine is themeable window decorator and compositing
manager for Beryl. Launch Theme Manager from
beryl-manager to change themes. Aquamarine is intended
for use with KDE.

%prep
%setup -q
%patch0 -p1 -b .make

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# Fix up xy_XY to just xy
for lang in es_ES hu_HU it_IT ru_RU
do
  dest=$(echo ${lang} | cut -d_ -f1)
  mv $RPM_BUILD_ROOT%{_datadir}/locale/${lang} \
    $RPM_BUILD_ROOT%{_datadir}/locale/${dest} 2>&1 > /dev/null
done

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/aquamarine
%{_libdir}/kde3/kcm_beryl.so
%{_libdir}/kde3/kcm_beryl.la
%{_datadir}/applications/kde/beryl.desktop
%{_datadir}/config.kcfg/aquamarine.kcfg
%{_libdir}/beryl/backends/libkconfig.so
%{_libdir}/beryl/backends/libkconfig.la


%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0-1
- beryl 0.2.0

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-2
- Fix up patch

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.2-1
- beryl 0.1.9999.2 (aka 0.2.0-rc2)

* Mon Feb 05 2007 Jarod Wilson <jwilson@redhat.com> 0.1.9999.1-1
- beryl 0.1.9999.1 (aka 0.2.0-rc1)

* Mon Jan 29 2007 Jarod Wilson <jwilson@redhat.com> 0.1.99.2-1
- New upstream release

* Thu Jan 11 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-3
- kcontrol beryl item requires .la files to function (#221733)

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-2
- Add BR: for translations

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 0.1.4-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 0.1.3-1
- New upstream release

* Fri Nov 17 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-3
- Remove R: qt, kdelibs, rely on auto-gen lib deps

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Trim BR:

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- Initial build
