
Summary: High-performance algorithms for vectors, matrices, and polynomials 
Name:    ntl 
Version: 5.4 
Release: 4%{?dist}
Obsoletes: NTL

# See doc/copying.txt
License: GPL
URL:     http://shoup.net/ntl/ 
Source:	 http://shoup.net/ntl/ntl-%{version}.tar.gz
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gmp-devel

# includes no debuginfo'able bits, disable
%define debug_package %{nil}

%description
NTL is a high-performance, portable C++ library providing data structures
and algorithms for arbitrary length integers; for vectors, matrices, and
polynomials over the integers and over finite fields; and for arbitrary
precision floating point arithmetic.

NTL provides high quality implementations of state-of-the-art algorithms for:
* arbitrary length integer arithmetic and arbitrary precision floating point
  arithmetic;
* polynomial arithmetic over the integers and finite fields including basic
  arithmetic, polynomial factorization, irreducibility testing, computation
  of minimal polynomials, traces, norms, and more;
* lattice basis reduction, including very robust and fast implementations of
  Schnorr-Euchner, block Korkin-Zolotarev reduction, and the new 
  Schnorr-Horner pruning heuristic for block Korkin-Zolotarev;
* basic linear algebra over the integers, finite fields, and arbitrary
  precision floating point numbers. 

%package devel
Summary: High-performance algorithms for vectors, matrices, and polynomials 
Group:   Development/Libraries
%description devel
NTL is a high-performance, portable C++ library providing data structures
and algorithms for arbitrary length integers; for vectors, matrices, and
polynomials over the integers and over finite fields; and for arbitrary
precision floating point arithmetic.

NTL provides high quality implementations of state-of-the-art algorithms for:
* arbitrary length integer arithmetic and arbitrary precision floating point
  arithmetic;
* polynomial arithmetic over the integers and finite fields including basic
  arithmetic, polynomial factorization, irreducibility testing, computation
  of minimal polynomials, traces, norms, and more;
* lattice basis reduction, including very robust and fast implementations of
  Schnorr-Euchner, block Korkin-Zolotarev reduction, and the new
  Schnorr-Horner pruning heuristic for block Korkin-Zolotarev;
* basic linear algebra over the integers, finite fields, and arbitrary
  precision floating point numbers.


%prep
%setup -q 


%build
cd src
./configure \
  CC="%{__cc}" \
  CXX="%{__cxx}" \
  CFLAGS="%{optflags}" \
  CXXFLAGS="%{optflags}" \
  PREFIX=%{_prefix} \
  DOCDIR=%{_docdir} \
  INCLUDEDIR=%{_includedir} \
  LIBDIR=%{_libdir} \
  NTL_GMP_LIP=on
cd -

# not smp-safe
make -C src 


%check ||:
# skip by default, takes a *long, long, long* (days?) time -- Rex
%{?_with_check:make -C src check}


%install
rm -rf $RPM_BUILD_ROOT

make -C src install \
  PREFIX=$RPM_BUILD_ROOT%{_prefix} \
  DOCDIR=$RPM_BUILD_ROOT%{_docdir} \
  INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir} \
  LIBDIR=$RPM_BUILD_ROOT%{_libdir} 

# Unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/NTL


%clean
rm -rf $RPM_BUILD_ROOT


%files devel
%defattr(-,root,root,-)
%doc README 
%doc doc/*
%{_includedir}/*
%{_libdir}/lib*.a


%changelog
* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-4
- fc6 respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-3
- fc6 respin

* Tue Apr 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-2
- Capitalize %%summary
- disable -debuginfo, includes no debuginfo'able bits 

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.4-1
- 5.4 (first try)


