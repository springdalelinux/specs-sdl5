Summary: Automatic mail answering program for Linux
Name: vacation
Version: 1.2.5
Release: 3%{?dist}
License: GPL
Group: Applications/Internet
Source: http://www.tcob1.uklinux.net/files/vacation-%{version}.tar.gz
Patch0: vacation.patch
Prefix: /usr
BuildRoot: /tmp/%{name}-%{version}-%{release}-root
URL: http://www.tcob1.uklinux.net/
BuildRequires: gdbm-devel

%description
Vacation is a port of the 386BSD vacation program (an automatic
mail-answering program found on many Unix systems) to Linux.

%prep
%setup -n vacation
%patch0 -p1
perl -pi -e 's|-m486||' Makefile
perl -pi -e 's|install -s|install|' Makefile

%build
rm -f vacation
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_mandir}/{man1,man5},%{_bindir}}
make BINDIR=$RPM_BUILD_ROOT%{_bindir} MANDIR=$RPM_BUILD_ROOT%{_mandir}/man install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING ChangeLog README vacation-%{version}.lsm
%{_bindir}/vac*
%{_mandir}/man1/vac*
#/usr/man/man5/aliases.5
# /usr/man/man5/forward.5.gz
