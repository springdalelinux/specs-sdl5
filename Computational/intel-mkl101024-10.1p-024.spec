%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles/intel-mkl
%define modulesversion 10.1
%define modulesminorversion 024

Summary: Intel(R) Math Kernel Library 10.1 for Linux*
Name: intel-mkl101%{modulesminorversion}
Version: 10.1p
Release: %{modulesminorversion}.2%{?dist}
License: Copyright (c) 2008 Intel Corporation
Group: Development/Libraries
Vendor: Intel Corporation
URL: http://www.intel.com/software/products/perflib
Prefix: /opt/intel/mkl/10.1.0.%{modulesminorversion}
Source: intel-mkl101%{modulesminorversion}-10.1p-%{modulesminorversion}.noarch.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/sh
%ifarch i386
Provides: 32/libguide.so, 32/libiomp5.so, 32/libmkl.so, 32/libmkl_blacs_intelmpi.so, 32/libmkl_core.so, 32/libmkl_def.so, 32/libmkl_gf.so, 32/libmkl_gnu_thread.so, 32/libmkl_intel.so, 32/libmkl_intel_thread.so, 32/libmkl_lapack.so, 32/libmkl_p4.so, 32/libmkl_p4m.so, 32/libmkl_p4p.so, 32/libmkl_pgi_thread.so, 32/libmkl_scalapack_core.so, 32/libmkl_sequential.so, 32/libmkl_vml_def.so, 32/libmkl_vml_ia.so, 32/libmkl_vml_p4.so, 32/libmkl_vml_p4m.so, 32/libmkl_vml_p4m2.so, 32/libmkl_vml_p4m3.so, 32/libmkl_vml_p4p.so
%define intelbits 32
%define intellibdir 32
%endif
%ifarch x86_64
Provides: em64t/libguide.so, em64t/libiomp5.so, em64t/libmkl.so, em64t/libmkl_blacs_intelmpi_ilp64.so, em64t/libmkl_blacs_intelmpi_lp64.so, em64t/libmkl_core.so, em64t/libmkl_def.so, em64t/libmkl_gf_ilp64.so, em64t/libmkl_gf_lp64.so, em64t/libmkl_gnu_thread.so, em64t/libmkl_intel_ilp64.so, em64t/libmkl_intel_lp64.so, em64t/libmkl_intel_sp2dp.so, em64t/libmkl_intel_thread.so, em64t/libmkl_lapack.so, em64t/libmkl_mc.so, em64t/libmkl_mc3.so, em64t/libmkl_p4n.so, em64t/libmkl_pgi_thread.so, em64t/libmkl_scalapack_ilp64.so, em64t/libmkl_scalapack_lp64.so, em64t/libmkl_sequential.so, em64t/libmkl_vml_def.so, em64t/libmkl_vml_mc.so, em64t/libmkl_vml_mc2.so, em64t/libmkl_vml_mc3.so, em64t/libmkl_vml_p4n.so
%define intelbits 64
%define intellibdir em64t
%endif
%ifarch i386 x86_64
Provides: intel-mkl101%{modulesminorversion} = 10.1p-%{modulesminorversion}
%endif 
Requires: environment-modules >= 3.2.3
BuildRequires: findutils


%description
The Intel(R) Math Kernel Library (Intel(R) MKL) for Linux* is composed of highly
optimized mathematical functions for engineering, scientific and financial
applications requiring high performance on Intel(R) platforms. The functional
areas of the library include linear algebra consisting of LAPACK and BLAS,
Discrete Fourier Transforms (DFT), vector transcendental functions (vector math
library/VML), and vector statistical functions (VSL). Intel MKL is optimized for
the features and capabilities of the latest Intel microprocessors.

%package        devel
Summary:        Development files for intel-mkl100014 library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-devel-common = %{version}-%{release}
AutoReqProv: 0

%description    devel
Development files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux.

%package        benchmarks
Summary:        Arch specific benchmark files for intel-mkl100014 library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-benchmarks-common = %{version}-%{release}
AutoReqProv: 0

%description    benchmarks
Architecture specific benchmark files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux.

%ifarch noarch
%package        doc
Summary:        Documentation and examples for intel-mkl100014 library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
AutoReqProv: 0

%description    doc
Documentation and examples for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux.

