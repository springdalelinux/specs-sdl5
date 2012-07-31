%define __python /usr/bin/python26
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

#uncomment next line for a release candidate or a beta
%global relc rc1

Name:           numpy26
Version:        1.5.1
Release:        0.1%{?dist}
Epoch:		1
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
License:        BSD
URL:            http://numeric.scipy.org/
Source0:        http://downloads.sourceforge.net/numpy/numpy-%{version}%{?relc}.tar.gz

BuildRoot:      %{_tmppath}/numpy-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python26-devel lapack-devel python26-setuptools gcc-gfortran atlas-devel python26-nose
Requires:      python26-nose

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package f2py
Summary:        f2py for numpy
Group:          Development/Libraries
Requires:       numpy26 = %{epoch}:%{version}-%{release}
Requires:       python26-devel
Provides:       f2py
Obsoletes:      f2py <= 2.45.241_1927

%description f2py
This package includes a version of f2py that works properly with NumPy.

%if 0%{?with_python3}
%package -n python3-numpy
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
License:        BSD
%description -n python3-numpy
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package -n python3-numpy-f2py
Summary:        f2py for numpy
Group:          Development/Libraries
Requires:       python3-numpy = %{epoch}:%{version}-%{release}
Requires:       python3-devel
Provides:       python3-f2py
Obsoletes:      python3-f2py <= 2.45.241_1927

%description -n python3-numpy-f2py
This package includes a version of f2py that works properly with NumPy.
%endif # with_python3

%prep
%setup -q -n numpy-%{version}%{?relc}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py build
popd
%endif # with _python3

env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py build

%install
rm -rf %{buildroot}
# first install python3 so the binaries are overwritten by the python2 ones

#%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# skip-build currently broken, this works around it for now
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py install --root %{buildroot}
rm -rf docs-f2py ; mv %{buildroot}%{python_sitearch}/numpy/f2py/docs docs-f2py
mv -f %{buildroot}%{python_sitearch}/numpy/f2py/f2py.1 f2py.1
rm -rf doc ; mv -f %{buildroot}%{python_sitearch}/numpy/doc .
install -D -p -m 0644 f2py.1 %{buildroot}%{_mandir}/man1/f2py26.1
pushd %{buildroot}%{_bindir} &> /dev/null
# symlink for anyone who was using f2py.numpy
ln -s f2py26 f2py26.numpy
popd &> /dev/null

#symlink for includes, BZ 185079
mkdir -p %{buildroot}/usr/include
ln -s %{python_sitearch}/numpy/core/include/numpy/ %{buildroot}/usr/include/numpy

# Remove doc files. They should in in %doc
rm -f %{buildroot}%{python_sitearch}/numpy/COMPATIBILITY
rm -f %{buildroot}%{python_sitearch}/numpy/DEV_README.txt
rm -f %{buildroot}%{python_sitearch}/numpy/INSTALL.txt
rm -f %{buildroot}%{python_sitearch}/numpy/LICENSE.txt
rm -f %{buildroot}%{python_sitearch}/numpy/README.txt
rm -f %{buildroot}%{python_sitearch}/numpy/THANKS.txt
rm -f %{buildroot}%{python_sitearch}/numpy/site.cfg.example

%check
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} -c "import pkg_resources, numpy ; numpy.test()" \
%ifarch s390 s390x
|| :
%endif
# don't remove this comment
popd &> /dev/null

%if 0%{?with_python3}
pushd doc &> /dev/null
# there is no python3-nose yet
#PYTHONPATH="%{buildroot}%{python3_sitearch}" %{__python3} -c "import pkg_resources, numpy ; numpy.test()" \
%ifarch s390 s390x
|| :
%endif
# don't remove this comment
popd &> /dev/null

%endif # with_python3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs-f2py doc/* LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%dir %{python_sitearch}/numpy
%{python_sitearch}/numpy/*.py*
%{python_sitearch}/numpy/core
%{python_sitearch}/numpy/distutils
%{python_sitearch}/numpy/fft
%{python_sitearch}/numpy/lib
%{python_sitearch}/numpy/linalg
%{python_sitearch}/numpy/ma
%{python_sitearch}/numpy/numarray
%{python_sitearch}/numpy/oldnumeric
%{python_sitearch}/numpy/random
%{python_sitearch}/numpy/testing
%{python_sitearch}/numpy/tests
%{python_sitearch}/numpy/tools
%{python_sitearch}/numpy/compat
%{python_sitearch}/numpy/matrixlib
%{python_sitearch}/numpy/polynomial
%{python_sitearch}/numpy-*.egg-info
%{_includedir}/numpy

%files f2py
%defattr(-,root,root,-)
%{_mandir}/man*/*
%{_bindir}/f2py26
%{_bindir}/f2py26.numpy
%{python_sitearch}/numpy/f2py

