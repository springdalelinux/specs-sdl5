Summary: A computer program for the calculation of Gromov-Witten invariants
Name: growi
Version: 1.0.2
Release: 2%{?dist}
Source0: %{name}-%{version}.tar.gz
Patch1: growi-1.0-includemove.patch
Patch2: growi-1.0.1-ccfixes.patch
Patch3: growi-1.0.1-gcc34.diff
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Url: http://www.mathematik.uni-kl.de/~gathmann/en/growi.html
BuildRequires: gdbm-devel gmp-devel
#BuildRequires: compat-gcc-34 compat-gcc-34-c++
#Requires: compat-gcc-34 compat-gcc-34-c++
BuildRequires: gcc-c++
Requires: gcc-c++

%description
GROWI is a C++ program for the computation of Gromov-Witten invariants. The current version 1.0 can compute:

    * (Absolute) Gromov-Witten invariants of projective spaces in any genus,
    * (Absolute) Gromov-Witten invariants of any hypersurface in a projective space in genus 0,
    * Relative Gromov-Witten invariants of projective spaces relative any hypersurface in genus 0.

"Descendants" can be used in all these invariants.

%prep
%setup
%patch1 -p1 -b .includemove
#patch2 -p1 -b .ccfixes
#patch3 -p1 -b .gcc34

%build
#export CC=gcc34 CXX=g++34
export CFLAGS="-O2 -g -pipe"
export CXXFLAGS="-O2 -g -pipe"
export FFLAGS="-O2 -g -pipe"
%configure
make

%install
%makeinstall
mkdir $RPM_BUILD_ROOT/%{_includedir}/growi
mv $RPM_BUILD_ROOT/%{_includedir}/*.h $RPM_BUILD_ROOT/%{_includedir}/growi

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc README COPYING INSTALL AUTHORS
%{_bindir}/*
%{_libdir}/lib*.a
%{_includedir}/growi

%changelog
* Fri Aug 17 2007 Josko Plazonic <plazonic@math.princeton.edu>
- drop my attempted c++ fixes and just use old version of c++