%package        devel-common
Summary:        Non arch specific development files for intel-mkl100014 library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
AutoReqProv: 0

%description    devel-common
Non architecture specific development files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux.

%package        benchmarks-common
Summary:        Non arch specific benchmark files for intel-mkl100014 library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
AutoReqProv: 0

%description    benchmarks-common
Non architecture specific benchmark files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux.

%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
rm -rf opt/intel/mkl/*/lib/64 opt/intel/mkl/*/uninstall.sh
rm -rf opt/intel/mkl/*/benchmarks/linpack/*itanium opt/intel/mkl/*/benchmarks/mp_linpack/bin_intel/ipf
rm -rf opt/intel/mkl/*/tests/cblas/source/libcwrap_ipf.a
rm -rf opt/intel/mkl/*/tools/environment/mklvars64*
rm -rf opt/intel/mkl/*/tools/support
%ifarch i386
rm -rf opt/intel/mkl/*/lib/em64t
rm -rf opt/intel/mkl/*/benchmarks/linpack/*xeon64
rm -rf opt/intel/mkl/*/benchmarks/mp_linpack/bin_intel/em64t
rm -rf opt/intel/mkl/*/tests/cblas/source/libcwrap_em64t.a
rm -rf opt/intel/mkl/*/tools/environment/mklvarsem64t*
%endif
%ifarch x86_64
rm -rf opt/intel/mkl/*/lib/32
rm -rf opt/intel/mkl/*/benchmarks/linpack/*xeon32
rm -rf opt/intel/mkl/*/benchmarks/mp_linpack/bin_intel/ia32
rm -rf opt/intel/mkl/*/tests/cblas/source/libcwrap_ia32.a
rm -rf opt/intel/mkl/*/tools/environment/mklvars32*
%endif
%ifarch noarch
rm -rf opt/intel/mkl/*/lib
rm -rf opt/intel/mkl/*/benchmarks/linpack/*xeon32
rm -rf opt/intel/mkl/*/benchmarks/linpack/*xeon64
rm -rf opt/intel/mkl/*/benchmarks/mp_linpack/bin_intel
rm -rf opt/intel/mkl/*/tools/environment
%endif
%ifarch i386 x86_64
rm -rf opt/intel/mkl/*/{man,include,interfaces,examples,doc} opt/intel/mkl/*/tools/{builder,plugins}
find opt/intel/mkl/*/tests -type f | grep -v libcwrap_ | xargs rm -f
rm -rf `ls -d opt/intel/mkl/*/benchmarks/mp_linpack/*|grep -v bin_intel`
rm -rf opt/intel/mkl/*/benchmarks/linpack/*help*
%endif
# and now make sure we got the right permissions
chmod -R u+w,a+rX,og-w .
popd


%ifarch i386 x86_64
pushd $RPM_BUILD_ROOT
INSTALL_DIR=/`ls -d opt/intel/mkl/*`
popd
ENVDIR="$RPM_BUILD_ROOT/$INSTALL_DIR/tools/environment"

if [ -e "$ENVDIR" ]; then
    tdir=$(echo "$INSTALL_DIR" | sed -e"s/\// /g")
    new_dir=""
    for dirn in $tdir; do
	[ "x$dirn" == "x" ] || new_dir="$new_dir\/$dirn"
    done
    gresult=0
    for envfile in $(ls $ENVDIR | grep mklvars); do
	cp $ENVDIR/$envfile $ENVDIR/$envfile.old &>/dev/null
	lrst=$?
	if [ "x$lrst" == "x0" ]; then 
	    sed s/\<INSTALLDIR\>/$new_dir/g $ENVDIR/$envfile.old 2>/dev/null 1>$ENVDIR/$envfile
	    lrst=$?
	    [ "x$gresult" == "x0" ] && gresult=$lrst
	fi
	[ "x$gresult" == "x0" ] || break
    done
    if [ "x$gresult" != "x0" ]; then
	for old_envfile in $(ls $ENVDIR | grep old); do
	    prev_one=$(echo "$old_envfile" | sed -e"s/\.old//g")
	    if [ "x$prev_one" != "x" ]; then
		rm -f $ENVDIR/$prev_one &>/dev/null
		cp $ENVDIR/$old_envfile $ENVDIR/$prev_one &>/dev/null
		rm -f $ENVDIR/$old_envfile &>/dev/null
	    fi
	done
    else
	rm -f $ENVDIR/*.old &>/dev/null
    fi
fi

CMKL_SLINK=$(echo "$INSTALL_DIR" | sed -e"s/mkl/cmkl/g")
if [ ! -e "$CMKL_SLINK" ]; then
    top_dir=$(dirname "$CMKL_SLINK" 2>/dev/null)
    mkdir -p "$RPM_BUILD_ROOT/$top_dir"	&>/dev/null
    slresult=$?
    [ "x$slresult" == "x0" ] && ln -s "$INSTALL_DIR" "$RPM_BUILD_ROOT/$CMKL_SLINK" 2>/dev/null
fi

mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/%{modulesversion}/%{modulesminorversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/%{modulesversion}/%{modulesminorversion}/%{intelbits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## intel-mkl %{version} %{intelbits}bit modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Intel MKL libraries version %{version} %{intelbits} bits"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for Intel MKL libraries version %{version} %{intelbits} bit"

prepend-path    INCLUDE $INSTALL_DIR/include
prepend-path    CPATH   $INSTALL_DIR/include
prepend-path    FPATH   $INSTALL_DIR/include
prepend-path    LD_LIBRARY_PATH $INSTALL_DIR/lib/%{intellibdir}
prepend-path    LIBRARY_PATH    $INSTALL_DIR/lib/%{intellibdir}
prepend-path    MANPATH $INSTALL_DIR/man
setenv		OMP_NUM_THREADS	1
ENDDEFAULT

%endif

%clean
rm -rf $RPM_BUILD_ROOT
%ifarch noarch

%files doc
%defattr(0755,root,root,0644)
/opt/intel/mkl/*/doc
/opt/intel/mkl/*/examples

%files devel-common
%defattr(0755,root,root,-)
/opt/intel/mkl/*/man
/opt/intel/mkl/*/include
/opt/intel/mkl/*/interfaces
/opt/intel/mkl/*/tests
%exclude /opt/intel/mkl/*/tests/cblas/source/libcwrap_em64t.a
%exclude /opt/intel/mkl/*/tests/cblas/source/libcwrap_ia32.a
/opt/intel/mkl/*/tools

