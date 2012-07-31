Name: udunits
Version: 1.12.4
Release: 11%{?dist}
Summary: A library for manipulating units of physical quantities
License: Freely distributable (BSD-like)
Group: System Environment/Libraries
URL: http://my.unidata.ucar.edu/content/software/udunits/index.html
# Upstream actually packages it as a .tar.Z, I repackaged to prevent ncompress 
# as a dependency.
Source0: udunits-1.12.4.tar.bz2
Patch0: udunits-1.12.4-linuxfixes.patch
Patch1: udunits-1.12.4-64bit.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-gfortran, gcc-c++, groff

%description
The Unidata units utility, udunits, supports conversion of unit specifications 
between formatted and binary forms, arithmetic manipulation of unit 
specifications, and conversion of values between compatible scales of 
measurement. A unit is the amount by which a physical quantity is measured. For 
example:

                  Physical Quantity   Possible Unit
                  _________________   _____________
                        time              weeks
                      distance         centimeters
                        power             watts

This utility works interactively and has two modes. In one mode, both an input 
and output unit specification are given, causing the utility to print the 
conversion between them. In the other mode, only an input unit specification is 
given. This causes the utility to print the definition -- in standard units -- 
of the input unit.

%package devel
Group: Development/Libraries
Summary: Headers and libraries for udunits
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the udunits library.

%package -n perl-udunits
Summary: Perl module for udunits
Group: System Environment/Libraries
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name}

%description -n perl-udunits
A perl module for udunits.

%prep
%setup -q
%patch0 -p1
# Yes, this is a dirty hack.
%ifarch x86_64 ppc64 sparc64
%patch1 -p1
%endif

%build
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
cd src/
export LD_MATH=-lm 
%configure
make all 

%install
rm -rf $RPM_BUILD_ROOT
cd src/
sed "s?/usr?${RPM_BUILD_ROOT}/usr?" Makefile > Makefile.install
make PREFIX=${RPM_BUILD_ROOT}/usr datadir=${RPM_BUILD_ROOT}/etc sysconfigdir=${RPM_BUILD_ROOT}/etc -f Makefile.install install
cp -p COPYRIGHT README RELEASE_NOTES VERSION ../
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man3f

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYRIGHT README RELEASE_NOTES VERSION
%{_bindir}/udunits
%{_mandir}/man1/udunits.1.gz
%config(noreplace) %{_sysconfdir}/udunits.dat

%files devel
%defattr(-,root,root)
%{_includedir}/udunits.h
%{_includedir}/udunits.inc
%{_libdir}/libudport.a
%{_libdir}/libudunits.a
%{_mandir}/man3/udunits.3.gz
%{_mandir}/man3/udunits.3f.gz

%files -n perl-udunits
%defattr(-,root,root)
%{perl_vendorarch}/UDUNITS.pm
%{perl_vendorarch}/auto/UDUNITS/UDUNITS.bs
%{perl_vendorarch}/auto/UDUNITS/UDUNITS.so
%{perl_vendorarch}/auto/UDUNITS/autosplit.ix
%dir %{perl_vendorarch}/auto/UDUNITS/
%{_mandir}/man1/udunitsperl.1.gz

%changelog
* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-11
- bump for FC-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-10
- bump for FC-5

* Sat Jul  9 2005 Ed Hill <ed@eh3.com> 1.12.4-9
- use -fPIC for all arches and remove redundant man3f entry

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-8
- remove hardcoded dist tags

* Fri May  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-7
- fix BuildRequires for the FC-3 spec (gcc-g77 vs gcc-gfortran)

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-6.fc4
- use dist tag

* Sat Apr 16 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-5
- x86_64 needs -fPIC

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-4
- use perl macros

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-3
- Corrected license
- Add BuildRequires: groff
- Add perl MODULE_COMPAT requires for perl-udunits
- Roll in fixes from Ed Hill's package
- Make -devel package

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-2
- minor spec cleanup

* Fri Mar 25 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-1
- inital package for Fedora Extras