%if 0%{?with_python3}
%files -n python3-numpy
%defattr(-,root,root,-)
%doc docs-f2py doc/* LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%{python3_sitearch}/numpy/__pycache__/*
%dir %{python3_sitearch}/numpy
%{python3_sitearch}/numpy/*.py*
%{python3_sitearch}/numpy/core
%{python3_sitearch}/numpy/distutils
%{python3_sitearch}/numpy/fft
%{python3_sitearch}/numpy/lib
%{python3_sitearch}/numpy/linalg
%{python3_sitearch}/numpy/ma
%{python3_sitearch}/numpy/numarray
%{python3_sitearch}/numpy/oldnumeric
%{python3_sitearch}/numpy/random
%{python3_sitearch}/numpy/testing
%{python3_sitearch}/numpy/tests
%{python3_sitearch}/numpy/compat
%{python3_sitearch}/numpy/matrixlib
%{python3_sitearch}/numpy/polynomial
%{python3_sitearch}/numpy-*.egg-info
#%{_includedir}/numpy

%files -n python3-numpy-f2py
%defattr(-,root,root,-)
#%{_mandir}/man*/*
%{_bindir}/f2py3
%{python3_sitearch}/numpy/f2py
%endif # with_python3


%changelog
* Wed Oct 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 1:1.5.1-0.1
- update to 1.5.1rc1
- add python3 subpackage
- some spec-cleanups

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-6
- actually add the patch this time

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-5
- fix segfault within %check on 2.7 (patch 2)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 18 2010 Dan Horák <dan[at]danny.cz> 1.4.1-3
- ignore the "Ticket #1299 second test" failure on s390(x)

* Thu Jun 24 2010 Jef Spaleta <jspaleta@fedoraprject.org> 1.4.1-2
- source commit fix 

* Thu Jun 24 2010 Jef Spaleta <jspaleta@fedoraprject.org> 1.4.1-1
- New upstream release. Include backported doublefree patch

* Mon Apr 26 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-8
- Moved distutils back to the main package, BZ 572820.

* Thu Apr 08 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-7
- Reverted to 1.3.0 after upstream pulled 1.4.0, BZ 579065.

* Tue Mar 02 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-5
- Linking /usr/include/numpy to .h files, BZ 185079.

* Tue Feb 16 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-4
- Re-enabling atlas BR, dropping lapack Requires.

* Wed Feb 10 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-3
- Since the previous didn't work, Requiring lapack.

* Tue Feb 09 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-2
- Temporarily dropping atlas BR to work around 562577.

* Fri Jan 22 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-1
- 1.4.0.
- Dropped ARM patch, ARM support added upstream.

* Tue Nov 17 2009 Jitesh Shah <jiteshs@marvell.com> - 1.3.0-6.fa1
- Add ARM support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-5
- Fixed atlas BR, BZ 505376.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-4
- EVR bump for pygame chainbuild.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-3
- Moved linalg, fft back to main package.

* Tue Apr 14 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-2
- Split out f2py into subpackage, thanks Peter Robinson pbrobinson@gmail.com.

* Tue Apr 07 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-1
- Update to latest upstream.
- Fixed Source0 URL.

* Thu Apr 02 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-0.rc1
- Update to latest upstream.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 1.2.1-3
- Require python-devel, BZ 488464.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 Jon Ciesla <limb@jcomserv.net> 1.2.1-1
- Update to 1.2.1.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.0-2
- Rebuild for Python 2.6

* Tue Oct 07 2008 Jon Ciesla <limb@jcomserv.net> 1.2.0-1
- New upstream release, added python-nose BR. BZ 465999.
- Using atlas blas, not blas-devel. BZ 461472.

* Wed Aug 06 2008 Jon Ciesla <limb@jcomserv.net> 1.1.1-1
- New upstream release

* Thu May 29 2008 Jarod Wilson <jwilson@redhat.com> 1.1.0-1
- New upstream release

* Tue May 06 2008 Jarod Wilson <jwilson@redhat.com> 1.0.4-1
- New upstream release

* Mon Feb 11 2008 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-2
- Add python egg to %%files on f9+

* Wed Aug 22 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-1
- New upstream release

* Wed Jun 06 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3-1
- New upstream release

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-2
- Drop BR: atlas-devel, since it just provides binary-compat
  blas and lapack libs. Atlas can still be optionally used
  at runtime. (Note: this is all per the atlas maintainer).

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-1
- New upstream release

* Tue Apr 17 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-4
- Update gfortran patch to recognize latest gfortran f95 support 
- Resolves rhbz#236444

* Fri Feb 23 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-3
- Fix up cpuinfo bug (#229753). Upstream bug/change:
  http://projects.scipy.org/scipy/scipy/ticket/349

* Thu Jan 04 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2
- Per discussion w/Jose Matos, Obsolete/Provide f2py, as the
  stand-alone one is no longer supported/maintained upstream

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 1.0.1-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.0-2
- Rebuild for python 2.5

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.0-1
- New upstream release

* Tue Sep 06 2006 Jarod Wilson <jwilson@redhat.com> 0.9.8-1
- New upstream release

* Wed Apr 26 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.6-1
- Upstream update

* Thu Feb 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.5-1
- Upstream update

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-2
- Rebuild for Fedora Extras 5

* Thu Feb  2 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-1
- Initial RPM release
- Added gfortran patch from Neal Becker
