Name:           emerald-themes
Url:            http://www.beryl-project.org/
License:        GPL
Group:          User Interface/Desktops
Version:        0.2.0
Release:        1%{?dist}

Summary:        Themes for Emerald, the window decorator for Beryl
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        http://releases.beryl-project.org/%{version}/%{name}-%{version}.tar.bz2

BuildArch:      noarch

Requires:       beryl-core >= %{version}, emerald >= %{version}
BuildRequires:  libtool


%description
Emerald is themeable window decorator and compositing 
manager for Beryl. Launch Theme Manager from
beryl-manager to change themes.

This package contains themes for emerald.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*~" | xargs rm -f
chmod a+r $RPM_BUILD_ROOT%{_datadir}/emerald/themes/Scaled_Black_Mod/*
rm -f $RPM_BUILD_ROOT%{_datadir}/emerald/themes/import.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_datadir}/emerald/*


%changelog
* Thu Mar 15 2007 Jarod Wilson <jwilson@redhat.com> 0.2.0-1
- beryl 0.2.0

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

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-2
- Use upstream tarball, now that there is one
- Remove import.sh, only used during build

* Fri Nov 10 2006 Jarod Wilson <jwilson@redhat.com> 0.1.2-1
- New upstream release

* Tue Oct 31 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-2
- Fix perms on Scaled_Black_Mod theme
- Add missing BR: libtool

* Thu Oct 26 2006 Jarod Wilson <jwilson@redhat.com> 0.1.1-1
- New upstream release
- Require beryl-core and emerald of at least the same version
- Move autoreconf bits to prep section

* Tue Oct 03 2006 Jarod Wilson <jwilson@redhat.com> 0.1.0-1
- Initial Fedora build
