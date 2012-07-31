Summary:  LASPack  is a package for solving large sparse systems of linear equations like those which arise from the discretization of partial differential equations. 
Name: LASPack
Version: 1.12.3
Release: 2%{?dist}
License: Other
Group: Scientific/Libraries
URL: http://www.tu-dresden.de/mwism/skalicky/laspack/laspack.html
Source: http://www.tu-dresden.de/mwism/skalicky/laspack-%{version}.tar.Z
Source1: laspack_COPYRIGHT
Buildroot: %{_tmppath}/%{name}-root
Prefix: %{_prefix}

%description
LASPack  is a package for solving large sparse systems of linear equations like those which arise from the discretization of partial differential equations. 

Main features:

    * The primary aim of LASPack is the implementation of efficient iterative methods for the solution of systems of linear equations. All routines and data structures are optimized for effective usage of resources especially with regard to large sparse matrices. The package can be accessed from an application through a straightforward interface defined in the form of procedure calls.
    * Besides the obligatory Jacobi, successive over-relaxation, Chebyshev, and conjugate gradient solvers, LASPack contains selected state-of-the-art algorithms which are commonly used for large sparse systems:
          o CG-like methods for non-symmetric systems: CGN, GMRES, BiCG, QMR, CGS, and BiCGStab,
    o multilevel methods such as the multigrid and conjugate gradient methods preconditioned by multigrid and BPX preconditioners.
      All the above solvers are applicable not only to the positive definite or non-symmetric matrices, but are also adopted for singular systems (e.g. arising from discretization of Neumann boundary value problems).
    * The implementation is based on an object-oriented approach (although it is programmed in C). Vectors and matrices are defined as new data types in connection with the corresponding supporting routines. The basic operations are implemented in such a way that they allow the programming of linear algebra algorithms in a natural way.
    * LASPack is extensible in a simple manner. An access to the internal representation of vectors and matrices is not necessary and is avoided, as required of the object-oriented programming. This allows an improvement of algorithms or a modification of data structures with no adjustment of application programs using the package.
    * LASPack is written in ANSI C and is thus largely portable. 

%prep
%setup -q -c -n laspack-%{version}
cp %{SOURCE1} COPYRIGHT

%build
export INCROOT=`pwd`
for makefiles in xc \
        laspack \
        laspack/examples/mlstest \
        laspack/examples/lastest \
        laspack/examples/vectopt \
        laspack/examples/matropt
do
	pushd $makefiles
	make INCROOT=$INCROOT LIBROOT="$INCROOT/laspack -L$INCROOT/xc" all
	popd
done

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_bindir},%{_includedir},%{_libdir}}
for makefiles in xc \
        laspack \
        laspack/examples/mlstest \
        laspack/examples/lastest \
        laspack/examples/vectopt \
        laspack/examples/matropt
do
        pushd $makefiles
        make LIBLOCAL=$RPM_BUILD_ROOT/%{_libdir} INCLOCAL=$RPM_BUILD_ROOT/%{_includedir} BINLOCAL=$RPM_BUILD_ROOT/%{_bindir}  install-local
        popd
done
rm -f laspack/html/form-mail.pl

%files
%defattr(-,root,root)
%doc COPYRIGHT readme laspack/doc/*.ps laspack/html/* 
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%changelog
* Thu May 01 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for RH 9

* Wed Jun 10 2002 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
