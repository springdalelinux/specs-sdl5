# Define this to 1 if you want this RPM to install a modulefile.  Only
# used if install_in_opt is true.
# type: bool (0/1)
%{!?install_modulefile: %define install_modulefile 1}
# type: string (root path to install modulefiles)
%{!?modulefile_path: %define modulefile_path /usr/local/share/Modules/modulefiles/}
# type: string (subdir to install modulefile)
%{!?modulefile_subdir: %define modulefile_subdir mvapich2}
# type: string (name of modulefile)
%{!?modulefile_name: %define modulefile_name %{version}}
# The name of the modules RPM.  Can vary from system to system.
# type: string (name of modules RPM)
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}
# 32 or 64?
%ifarch %{ix86}
%define modulebits 32
%else
%define modulebits 64
%endif

# compiler for which we are doing this
%define compiler gcc

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilershort gcc
%if 0%{?suse_version}
# These days suse packages gfortran in gcc-fortran, just to make my life difficult
%define compilerruntimesection BuildRequires: gcc-fortran gcc-c++
%define compilerdevelsection Requires: gcc-fortran gcc-c++
%else
%if "%{?rhel}" == "4"
%define compilerruntimesection BuildRequires: gcc-g77 gcc-c++
%define compilerdevelsection Requires: gcc-g77 gcc-c++
%else
%define compilerruntimesection BuildRequires: gcc-gfortran gcc-c++
%define compilerdevelsection Requires: gcc-gfortran gcc-c++
%endif
%endif
%define compilerdocsection #nothing here
%define localdir /usr/local
# do nothing special for gcc for build prep
%define compilerbuildprep %{nil}
# we need a special ldflags
%define compilerldflags -Wl,-z,noexecstack
# this is for configuring modules
%define compilermodulename gcc
%define compilerloadmodule %{nil}
# and this is a list of conflicting modules
%define compilerconflictmodule mpich/ mpich2/ lam/ intel/ pgi/ openmpi/
%define compilermodulefile %{nil}
%endif
#
# Intel 9.1 compiler
%if "%{compiler}" == "intel91"
%define compilershort intel
%define compilershortversion intel-9
%if "%{?rhel}" == "4"
%define compilerruntimesection BuildRequires: intel-compiler91-default-modules\
Requires: intel-compiler91-default-modules\
Provides: mvapich2-intel-runtime = %{version}-091.%{release}
%else
%define compilerruntimesection BuildRequires: intel-compiler91-%{modulebits}-default-modules\
Requires: intel-compiler91-%{modulebits}-default-modules\
Provides: mvapich2-intel-runtime = %{version}-091.%{release}
%endif
%define compilerdevelsection Provides: mvapich2-intel-devel = %{version}-091.%{release}
%define compilerdocsection Provides: mvapich2-intel-doc = %{version}-091.%{release}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort F90=ifort; . /etc/profile.d/modules.sh; module load intel
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-9.1
%define compilerloadmodule module load intel/9.1/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ pgi/ openmpi/
%if "%{?rhel}" == "4"
# for our older clusters we want 9.1 intel to be default, at least for now
%define compilermodulefile .modulerc-intel-%{modulebits}-991-%{version}
%else
# not so for newer ones
%define compilermodulefile .modulerc-intel-%{modulebits}-091-%{version}
%endif
%endif
#
# Intel 10.0 compiler
%if "%{compiler}" == "intel101" || "%{compiler}" == "intel111"
# we will extract versions we need out of above string
%define intelmajor %( echo %{compiler} | cut -b6-7 )
%define intelminor %( echo %{compiler} | cut -b8 )
%define intelversion %{intelmajor}.%{intelminor}
%define intelversionnum %{intelmajor}%{intelminor}
%if "%{compiler}" == "intel111"
%define intelminrelease 038
%define extradevel -devel
%else
%define intelminrelease 001
%define extradevel %{nil}
%endif
%define compilershort intel
%define compilershortversion intel-%{intelmajor}
%define compilerruntimesection BuildRequires: compat-libstdc++-33 intel-compiler%{intelmajor}-%{modulebits}-default-modules%{extradevel} >= %{intelversion}-%{intelminrelease}\
Requires: intel-compiler%{intelmajor}-%{modulebits}-default-modules >= %{intelversion}\
Provides: mvapich2-intel-runtime = %{version}-%{intelversionnum}.%{release}
%define compilerdevelsection Provides: mvapich2-intel-devel = %{version}-%{intelversionnum}.%{release}\
Requires: intel-compiler%{intelmajor}-%{modulebits}-default-modules%{extradevel} >= %{intelversion}-%{intelminrelease}
%define compilerdocsection Provides: mvapich2-intel-doc = %{version}-%{intelversionnum}.%{release}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort F90=ifort; . /etc/profile.d/modules.sh; module load intel
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-%{intelversion}
%define compilerloadmodule module load intel/%{intelmajor}/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ pgi/ openmpi/
%define compilermodulefile .modulerc-intel-%{modulebits}-%{intelversionnum}-%{version}
%endif
#
# PGI compiler
%if "%{compiler}" == "pgi71" || "%{compiler}" == "pgi80"
# we will extract versions we need out of above string
%define pgimajor %( echo %{compiler} | cut -b4 )
%define pgiminor %( echo %{compiler} | cut -b5 )
%define pgiversion %{pgimajor}.%{pgiminor}
%define pgiversionnum 0%{pgimajor}%{pgiminor}
%define compilershort pgi
%define compilershortversion pgi-%{pgimajor}
%define compilerruntimesection BuildRequires: pgi-workstation >= %{pgiversion}\
Requires: pgi-workstation-libs >= %{pgiversion}\
Provides: mvapich2-pgi-runtime = %{version}-%{pgiversionnum}.%{release}
%define compilerdevelsection Requires: pgi-workstation >= %{pgiversion}\
Provides: mvapich2-pgi-devel = %{version}-%{pgiversionnum}.%{release}
%define compilerdocsection Provides: mvapich2-pgi-doc = %{version}-%{pgiversionnum}.%{release}
%define localdir /usr/local/pgi
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pgcc CXX=pgCC F77=pgf77 F90=pgf90; . /etc/profile.d/modules.sh; module load pgi
%define cflags -fast
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pgi-%{pgiversion}
%define compilerloadmodule module load pgi/%{pgimajor}/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ intel/ openmpi/
%define compilermodulefile .modulerc-pgi-%{modulebits}-%{pgiversionnum}-%{version}
%endif
#
# Pathscale compiler
%if "%{compiler}" == "pathscale32"
# we will extract versions we need out of above string
%define pathscalemajor %( echo %{compiler} | cut -b10 )
%define pathscaleminor %( echo %{compiler} | cut -b11 )
%define pathscaleversion %{pathscalemajor}.%{pathscaleminor}
%define pathscaleversionnum 0%{pathscalemajor}%{pathscaleminor}
%define compilershort pathscale
%define compilershortversion pathscale-%{pathscalemajor}
%define compilerruntimesection BuildRequires: pathscale-compilers >= %{pathscaleversion}\
Requires: pathscale-compilers-libs >= %{pathscaleversion}\
Provides: mvapich2-pathscale-runtime = %{version}-%{pathscaleversionnum}.%{release}
%define compilerdevelsection Requires: pathscale-compilers >= %{pathscaleversion}\
Provides: mvapich2-pathscale-devel = %{version}-%{pathscaleversionnum}.%{release}
%define compilerdocsection Provides: mvapich2-pathscale-doc = %{version}-%{pathscaleversionnum}.%{release}
%define localdir /usr/local/pathscale
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pathcc CXX=pathCC F77=pathf90 F90=pathf90; . /etc/profile.d/modules.sh; module load pathscale
%define cflags -O3
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pathscale-%{pathscaleversion}
%define compilerloadmodule module load pathscale/%{pathscaleversion}/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ intel/ openmpi/
%define compilermodulefile .modulerc-pathscale-%{modulebits}-%{pathscaleversionnum}-%{version}
%endif