%files benchmarks-common
%defattr(0755,root,root,-)
/opt/intel/mkl/*/benchmarks

%else

%files
%defattr(0755,root,root)
%dir /opt/intel/mkl/*
%dir /opt/intel/mkl/*/lib
%ifarch i386
%dir /opt/intel/mkl/*/lib/32
/opt/intel/mkl/*/lib/32/lib*so
/opt/intel/mkl/*/lib/32/locale
%else
%dir /opt/intel/mkl/*/lib/em64t
/opt/intel/mkl/*/lib/em64t/lib*so
/opt/intel/mkl/*/lib/em64t/locale
%endif
/opt/intel/cmkl/*
%dir /opt/intel/mkl/*/tools
%dir /opt/intel/mkl/*/tools/environment
/opt/intel/mkl/*/tools/environment/mkl*
%dir %{modulesdestination}
%dir %{modulesdestination}/%{modulesversion}
%dir %{modulesdestination}/%{modulesversion}/%{modulesminorversion}
%{modulesdestination}/%{modulesversion}/%{modulesminorversion}/%{intelbits}

%files devel
%defattr(0755,root,root,-)
%ifarch i386
/opt/intel/mkl/*/lib/32/lib*a
/opt/intel/mkl/*/tests/cblas/source/libcwrap_ia32.a
%else
/opt/intel/mkl/*/lib/em64t/lib*a
/opt/intel/mkl/*/tests/cblas/source/libcwrap_em64t.a
%endif

%files benchmarks
%defattr(0755,root,root)
#/opt/intel/mkl/*/benchmarks/linpack/
%ifarch i386
/opt/intel/mkl/*/benchmarks/linpack/*xeon32
/opt/intel/mkl/*/benchmarks/mp_linpack/bin_intel/ia32
%else
/opt/intel/mkl/*/benchmarks/linpack/*xeon64
/opt/intel/mkl/*/benchmarks/mp_linpack/bin_intel/em64t
%endif

%endif

