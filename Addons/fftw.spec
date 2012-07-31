Name:           fftw
Version:        3.1.2
Release:        3%{?dist}
Summary:        Fast Fourier Transform library

Group:          System Environment/Libraries
License:        GPL
URL:            http://www.fftw.org/
Source0:        ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

Provides:       fftw3 = %{version}-%{release}
Obsoletes:      fftw3 < 3.1

%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.


%package        devel
Summary:        Headers, libraries and docs for the FFTW library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} pkgconfig

Provides:       fftw3-devel = %{version}-%{release}
Obsoletes:      fftw3-devel < 3.1


%description    devel
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.


%prep
%setup -q -c %{name}-%{version}
mv %{name}-%{version} single
cp -a single double
cp -a single long


%build
CONFIG_FLAGS="--enable-shared --disable-dependency-tracking --enable-threads"
pushd double
	%configure $CONFIG_FLAGS
	make %{?_smp_mflags}
popd
pushd single
	%configure $CONFIG_FLAGS --enable-single
	make %{?_smp_mflags}
popd
pushd long
	%configure $CONFIG_FLAGS --enable-long-double
	make %{?_smp_mflags}
popd


%install
rm -rf ${RPM_BUILD_ROOT}
pushd double
	make install DESTDIR=${RPM_BUILD_ROOT}
	cp -a AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO ../
	cp -a doc/ ../
popd
pushd single
	make install DESTDIR=${RPM_BUILD_ROOT}
popd
pushd long
	make install DESTDIR=${RPM_BUILD_ROOT}
popd
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%clean
rm -rf ${RPM_BUILD_ROOT}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%post devel
/sbin/install-info --section="Math" %{_infodir}/%{name}.info.gz %{_infodir}/dir  2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.pdf doc/html/* doc/FAQ/fftw-faq.html/
%doc %{_infodir}/*.info*
%exclude %{_libdir}/*.la
%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%changelog
* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.1.2-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-2
- BuildRequires: pkgconfig for -devel (bug 206444).

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-1
- New release.

* Fri Jun  2 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.1-1
- New upstream release.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-4
- Re-enable static libs (bug 181897).
- Build long-double version of libraries (bug 182587).

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-3
- Add Obsoletes and Provides.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-2
- Rebuild for Fedora Extras 5.
- Disable static libs.
- Remove obsolete configure options.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-1
- Upgrade to the 3.x branch, incorporating changes from the fftw3 spec file.
- Add dist tag.

* Mon May 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.5-8
- BuildReq gcc-gfortran (#156490).

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.5-7
- rebuild on all arches
- buildrequire compat-gcc-32-g77

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.1.5-5
- Bump release to provide Extras upgrade path.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.4
- BuildReq gcc-g77.

* Mon Sep 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.3
- Dropped post/preun scripts for info.

* Wed Sep 17 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.2
- Remove aesthetic comments.
- buildroot -> RPM_BUILD_ROOT.
- post/preun for info files.

* Mon Apr 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.1
- Updated to 2.1.5.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.4-0.fdr.2
- Added Epoch:0.
- Added ldconfig to post and postun.

* Sun Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.4-0.fdr.1
- Updated to 2.1.4.

* Fri Mar 14 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.3-0.fdr.1
- Fedorafied.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.

