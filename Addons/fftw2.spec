Name:           fftw2
Version:        2.1.5
Release:        13%{?dist}
Summary:        Fast Fourier Transform library
%define 	real_name fftw

Group:          System Environment/Libraries
License:        GPL
URL:            http://www.fftw.org/
Source0:        ftp://ftp.fftw.org/pub/fftw/fftw-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran

%description
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.


%package        devel
Summary:        Headers, libraries and docs for the FFTW library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.



%prep
%setup -q -c %{real_name}-%{version}
mv %{real_name}-%{version} single
cp -a single double



%build
pushd double
	%ifarch i386
		%configure \
			--enable-shared \
			--enable-threads \
			--enable-i386-hacks
	%else
		%configure \
			--enable-shared \
			--enable-threads
	%endif
	make %{?_smp_mflags}
popd
pushd single
	%configure \
		--enable-shared \
		--enable-type-prefix \
		--enable-threads \
		--enable-float
	make %{?_smp_mflags}
popd



%install
rm -rf ${RPM_BUILD_ROOT}
pushd double
	make install DESTDIR=${RPM_BUILD_ROOT}
	cp -a AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO ../
	cp -a FAQ/fftw-faq.html/ doc/ ../
popd
pushd single
	make install DESTDIR=${RPM_BUILD_ROOT}
popd
rm -f doc/Makefile*
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'



%clean
rm -rf ${RPM_BUILD_ROOT}



%post -p /sbin/ldconfig



%postun -p /sbin/ldconfig



%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc  doc/
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_infodir}/*



%changelog
* Tue Aug 29 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-13
- Rebuild for FE6

* Sat Feb 18 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-12
- Rebuild for FC-5.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-11
- Fix incomplete substitution

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-10
- Add disttag to release.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-9
- Rename package to fftw2.

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

