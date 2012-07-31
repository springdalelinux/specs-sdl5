%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define __os_install_post %{nil}

# change to set default install location
%define installdest /opt/intel/mkl/9.0

Name:           intel-mkl-ilp64
Summary:        ILP64 versions of the BLAS, LAPACK, ScaLAPACK, and FFT libraries
License:        Intel
Group:          Development
Version:        9.0p
Release:        2.PU_IAS.2cluster
Source0:        l_mkl_ilp64_p_9.0.002.zip
BuildRoot:      /var/tmp/%{name}-%{version}-%{release}
Requires:	intel-mkl
BuildArch:	noarch
AutoReqProv:	0

%description
The libraries provided in this package are ILP64 versions of the BLAS, 
LAPACK, ScaLAPACK (available for use with the cluster edition), and 
FFT libraries in the Intel® Math Kernel Library 9.0 for Linux*. In 
this version of the library, parameters with FORTRAN type INTEGER or 
C type int should be read as INTEGER*8 or long respectively. 

Note: This package only contains a subset of the full Intel MKL library 
binaries and hence requires the full version of Intel MKL be installed first.

%prep
# do not uncompress, we will do it manually
%setup -c -T

%build
# nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdest}
cd $RPM_BUILD_ROOT%{installdest}
unzip %{SOURCE0}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{installdest}/*

%changelog
* Tue Dec 12 2006 Josko Plazonic <plazonic@math.princeton.edu>
- make the rpm build as noarch to match intel-mkl - bad but
  what can we do

* Mon Dec 11 2006 Dennis McRitchie <dmcr@Princeton.EDU>
- initial build
