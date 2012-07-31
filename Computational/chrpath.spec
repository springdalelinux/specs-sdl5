Summary: Modify rpath of compiled programs
Name: chrpath
Version: 0.13
Release: 1.1%{?dist}.1
License: GPL
Group: Development/Tools
URL: ftp://ftp.hungry.com/pub/hungry/chrpath/
Source0: ftp://ftp.hungry.com/pub/hungry/chrpath/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
chrpath allows you to modify the dynamic library load path (rpath) of
compiled programs.  Currently, only removing and modifying the rpath
is supported.

%prep
%setup -q

%build
%configure
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/usr/doc

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS ChangeLog*
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

%changelog
* Sun May 06 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- rebuilt for RHEL5 final

* Sun Mar 12 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.13-1
- Initial build.

