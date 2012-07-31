%define __python /usr/bin/python26
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:		healpy26
Version:	0.9.6.1	
Release:	6%{?dist}
Summary:	A python wrapper of the healpix library	

Group:		Applications/Engineering	
License:	GPLv2+	
URL:		http://code.google.com/p/healpy/	
Source0:	http://healpy.googlecode.com/files/healpy-%{version}.tar.gz
Patch:		healpy-0.9.6-fedoralib.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python26-devel >= 2.4 
BuildRequires:	healpix-c++-devel >= 2.11 
BuildRequires:	cfitsio-devel
BuildRequires:	numpy26 >= 1.0.1 
Requires:	numpy26 >= 1.0.1 
Requires:	python26-matplotlib >= 0.98.4
Requires:	pyfits26 

%description
Healpy provides a python package to manipulate healpix maps. It is based
on the standard numeric and visualisation tools for Python, Numpy and
matplotlib.  To find find more information about Healpix, please visit
its home page at http://healpix.jpl.nasa.gov/. 

%prep
%setup -q -n healpy-%{version}

# Patch healpy to build against Fedora's healpix-c++ and cfitsio librarys.
%patch -p1 -b .fedoralib

# Move COPYING file to top of directory
cp -p hpbeta/COPYING .

# Physically remove the directory containing healpy's healpix-c++ and cfitsio.
rm -rf hpbeta/


%build
export CC="gcc"
export CXX="g++"
export CFLAGS="%{optflags} -fopenmp"
export CXXFLAGS="$CFLAGS"

%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

chmod 755 %{buildroot}%{python_sitearch}/healpy/*.so


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc PKG-INFO ChangeLog test/test_fit_dipole.py COPYING
%{python_sitearch}/*egg-info
%{python_sitearch}/healpy/


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6.1-3
- Changed name back to healpy

* Tue Jun 16 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6.1-2
- Changed permissions on *.so files to '755'
- Add ChangeLog and test/test_fit_dipole.py to %%doc.
- Add COPYING to documentation

* Fri Jun 12 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6.1-1
- New upstream release.
- Added CFLAGS and CXXFLAGS
- Added -fopenmp to build FLAGS
- Added minimum dependency package versions as recommended by upstream.

* Mon Jun 8 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6-4
- Removed cfitsio and healpix-c++ from Requires.
- Added numpy to BuildRequires 

* Mon Jun 8 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6-3
- Removed cfitsio and healpix-c++ from Requires.
- Removed INSTALL from %%doc section.
- Remove healpix and cfitso libraries from tarball during build.

* Mon Jun 8 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6-2
- Patch healpy to build against Fedora's healpix-c++ and cfitsio librarys.

* Sun Jun 7 2009 Joseph Smidt <josephsmidt@gmail.com> 0.9.6-1
- Initial RPM release.
