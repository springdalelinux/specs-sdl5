Name:		memtester
Version:	4.1.2
Release:	1%{?dist}
Summary:	Utility to test for faulty memory subsystem

Group:		System Environment/Base
License:	GPLv2
URL:		http://pyropus.ca/software/memtester/
Source0:	http://pyropus.ca/software/memtester/old-versions/%{name}-%{version}.tar.gz
Patch0:		memtester-4.0.8-debuginfo.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	dos2unix
#Requires:	

%description
memtester is a utility for testing the memory subsystem in a computer to
determine if it is faulty.



%prep
%setup -q
%patch0 -p1 -b .debuginfo


%build
make %{?_smp_mflags} -e OPT="%{optflags}"


%install
rm -rf $RPM_BUILD_ROOT
mv README README.iso88591
iconv -o README -f iso88591 -t utf8 README.iso88591
touch -r README.iso88591 README
rm -f README.iso88591
dos2unix -k BUGS
make -e INSTALLPATH=$RPM_BUILD_ROOT%{_prefix} install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
#fix location of manual
mv $RPM_BUILD_ROOT%{_prefix}/man/man8/memtester.8.gz $RPM_BUILD_ROOT%{_mandir}/man8


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc BUGS CHANGELOG COPYING README README.tests
%{_bindir}/memtester
%{_mandir}/man8/memtester.8.gz



%changelog
* Sat Aug 01 2009 Lucian Langa <cooly@gnome.eu.org> - 4.1.2-1
- new upstream release

* Sun Jul 26 2009 Lucian Langa <cooly@gnome.eu.org> - 4.1.1-1
- misc cleanups
- new upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Lucian Langa <cooly@gnome.eu.org> - 4.0.8-2
- preserve timestamps
- fix patch

* Sat Sep 27 2008 Lucian Langa <cooly@gnome.eu.org> - 4.0.8-1
- initial specfile


