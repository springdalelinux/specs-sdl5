Name: udunits2
Version: 2.1.24
Release: 2%{?dist}
Summary: A library for manipulating units of physical quantities
License: MIT
Group: System Environment/Libraries
URL: http://www.unidata.ucar.edu/software/udunits/
Source0: ftp://ftp.unidata.ucar.edu/pub/udunits/udunits-%{version}.tar.gz
BuildRequires: gcc-c++, groff, byacc, expat-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Unidata units utility, udunits2, supports conversion of unit specifications 
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
Summary: Headers and libraries for udunits2
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the udunits2 library.

%prep
%setup -q -n udunits-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install install-html install-pdf
mkdir -p %{buildroot}%{_infodir}/
install -p -m0644 %{name}.info %{buildroot}%{_infodir}

# We need to do this to avoid conflicting with udunits v1
mkdir -p %{buildroot}%{_includedir}/%{name}/
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/%{name}/
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}/dir

%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc ANNOUNCEMENT CHANGE_LOG LICENSE
%{_bindir}/%{name}
%{_datadir}/udunits/
%{_infodir}/%{name}*.info*
%{_libdir}/libudunits2.so.*
%doc %{_docdir}/udunits

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/libudunits2.so

%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 9 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1.24-1
- Update to 2.1.24
- Install docs via install-html/pdf

* Mon Nov 7 2011 Orion Poplawski <orion@cora.nwra.com> - 2.1.22-1
- Update to 2.1.22

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.19-1
- update to 2.1.19

* Thu Jul  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.17-3
- missing BuildRequires: expat-devel

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.17-2
- tag mistake

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.17-1
- update to 2.1.17
- cleanup spec file

* Sun Dec  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.11-1
- initial package for udunits2: 2.1.11
