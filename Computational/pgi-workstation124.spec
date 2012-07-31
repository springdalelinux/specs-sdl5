%define modulesdestination /opt/share/Modules/modulefiles

# The name of the modules RPM
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}

%ifarch %{ix86}
%define pgibits 32
%define liblf liblf
%else
%define pgibits 64
%define liblf libso
%endif

Summary: PGI Workstation Compilers
Version: 12.4
%define numversion %( echo %{version} | tr -d . )
%define year 2012
Name: pgi-workstation%{numversion}
%define shortversion %( echo %{version} | cut -d. -f1 )
%define numversion %( echo %{version} | tr -d . )
Release: 7%{?dist}
Group: Development/Language
%define destdir /opt/pgi/%{version}
%ifarch %{ix86}
%define fulldir %{destdir}/linux86/%{version}
%define fulldirv %{destdir}/linux86/%{year}
%endif
%ifarch x86_64
%define fulldir %{destdir}/linux86-64/%{version}
%define fulldirv %{destdir}/linux86-64/%{year}
%endif
Source0: pgilinux-%{year}-%{numversion}.tar.gz
#Source1: pthread.h
License: Commercial
URL: http://www.pgroup.com/
BuildRoot: %{_tmppath}/%{name}-root
# do not do anything to files, no stripping or debuginfo
%define __os_install_post %{nil}
%define debug_package %{nil}
AutoReqProv: 0
BuildRequires: numactl gcc perl symlinks expect hardlink symlinks
BuildRequires: /usr/lib/crt1.o
%if 0%{?rhel} && "%rhel" > "4"
BuildRequires: numactl-devel gcc-gfortran
Requires: numactl-devel gcc-gfortran
%endif
Requires: numactl gcc
Requires: %{name}-libs = %{version}-%{release}
Requires: pgi-license
Provides: pgi-workstation = %{version}-%{release}
Provides: pgi-workstation = %{version}
Provides: %{name} = %{version}

%description
PGI compilers and tools.

%package doc
Summary: PGI Workstation Compiler documentation
Group: Development/Language
AutoReqProv: 0
Requires: %{name} = %{version}-%{release}
Provides: %{name}-doc = %{version}

%description doc
Documentation for PGI compilers and tools.

%package libs
Summary: PGI Workstation Compiler libraries
Group: Development/Language
#Provides: libpgbind.so libpgc.so libpgnuma.so
Requires: %{modules_rpm_name}
AutoReqProv: 0
Provides: pgi-workstation-libs = %{version}-%{release}
Provides: pgi-workstation-libs = %{version}
Provides: %{name}-libs = %{version}
%ifarch %{ix86}
Provides: gdix86.so libpgbind.so libpgc.so
%endif
%ifarch x86_64
Provides: gdix86-64.so()(64bit) libC.so()(64bit) libpgbind.so()(64bit) libpgc.so()(64bit)
Provides: libpgf90.so()(64bit) libpgf902.so()(64bit) libpgf90_prof.so()(64bit) libpgf90_rpm1.so()(64bit)
Provides: libpgf90_rpm1_p.so()(64bit) libpgf90rtl.so()(64bit) libpgftnrtl.so()(64bit) libpghpf.so()(64bit)
Provides: libpghpf2.so()(64bit) libpghpf_mpi.so()(64bit) libpghpf_mpi_p.so()(64bit) libpgmp.so()(64bit)
Provides: libpghpf_prof.so()(64bit) libpghpf_rpm.so()(64bit) libpghpf_rpm1.so()(64bit) libpghpf_rpm1_p.so()(64bit)
Provides: libpghpf_rpm_p.so()(64bit) libpghpf_smp.so()(64bit) libpghpf_smp_p.so()(64bit) libpgnod_prof.so()(64bit)
Provides: libpgnod_prof_g.so()(64bit) libpgnod_prof_papi.so()(64bit) libpgnod_prof_pfo.so()(64bit) 
Provides: libpgnod_prof_time.so()(64bit) libstd.so()(64bit)  
%endif

%description libs
Various shared libraries for PGI compilers.

