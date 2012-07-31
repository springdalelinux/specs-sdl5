%define __python /usr/bin/python26
%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')
Summary: Scipy: Scientific Tools for Python
Name: scipy26
Version: 0.8.0
Release: 3%{?dist}

Group: Development/Libraries
License: BSD and LGPLv2+
Url: http://www.scipy.org
Source0: http://prdownloads.sourceforge.net/scipy/scipy-%{version}.tar.gz
# Missing setup.py files which control the build of this module
# These should be removed as soon as upstream pushes a release with this fixed
Source1: stsci_image_setup.py
Source2: stsci_convolve_setup.py
Patch0: stsci_image_syntax.patch
Patch1: scipy_gcc43.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: numpy26, python26-devel,numpy26-f2py
BuildRequires: fftw-devel, blas-devel, lapack-devel, ufsparse-devel
BuildRequires: atlas-devel
BuildRequires: gcc-gfortran, swig
Requires: numpy26, python26,numpy26-f2py


%description
Scipy is open-source software for mathematics, science, and
engineering. The core library is NumPy which provides convenient and
fast N-dimensional array manipulation. The SciPy library is built to
work with NumPy arrays, and provides many user-friendly and efficient
numerical routines such as routines for numerical integration and
optimization. Together, they run on all popular operating systems, are
quick to install, and are free of charge. NumPy and SciPy are easy to
use, but powerful enough to be depended upon by some of the world's
leading scientists and engineers.


%prep 
%setup -q -n scipy-%{version}
#patch0 -p0
#patch1 -p1
cat > site.cfg << EOF
[amd]
library_dirs = %{_libdir}
include_dirs = /usr/include/suitesparse:/usr/include/ufsparse
amd_libs = amd

[umfpack]
library_dirs = %{_libdir}
include_dirs = /usr/include/suitesparse:/usr/include/ufsparse
umfpack_libs = umfpack
EOF

#cp %{SOURCE1} scipy/stsci/image/setup.py
#cp %{SOURCE2} scipy/stsci/convolve/setup.py

%build
env CFLAGS="$RPM_OPT_FLAGS" ATLAS=%{_libdir}/atlas FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} %{__python} setup.py config_fc --fcompiler=gnu95 --noarch build


%install
rm -rf $RPM_BUILD_ROOT
env CFLAGS="$RPM_OPT_FLAGS" ATLAS=%{_libdir}/atlas FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} %{__python} setup.py install --root=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files 
%defattr(-,root,root,-)
%doc LICENSE.txt
%{python_sitearch}/scipy
%{python_sitearch}/*.egg-info



%changelog
* Mon Apr 11 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.1-3
- Bump for rebuild against numpy 1.3 

* Thu Apr  1 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.1-2
- Bump for rebuild against numpy 1.4.0 

* Thu Dec 10 2009 Jon Ciesla <limb@jcomserv.net> - 0.7.1-1
- Update to 0.7.1.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14  2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-4
- Fix for gcc34 weave blitz bug #505379

* Tue Apr 7  2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-3
- Add f2py requires to prepared for numpy packaging split

* Sun Mar 1  2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-2
- Patch for stsci image function syntax fix.

* Thu Feb 26 2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-1
- Update to final 0.7 release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-0.3.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 0.7.0-0.2.b1
- Rebuild for atlas-3.8.2

* Mon Dec 01 2008  Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-0.1.b1
- Update to latest beta which lists python 2.6 support

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-8
- Rebuild for Python 2.6

* Fri Oct 03 2008 Jef Spaleta <jspaleta@fedoraproject.org> - 0.6.0-7
- fix the stsci fix

* Thu Oct 02 2008 Jef Spaleta <jspaleta@fedoraproject.org> - 0.6.0-6
- include missing setup files for stsci module

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.0-5
- Autorebuild for GCC 4.3

* Fri Jan 04 2008 Jef Spaleta <jspaleta@fedoraproject.org> - 0.6.0-4
- fix for egg-info file creation

* Wed Oct 03 2007 Jef Spaleta <jspaleta@gmail.com> - 0.6.0-3
- include_dirs changes for ufsparse change in development

* Tue Oct 02 2007 Jef Spaleta <jspaleta@gmail.com> - 0.6.0-2
- Fix licensing to match Fedora packaging guidance
- Remove unnecessary library deps

* Tue Sep 25 2007 Jarrod Millman <millman@berkeley.edu> - 0.6.0-1
- update to new upstream source
- update Summary, License, Url, and description
- added extra dependencies
- remove symlink since Lib has been renamed scipy

* Tue Aug 21 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2.1-1
- Update to new upstream source

* Tue Aug 21 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-3
- fix licensing tag and bump for buildid rebuild

* Wed Apr 18 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-2.2
- go back to using gfortran now that numpy is patched

* Sat Apr 14 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-2.1
- minor correction for f77 usage

* Sat Apr 14 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-2
- revert to f77 due to issue with numpy in development

* Sat Apr 14 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-1.1
- remove arch specific optimizations

* Wed Feb 21 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-1
- Update for new upstream release

* Mon Dec  11 2006 Jef Spaleta <jspaleta@gmail.com> - 0.5.1-5
- Bump for rebuild against python 2.5 in devel tree

* Sun Dec  3 2006 Jef Spaleta <jspaleta@gmail.com> - 0.5.1-4
- Minor adjustments to specfile for packaging guidelines. 
- Changed buildrequires fftw version 3  from fftw2

* Sat Dec  2 2006 Jef Spaleta <jspaleta@gmail.com> - 0.5.1-2
- Updated spec for FE Packaging Guidelines and for upstream version 0.5.1

* Mon May  8 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-4
- Add BuildRequires gcc-c++
- Add python-devel
- Add libstdc++

* Mon May  8 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-3
- Add BuildRequires gcc-gfortran

* Sun May  7 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-3
- Add BuildRequires numpy


* Wed May  3 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-2
- Fix BuildRoot
- Add BuildRequires, Requires
- Test remove d1mach patch
- Fix defattr
- Add changelog
- Removed Prefix, Vendor
- Fix Source0

