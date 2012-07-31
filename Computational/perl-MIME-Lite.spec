Name:           perl-MIME-Lite
Version:        3.01
Release:        5%{?dist}.1
Summary:        MIME::Lite - low-calorie MIME generator

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/MIME-Lite/
Source0:        http://www.cpan.org/authors/id/Y/YV/YVES/MIME-Lite-3.01.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl >= 1:5.6.1
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
MIME::Lite is intended as a simple, standalone module for generating (not 
parsing!) MIME messages... specifically, it allows you to output a simple,
decent single- or multi-part message with text or binaryattachments.  It does
not require that you have the Mail:: or MIME:: modules installed.

%prep
%setup -q -n MIME-Lite-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


%check || :
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc changes.pod README examples contrib  
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.01-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> 3.01-5
- Rebuild

* Thu Mar 30 2006 Mike McGrath <imlinux@gmail.com> 3.01-4
- New maintainer

* Thu Jun 23 2005 Ralf Corsepius <ralf@links2linux.de> 3.01-3
- Add %%{dist}.

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 3.01-2
- Review suggestions from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 3.01-1
- Initial packageing.