%package acml
Summary: PGI Workstation Compiler ACML libraries
Group: Development/Language
Provides: libacml.a libacml_mp.a acml.h
%ifarch x86_64
Provides: libacml.so libacml_mv.so libacml_mp.so libacml_mv.a acml_mv.h acml_mv_m128.h
%endif
Requires: %{name}-libs = %{version}-%{release}
Provides: pgi-workstation-acml = %{version}-%{release}
Provides: pgi-workstation-acml = %{version}
Provides: %{name}-acml = %{version}
AutoReqProv: 0

%description acml
PGI Workstation Compiler ACML libraries

%package cuda
Summary: PGI Workstation Compiler Cuda
Group: Development/Language
Requires: %{name}-libs = %{version}-%{release}
Provides: pgi-workstation-cuda = %{version}-%{release}
Provides: pgi-workstation-cuda = %{version}
Provides: %{name}-cuda = %{version}
AutoReqProv: 0

%description cuda
PGI Workstation Compiler Cuda libraries and development files

%prep
%setup -q -c -n %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT%{destdir}
mkdir -p $RPM_BUILD_ROOT%{destdir}

cat > do_expect_install <<ENDEXPECT
#!/usr/bin/expect
set timeout 600
spawn ./install
expect "More--"
send "q"
expect accept
send "accept\r"
expect "Please choose install option:"
send "1\r"
expect "Installation directory"
send "$RPM_BUILD_ROOT%{destdir}\r"
expect "Install the ACML"
send "y\r"
expect "More--"
send "q"
expect accept
send "accept\r"
# this is whether to install acml 4.4.0 or 5.1.0 or 5.1.0 using FMA4, 1 is default 4.4.0
expect "Enter another value to override the default"
send "1\r"
expect "Install CUDA Toolkit Components"
send "y\r"
expect "More--"
send "q"
expect accept
send "accept\r"
expect "Install OpenACC compilers"
send "y\r"
expect "More--"
send "q"
expect accept
send "accept\r"
expect "Install JAVA JRE"
send "y\r"
expect "More--"
send "q"
expect accept
send "accept\r"
expect "Do you wish to update"
send "y\r"
expect "Do you wish to install MPICH"
send "n\r"
expect "Do you wish to generate license keys"
send "n\r"
expect "Do you want the files in the install directory to be"
send "n\r"
ENDEXPECT
chmod +x do_expect_install
./do_expect_install

%ifarch x86_64
rm -rf $RPM_BUILD_ROOT%{destdir}/linux86
%endif
# now fixup references to $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -exec grep -r $RPM_BUILD_ROOT '{}' \; -exec perl -pi -e "s,$RPM_BUILD_ROOT,,g" '{}' \;

# compress by hand our man pages
find $RPM_BUILD_ROOT%{fulldir}/man/ -type f -exec gzip -9 {} \;

# some symlinks point to under $RPM_BUILD_ROOT, fix them
symlinks -cr $RPM_BUILD_ROOT%{destdir}

hardlink $RPM_BUILD_ROOT%{destdir}

mv $RPM_BUILD_ROOT%{destdir}/{INSTALL*,S*,license*} $RPM_BUILD_ROOT%{fulldir}