# with pvfs2?
%if 0%{?suse_version}
%{!?pvfs2: %define pvfs2 0}
%else
%{!?pvfs2: %define pvfs2 1}
%endif

# with lustre?
%{!?lustre: %define lustre 1}

# we need this for backwards compatibility
# before RHEL5 we had /usr/local/intel/mvapich2-intel and now we have /usr/local/intel/mvapich2
# i.e. the duplicate -intel has been dropped.  Act accordingly to distro:
%if "%{?rhel}" == "4"
# now, here it gets stupidly complex, as we used to have intel-ib and gcc-ib and
# these builds all use ib we have to add -ib in those cases...
%if "%{compilershort}" == "intel" || "%{compilershort}" == "gcc"
%define localdirlib %{localdir}/%{_lib}/mvapich2-%{compilershort}-ib
%else
%define localdirlib %{localdir}/%{_lib}/mvapich2-%{compilershort}
%endif
%else
%define localdirlib %{localdir}/%{_lib}/mvapich2
%endif

%define _prefix /usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}
%define _sysconfdir %{_prefix}/etc
%define _mandir %{_prefix}/man
%define _docdir %{_datadir}/doc
%define _infodir %{_datadir}/info

Summary: OSU MVAPICH2 MPI package
License: BSD
Group: Development/Libraries
Name: mvapich2-%{compiler}
Version: 1.4.1
Release: 3%{?dist}
Source: mvapich2-%{version}.tgz
Patch0: mvapich2-make.patch
URL: http://mvapich.cse.ohio-state.edu/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibumad-devel libibverbs-devel librdmacm-devel
ExclusiveArch: i386 ia64 x86_64
%if %{install_modulefile}
BuildRequires: %{modules_rpm_name}
%endif
%{compilerruntimesection}
%if 0%{?suse_version} || "%{?rhel}" < "5"
BuildRequires: numactl
Requires: numactl
%else
BuildRequires: numactl-devel
Requires: numactl-devel
Requires: librdmacm
%endif
%if 0%{?suse_version}
BuildRequires: sysfsutils, libibverbs-devel
%else
%if "%{?rhel}" < "5"
BuildRequires: sysfsutils-devel
%else
BuildRequires: libsysfs-devel
%endif
%endif
%if %{install_modulefile}
Requires: %{modules_rpm_name}
%endif
%if %{pvfs2}
BuildRequires: pvfs2-devel
%endif
%if %{lustre}
BuildRequires: lustre18-devel
%endif

