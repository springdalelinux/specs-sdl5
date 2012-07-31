Name:           perl-version
Version:        0.76
Release:        1%{?dist}.1
Summary:        Perl extension for Version Objects
Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/version
Source0:        http://search.cpan.org/CPAN/authors/id/J/JP/JPEACOCK/version-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Epoch:          1

BuildRequires:	perl(Module::Build) >= 0.2611, perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}

%prep
%setup -q -n version-%{version}
sed -i "s|#!perl|#!%{__perl}|" lib/version.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
chmod u+x blib/lib/version.pm blib/lib/version/vxs.pm
make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%doc %{perl_vendorarch}/version.pod
%{perl_vendorarch}/auto/version/
%{perl_vendorarch}/version/
%{perl_vendorarch}/version.pm
%{_mandir}/man3/*.3*


%changelog
* Tue Jul  3 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.7203-1.1
- add BR: Test::More

* Tue Jul  3 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.7203-1
- i love perl versioning. bumping to 0.7203

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.69-1
- funky perl numbering gives us an epoch as we go to 0.69

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.6701-1
- bump to 0.6701

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.64-1
- bump to 0.64

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.59-1
- bump to 0.59

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.57-1
- bump to 0.57

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.51-3
- one sed line only, not global, using __perl

* Sun Jan  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.51-2
- clean up scripty bits of some .pm files

* Fri Jan  6 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.51-1
- bump to 0.51
- pod file is doc

* Fri Jan  6 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.50-2
- don't pass optflags twice
- remove .bs files

* Thu Jan  5 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.50-1
- Initial package for Fedora Extras