# Modules stuff
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{version}
cat > $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{version}/%{pgibits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{compiler} %{intelversion} %{inteltype} %{pgibits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using PGI Workstation compilers %{version} %{pgibits} bits"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for the PGI Workstation compilers %{version} %{pgibits} bits"
prepend-path    PATH            %{fulldir}/bin
prepend-path    MANPATH         %{fulldir}/man
prepend-path    LD_LIBRARY_PATH %{fulldir}/lib:%{fulldir}/%{liblf}:%{fulldirv}/cuda/4.0/%{_lib}:%{fulldirv}/cuda/4.1/%{_lib}
prepend-path    LM_LICENSE_FILE /opt/pgi/license.dat
set     version      "3.2.3"
ENDDEFAULT

cat > $RPM_BUILD_ROOT%{modulesdestination}/pgi/.modulerc-pgi-%{numversion}-%{pgibits} <<ENDGENERIC
#%Module
module-alias pgi/%{shortversion} pgi/%{version}
ENDGENERIC
mkdir $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{shortversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{shortversion}/.modulerc-pgi-%{numversion}-%{pgibits} <<ENDMOREGENERIC
#%Module
module-alias pgi/%{shortversion}/%{pgibits} pgi/%{version}/%{pgibits}
ENDMOREGENERIC

## finally install the pthread.h workaround in the includedir
#install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{fulldir}/include/

# make sure files can be read
chmod -R a+rX,og-w,u+w $RPM_BUILD_ROOT%{destdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc %{fulldir}/*LICENSE*
%doc %{fulldir}/man/*
%{fulldir}/bin/*
%{fulldir}/bin/.p*
%exclude %{fulldir}/bin/pgcudainit
%{fulldir}/etc
%{fulldir}/include 
%{fulldir}/include_acc
%{fulldir}/jre
%{fulldir}/lib*/*
%{fulldir}/src
# the following are packaged in other subrpms
%exclude %{fulldir}/lib*/*.so
%exclude %{fulldir}/include/acml*
%exclude %{fulldir}/lib/libacml*
%ifarch x86_64
%exclude %{fulldir}/libso/libacml*
%{fulldir}/cray
%endif
# more complicated stuff
%{fulldirv}/*
%exclude %{fulldirv}/bin
%exclude %{fulldirv}/cuda
%exclude %{fulldirv}/man
%exclude %{fulldirv}/lib*
%exclude %{fulldirv}/doc
%exclude %{fulldirv}/acml
%exclude %{fulldirv}/EXAMPLES
%exclude %{fulldirv}/index.htm
%exclude %{fulldirv}/REDIST
%exclude %{fulldirv}/REDIST-RLR
%ifarch %{ix86}
%exclude %{fulldirv}/PORTABLE
%endif

%files libs
%defattr(-,root,root)
%dir %{destdir}
%dir %{destdir}/linux*
%dir %{fulldirv}
%dir %{fulldir}
%ifarch %{ix86}
%{fulldir}/PORTABLE
%endif
%{fulldir}/REDIST
%{fulldir}/REDIST-RLR
%dir %{fulldir}/lib*
%{fulldir}/lib*/*.so
%dir %{fulldir}/bin
%{fulldir}/bin/pgcudainit
%dir %{fulldir}/man
%dir %{modulesdestination}/pgi
%dir %{modulesdestination}/pgi/%{version}
%{modulesdestination}/pgi/%{version}/%{pgibits}
%dir %{modulesdestination}/pgi/%{shortversion}
%{modulesdestination}/pgi/.modulerc-pgi-%{numversion}-%{pgibits}
%{modulesdestination}/pgi/%{shortversion}/.modulerc-pgi-%{numversion}-%{pgibits}
%{fulldirv}/bin
%{fulldirv}/man
%{fulldirv}/lib*
%ifarch %{ix86}
%{fulldirv}/PORTABLE
%endif
%{fulldirv}/REDIST
%exclude %{fulldir}/lib*/libacml*
%{fulldirv}/cuda/*/lib*/lib*so*

%files doc
%defattr(-,root,root)
%doc %{fulldir}/doc
%doc %{fulldir}/index.htm
%doc %{fulldir}/EXAMPLES
%doc %{fulldir}/INSTALL.txt 
%doc %{fulldir}/SUBSCRIPTION_SERVICE
%doc %{fulldir}/license.info
%{fulldirv}/doc
%{fulldirv}/EXAMPLES
%{fulldirv}/index.htm

%files acml
%defattr(-,root,root)
%{fulldirv}/acml
%{fulldir}/include/acml*
%{fulldir}/lib/libacml*
%ifarch x86_64
%{fulldir}/libso/libacml*
%endif

%files cuda
%defattr(-,root,root)
%{fulldirv}/cuda
%exclude %{fulldirv}/cuda/*/lib*/lib*so*

%changelog
* Tue Jul 07 2005 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