%description
This is an MPI-2 implementation which includes all MPI-1 features.  It is
based on MPICH2 and MVICH.

%package devel
Summary: Development tools and header files for mvapich2 with %{compiler} compiler
Group: Development/Libraries
Requires: %{name} torque-devel libibumad-devel libibverbs-devel librdmacm-devel
%{compilerdevelsection}
Provides: mvapich2-%{compiler}-devel = %{version}
%if %{pvfs2}
Requires: pvfs2-devel
%endif
Requires: mvapich2-%{compiler} = %{version}-%{release}

%description devel
Development and doc files for mvapich2.

%prep
%setup -q -n mvapich2-%{version}
#patch0 -p1 -b .make

%build
# Kill the stack protection and fortify source stuff...it slows things down
# and mvapich2 hasn't been audited for it yet
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`

CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS} -I%{localdir}/include"
CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS} -I%{localdir}/include"
F77FLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS} -I%{localdir}/include"
FFLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS} -I%{localdir}/include"
F90FLAGS="%{?fcflags:%{fcflags}}%{!?fcflags:$RPM_OPT_FLAGS} -I%{localdir}/include"
LIBS="-lpthread -L%{localdir}/%{_lib} -L%{localdirlib} %{?pvfs2:-lpvfs2}"

%{compilerbuildprep}

export CFLAGS CXXFLAGS F77FLAGS F90FLAGS FFLAGS LIBS

%configure --with-rdma=gen2 --enable-f77 --enable-f90 --enable-cxx --enable-romio --with-file-system=nfs+ufs%{?lustre:+lustre}%{?pvfs2:+pvfs2} --enable-sharedlibs=gcc
make

%install
rm -fr %{buildroot}
make DESTDIR=%{buildroot} install

# we use this in libs compiled with mvapich2
mkdir -p %dir $RPM_BUILD_ROOT/%{localdirlib}
mkdir -p %dir $RPM_BUILD_ROOT/%{localdir}/include

%if %{install_modulefile}
%{__mkdir_p} $RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}

cat <<EOF >$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}/%{modulebits}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds MVAPICH2 %{compilermodulename} %{version} to various paths"
}  

module-whatis   "Sets up MVAPICH2 %{compilermodulename} %{version} in your environment"

# We check to see if any incompatible intel compilers are loaded
if {[module-info mode load] && ![module-info mode remove]} {
  if {[info exists env(LOADEDMODULES)]} {
    set envloaded [split \$env(LOADEDMODULES) ":"]
    foreach mod [lsort -decreasing \$envloaded] {
      set mmod "\$mod/"
      # if an mpich module and it is different from us - then it conflicts, easy
      if {[string first "mvapich2/" \$mmod] == 0 && [string first "mvapich2/%{compilermodulename}/%{version}/%{modulebits}" \$mmod] != 0 } {
        puts stderr "Conflicting module \$mod - removing before inserting requested module mvapich2/%{compilermodulename}/%{version}/%{modulebits}"
        module unload \$mod
      }
    }
    foreach conflicts [ split "%{compilerconflictmodule}" " " ] {
      set envloaded [split \$env(LOADEDMODULES) ":"]
      foreach mod [lsort -decreasing \$envloaded] {
        set mmod "\$mod/"
        if {[string first \$conflicts \$mmod] == 0} {
          puts stderr "Conflicting module \$mmod - removing before inserting requested module mvapich2/%{compilermodulename}/%{version}/%{modulebits}"
          module unload \$mod
          }
      }
    }
  }
}


%{compilerloadmodule}
prepend-path PATH "%{_prefix}/bin"
prepend-path LD_LIBRARY_PATH "%{_libdir}:%{localdirlib}"
prepend-path MANPATH "%{_mandir}"
append-path -delim { } LOCAL_LDFLAGS "-L%{_libdir} -L%{localdirlib}"
append-path -delim { } LOCAL_INCLUDE "-L%{localdir}/include"
EOF
%endif
# End of modulefile if
%if "%{compilermodulefile}" != ""
cat <<ENDMODULEFILETRICK >$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
#%Module
module-alias mvapich2/%{compilershort} mvapich2/%{compilermodulename}
module-alias mvapich2/%{compilershortversion} mvapich2/%{compilermodulename}
ENDMODULEFILETRICK
%if "%{?rhel}" == "4"
%if "%{compiler}" == "intel91"
# one more tweak
cat <<ENDMODULERHEL4INTEL91 >>$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
module-alias mvapich2 mvapich2/%{compilermodulename}
ENDMODULERHEL4INTEL91
%endif
%endif

%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir /usr/local/mvapich2
%dir /usr/local/mvapich2/%{version}
%dir /usr/local/mvapich2/%{version}/%{compiler}
%dir /usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}
%dir /usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin
%dir /usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/%{_lib}
%dir /usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/etc
%dir %{localdir}/include
%dir %{localdir}/%{_lib}
%dir %{localdirlib}
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/c*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpd*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpiexec*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpirun*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpiname
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpispawn
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/parkill
#/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/%{_lib}/lib*so.1*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/etc/mpe*
%if %{install_modulefile}
%dir %{modulefile_path}/%{modulefile_subdir}
%dir %{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}
%dir %{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}
%{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}/%{modulebits}
%if "%{compilermodulefile}" != ""
%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
%endif
%endif

%files devel
%defattr(-,root,root,-)
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpecc*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpefc*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpic*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/bin/mpif*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/etc/mpi*
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/include
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/man
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/%{_lib}/lib*.a
#/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/%{_lib}/lib*.so
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/%{_lib}/mpe_prof.o
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/%{_lib}/pkgconfig
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/share
/usr/local/mvapich2/%{version}/%{compiler}/%{_target_cpu}/sbin

%changelog
* Thu Oct 16 2008 Doug Ledford <dledford@redhat.com> - 1.0.3-3
- Make sure MPD_BIN is set in the mpivars files
- Related: bz466390

* Fri Oct 03 2008 Doug Ledford <dledford@redhat.com> - 1.0.3-2
- Make scriptlets match mvapich
- Include a Requires(post) and Requires(preun) so installs work properly
- Resolves: bz465448

* Thu Sep 18 2008 Doug Ledford <dledford@redhat.com> - 1.0.3-1
- Initial rhel5 package
- Resolves: bz451477

* Sun May 04 2008 Jonathan Perkins <perkinjo@cse.ohio-state.edu>
- Created initial MVAPICH2 1.0.3 SRPM with IB and iWARP support.

