Name:           atlas
Version:        3.6.0
Release:        11%{?dist}
Summary:        Automatically Tuned Linear Algebra Software

Group:          System Environment/Libraries
License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:        README.Fedora
Patch0:         http://ftp.debian.org/debian/pool/main/a/atlas3/%{name}3_%{version}-20.diff.gz
Patch1:         %{name}-%{version}-gfortran.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       /etc/ld.so.conf.d
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  gcc-gfortran lapack-devel expect sharutils gawk
Obsoletes: ATLAS

%define ver_major 3
%define ver %{ver_major}.0

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration. In order to package ATLAS for Fedora some compromises
are necessary so that good performance can be obtained on a variety
of hardware. This set of ATLAS binary packages is therefore not
necessarily optimal for any specific hardware configuration.  However,
the source package can be used to compile customized ATLAS packages;
see the documentation for information.



%package devel
Summary:        Development libraries for ATLAS
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the static libraries and headers for development
with ATLAS (Automatically Tuned Linear Algebra Software).


############## Subpackages for architecture extensions #################
#
# Because a set of ATLAS libraries is a ~5 MB package, separate packages
# are created for SSE, SSE2, and 3DNow extensions to ix86 and AltiVec
# extensions to PowerPC.

%ifarch i386
%define archt i386
%define types base sse sse2 3dnow

%package sse
Summary:        ATLAS libraries for SSE extensions
Group:          System Environment/Libraries
%description sse
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the SSE extensions
to the ix86 architecture.
%package sse-devel
Summary:        Development libraries for ATLAS with SSE extensions
Group:          Development/Libraries
Requires:       %{name}-sse = %{version}-%{release}
%description sse-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the SSE extensions to the ix86 architecture.


%package sse2
Summary:        ATLAS libraries for SSE2 extensions
Group:          System Environment/Libraries
%description sse2
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the SSE2
extensions to the ix86 architecture.
%package sse2-devel
Summary:        Development libraries for ATLAS with SSE2 extensions
Group:          Development/Libraries
Requires:       %{name}-sse2 = %{version}-%{release}
%description sse2-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the SSE2 extensions to the ix86 architecture.


%package 3dnow
Summary:        ATLAS libraries for 3DNow extensions
Group:          System Environment/Libraries
%description 3dnow
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the 3DNow
extensions to the ix86 architecture.
%package 3dnow-devel
Summary:        Development libraries for ATLAS with 3DNow extensions
Group:          Development/Libraries
Requires:       %{name}-3dnow = %{version}-%{release}
%description 3dnow-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the 3DNow extensions to the ix86 architecture.


%endif
%ifarch ppc
%define archt powerpc
%define types base altivec

%package altivec
Summary:        ATLAS libraries for AltiVec extensions
Group:          System Environment/Libraries
%description altivec
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the AltiVec
extensions to the PowerPC architecture.
%package altivec-devel
Summary:        Development libraries for ATLAS with AltiVec extensions
Group:          Development/Libraries
Requires:       %{name}-altivec = %{version}-%{release}
%description altivec-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the AltiVec extensions to the PowerPC architecture.

%endif
%ifarch x86_64
%define archt amd64
%define types base
%define bit 2
%else
%define bit 1
%endif

%if "%{?enable_custom_atlas}" == "1"
# This flag enables building customized ATLAS libraries with all
# compile-time optimizations. Note that compilation will take a very
# long time, and that the resulting binaries are not guaranteed to
# work well or even at all on other hardware.

%define archt %{_arch}
%define types custom

%package custom
Summary:        Custom-compiled ATLAS libraries
Group:          System Environment/Libraries
%description custom
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with all compile-time optimizations enabled.
%package custom-devel
Summary:        Development libraries for ATLAS with AltiVec extensions
Group:          Development/Libraries
Requires:       %{name}-custom = %{version}-%{release}
%description custom-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
all compile-time optimizations enabled.
%endif


%prep
%setup -q -n ATLAS
%patch0 -p1
%patch1 -p0
cp %{SOURCE1} doc


%build
# The following build procedure is more or less copied from the Debian
# sources, where the output of a previously recorded build is
# replayed, so as to bypass the compile-time optimizations and produce
# predictable results independent of the hardware on which it is
# compiled. This forces builds to be sequential, so SMP builds are not
# supported.
chmod +x debian/config.expect debian/ab
sed -i debian/ab -e s/g77/gfortran/

########## Static Libraries ##########################################
for TYPE in %{types}; do
  if [ "$TYPE" = "3dnow" ]; then
    TDN=y
  else
    TDN=n
  fi
  BUILD_DIR=Linux_${TYPE}_static
  ARCH_DIR=$BUILD_DIR CACHE_SIZE= BIT=%{bit} \
    DEFAULTS=y TDNCOMP=$TDN debian/config.expect
  cat Make.$BUILD_DIR |\
	sed -e "s, TOPdir = \(.*\), TOPdir = `pwd`,1" \
	    -e "s, FLAPACKlib = , FLAPACKlib = %{_libdir}/liblapack.a,1" >foo
  mv foo Make.$BUILD_DIR
  make killall arch=$BUILD_DIR
  make startup arch=$BUILD_DIR

  if [ "$TYPE" = "custom" ]; then
    BUILD_DATA_DIR=atlas-$TYPE-%{archt}
    if [ -a %{_sourcedir}/$BUILD_DATA_DIR.tgz ]; then
      tar zxf %{_sourcedir}/$BUILD_DATA_DIR.tgz
    else
      make install arch=$BUILD_DIR >out 2>&1 &
      pid=$!
      echo Waiting on $pid
      tail -f --pid $pid out &
      wait $pid
      rm -rf ${BUILD_DATA_DIR}
      mkdir -p ${BUILD_DATA_DIR}
      cat out | sed -e "s,`pwd`,TOPDIR,g" -e "s,$BUILD_DIR,CARCH,g" | \
		gzip -9 | uuencode - >${BUILD_DATA_DIR}/build.uu
      rm -f out
      mkdir -p ${BUILD_DATA_DIR}/include
      cp include/$BUILD_DIR/* ${BUILD_DATA_DIR}/include
      mkdir -p ${BUILD_DATA_DIR}/mm
      cp tune/blas/gemm/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/mm
      mkdir -p ${BUILD_DATA_DIR}/mv
      cp tune/blas/gemv/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/mv
      mkdir -p ${BUILD_DATA_DIR}/r1
      cp tune/blas/ger/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/r1
      mkdir -p ${BUILD_DATA_DIR}/l1
      cp tune/blas/level1/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/l1
      tar zcf %{_sourcedir}/${BUILD_DATA_DIR}.tgz ${BUILD_DATA_DIR}
    fi
  else
    BUILD_DATA_DIR=debian/%{archt}/${TYPE}
  fi

  cp ${BUILD_DATA_DIR}/mm/* tune/blas/gemm/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/mv/* tune/blas/gemv/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/r1/* tune/blas/ger/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/l1/* tune/blas/level1/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/include/* include/$BUILD_DIR

  cat ${BUILD_DATA_DIR}/build.uu | uudecode | zcat - | \
	sed -e s/g77/gfortran/ -e s/-DAdd__/-DAdd_/ | debian/ab topdir=`pwd` \
	carch=$BUILD_DIR fpic="-Wa,--noexecstack" debug= | bash -x -e
  mv lib/$BUILD_DIR/liblapack.a lib/$BUILD_DIR/liblapack_atlas.a

  # Create replacement for BLAS and LAPACK Libraries
  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libatlas.a
    ar x ../lib/$BUILD_DIR/libf77blas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  rm -f lib/$BUILD_DIR/libblas.a
  ar r lib/$BUILD_DIR/libblas.a tmp/*.o
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x %{_libdir}/liblapack.a
    ar x ../lib/$BUILD_DIR/liblapack_atlas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  rm -f lib/$BUILD_DIR/liblapack.a
  ar r lib/$BUILD_DIR/liblapack.a tmp/*.o
  rm -rf tmp

  ########## Shared Libraries ##########################################
  BUILD_DIR=Linux_${TYPE}_shared
  ARCH_DIR=$BUILD_DIR CACHE_SIZE= BIT=%{bit} \
      DEFAULTS=y TDNCOMP=$TDN debian/config.expect
  cat Make.$BUILD_DIR |\
	sed -e "s, TOPdir = \(.*\), TOPdir = `pwd`,1" \
	    -e "s, FLAPACKlib = , FLAPACKlib = %{_libdir}/liblapack_pic.a,1" \
	    -e "s, F77FLAGS = \(.*\), F77FLAGS = \1 -fPIC,1" \
	    -e "s, CCFLAGS = \(.*\), CCFLAGS = \1 -fPIC,1" \
	    -e "s, MMFLAGS = \(.*\), MMFLAGS = \1 -fPIC,1" \
	    -e "s, XCCFLAGS = \(.*\), XCCFLAGS = \1 -fPIC,1" >foo
  mv foo Make.$BUILD_DIR
  make killall arch=$BUILD_DIR
  make startup arch=$BUILD_DIR

  cp ${BUILD_DATA_DIR}/mm/* tune/blas/gemm/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/mv/* tune/blas/gemv/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/r1/* tune/blas/ger/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/l1/* tune/blas/level1/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/include/* include/$BUILD_DIR

  cat ${BUILD_DATA_DIR}/build.uu | uudecode | zcat - | \
	sed -e s/g77/gfortran/ -e s/-DAdd__/-DAdd_/ | debian/ab topdir=`pwd` \
	carch=$BUILD_DIR fpic="-Wa,--noexecstack -fPIC" debug= | bash -x -e
  mv lib/$BUILD_DIR/liblapack.a lib/$BUILD_DIR/liblapack_atlas.a

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libatlas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=libatlas.so.%{ver_major} \
	-o lib/$BUILD_DIR/libatlas.so.%{ver} tmp/*.o -lm
  ln -s libatlas.so.%{ver} lib/$BUILD_DIR/libatlas.so.%{ver_major}
  ln -s libatlas.so.%{ver} lib/$BUILD_DIR/libatlas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libcblas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=libcblas.so.%{ver_major} \
	-o lib/$BUILD_DIR/libcblas.so.%{ver} tmp/*.o -L lib/$BUILD_DIR -latlas
  ln -s libcblas.so.%{ver} lib/$BUILD_DIR/libcblas.so.%{ver_major}
  ln -s libcblas.so.%{ver} lib/$BUILD_DIR/libcblas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libf77blas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=libf77blas.so.%{ver_major} \
	-o lib/$BUILD_DIR/libf77blas.so.%{ver} tmp/*.o \
	-L lib/$BUILD_DIR -latlas -lgfortran
  ln -s libf77blas.so.%{ver} lib/$BUILD_DIR/libf77blas.so.%{ver_major}
  ln -s libf77blas.so.%{ver} lib/$BUILD_DIR/libf77blas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/liblapack_atlas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=liblapack_atlas.so.%{ver_major} \
	-o lib/$BUILD_DIR/liblapack_atlas.so.%{ver} tmp/*.o \
	-L lib/$BUILD_DIR -lcblas -lf77blas
  ln -s liblapack_atlas.so.%{ver} lib/$BUILD_DIR/liblapack_atlas.so.%{ver_major}
  ln -s liblapack_atlas.so.%{ver} lib/$BUILD_DIR/liblapack_atlas.so
  rm -rf tmp

  # Create replacement for BLAS and LAPACK Libraries
  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libatlas.a
    ar x ../lib/$BUILD_DIR/libf77blas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  cc -shared -Wl,-soname=libblas.so.%{ver_major} \
	-o lib/$BUILD_DIR/libblas.so.%{ver} tmp/*.o -lgfortran
  ln -s libblas.so.%{ver} lib/$BUILD_DIR/libblas.so.%{ver_major}
  ln -s libblas.so.%{ver} lib/$BUILD_DIR/libblas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x %{_libdir}/liblapack_pic.a
    ar x ../lib/$BUILD_DIR/liblapack_atlas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  cc -shared -Wl,-soname=liblapack.so.%{ver_major} \
	-o lib/$BUILD_DIR/liblapack.so.%{ver} tmp/*.o \
	-L lib/$BUILD_DIR -lblas -lgfortran
  ln -s liblapack.so.%{ver} lib/$BUILD_DIR/liblapack.so.%{ver_major}
  ln -s liblapack.so.%{ver} lib/$BUILD_DIR/liblapack.so
  rm -rf tmp
done


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT%{_includedir}/atlas
cp -a include/*.h $RPM_BUILD_ROOT%{_includedir}/atlas

LIBNAMES="libatlas libcblas libf77blas liblapack_atlas libblas liblapack"
for TYPE in %{types}; do
  if [ "$TYPE" = "base" ]; then
    EXTDIR="atlas"
    echo "%{_libdir}/atlas" \
      > $RPM_BUILD_ROOT/etc/ld.so.conf.d/atlas-%{_arch}.conf
  elif [ "$TYPE" = "custom" ]; then
    EXTDIR="atlas-custom"
    echo "%{_libdir}/atlas-custom" \
      > $RPM_BUILD_ROOT/etc/ld.so.conf.d/atlas-custom-%{_arch}.conf
  else
    EXTDIR=$TYPE
    if [ "$TYPE" != "sse2" ]; then
      echo "/usr/lib/$TYPE" \
        > $RPM_BUILD_ROOT/etc/ld.so.conf.d/atlas-$TYPE.conf
    fi
  fi

  mkdir -p $RPM_BUILD_ROOT%{_libdir}/${EXTDIR}
  for LIB in $LIBNAMES; do
    LIBS="lib/Linux_${TYPE}_static/$LIB.a lib/Linux_${TYPE}_shared/$LIB.so*"
    cp -a $LIBS ${RPM_BUILD_ROOT}%{_libdir}/${EXTDIR}
  done
done



%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%ifarch i386

%post -n atlas-sse -p /sbin/ldconfig

%postun -n atlas-sse -p /sbin/ldconfig

%post -n atlas-sse2 -p /sbin/ldconfig

%postun -n atlas-sse2 -p /sbin/ldconfig

%post -n atlas-3dnow -p /sbin/ldconfig

%postun -n atlas-3dnow -p /sbin/ldconfig

%endif
%ifarch ppc

%post -n atlas-altivec -p /sbin/ldconfig

%postun -n atlas-altivec -p /sbin/ldconfig

%endif
%if "%{?enable_custom_atlas}" == "1"

%post -n atlas-custom -p /sbin/ldconfig

%postun -n atlas-custom -p /sbin/ldconfig

%files custom
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/atlas-custom
%{_libdir}/atlas-custom/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-custom-%{_arch}.conf

%files custom-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/atlas-custom
%{_libdir}/atlas-custom/*.so
%{_libdir}/atlas-custom/*.a
%{_includedir}/atlas

%else


%files
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

%files devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%{_libdir}/atlas/*.so
%{_libdir}/atlas/*.a
%{_includedir}/atlas

%ifarch i386

%files sse
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/sse
%{_libdir}/sse/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-sse.conf

%files sse-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/sse
%{_libdir}/sse/*.so
%{_libdir}/sse/*.a
%{_includedir}/atlas


%files sse2
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/sse2
%{_libdir}/sse2/*.so.*

%files sse2-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/sse2
%{_libdir}/sse2/*.so
%{_libdir}/sse2/*.a
%{_includedir}/atlas


%files 3dnow
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/3dnow
%{_libdir}/3dnow/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-3dnow.conf

%files 3dnow-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/3dnow
%{_libdir}/3dnow/*.so
%{_libdir}/3dnow/*.a
%{_includedir}/atlas

%endif
%ifarch ppc

%files altivec
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/altivec
%{_libdir}/altivec/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-altivec.conf

%files altivec-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/altivec
%{_libdir}/altivec/*.so
%{_libdir}/altivec/*.a
%{_includedir}/atlas

%endif

%endif

%changelog
* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-11
- Rebuild for FC6.
- Remove outdated comments from spec file.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-10
- Rebuild for Fedora Extras 5.
- Add --noexecstack to compilation of assembly kernels. These were
  previously marked executable, which caused problems with selinux.

* Mon Dec 19 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-9
- Rebuild for gcc 4.1.

* Mon Oct 10 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-8
- Make all devel subpackages depend on their non-devel counterparts.
- Add /etc/ld.so.conf.d files for -sse and -3dnow, because they don't
  seem to get picked up automatically.

* Wed Oct 05 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-7
- Forgot to add the new patch to sources.

* Tue Oct 04 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-6
- Use new Debian patch, and enable shared libs (they previously failed
  to build on gcc 4).
- Minor updates to description and README.Fedora file.
- Fix buildroot name to match FE preferred form.
- Fixes for custom optimized builds.
- Add dist tag.

* Wed Sep 28 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-5
- fix files lists.

* Mon Sep 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-4
- generate library symlinks earlier for the benefit of later linking steps.

* Wed Sep 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-3
- Change lapack dependency to lapack-devel, and use lapack_pic.a for
  building liblapack.so.

* Wed Sep 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-2
- Add "bit" macro to correctly build on x86_64.

* Tue Aug 16 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-1
- Initial version.
