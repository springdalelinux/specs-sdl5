Summary:	Sample rate conversion library for audio data
Name:		libsamplerate
Version:	0.1.7
Release:	2%{?dist}
License:	GPLv2+
Group:		System Environment/Libraries
URL:		http://www.mega-nerd.com/SRC/
Source0:	http://www.mega-nerd.com/SRC/%{name}-%{version}.tar.gz
Patch0:         libsamplerate-0.1.7-test.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires:	libsndfile-devel >= 1.0.6, pkgconfig

%description
Secret Rabbit Code is a sample rate converter for audio. It is capable
of arbitrary and time varying conversions. It can downsample by a
factor of 12 and upsample by the same factor. The ratio of input and
output sample rates can be a real number. The conversion ratio can
also vary with time for speeding up and slowing down effects.


%package devel
Summary:	Development related files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig

%description devel
Secret Rabbit Code is a sample rate converter for audio. It is capable
of arbitrary and time varying conversions. It can downsample by a
factor of 12 and upsample by the same factor. The ratio of input and
output sample rates can be a real number. The conversion ratio can
also vary with time for speeding up and slowing down effects.
This package contains development files for %{name}


%prep
%setup -q
%patch0 -p1 -b .test


%build
%configure --disable-dependency-tracking --disable-fftw --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT _doc
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{name}.la
cp -a doc _doc
rm _doc/Makefile*


%check
export LD_LIBRARY_PATH=`pwd`/src/.libs
make check
unset LD_LIBRARY_PATH


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README _doc/*
%{_bindir}/sndfile-resample
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/samplerate.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/samplerate.pc


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.1.7-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Hans de Goede <hdegoede@redhat.com> 0.1.6-1
- New upstream release 0.1.6

* Tue Jul 15 2008 Lubomir Rintel <lkundrak@v3.sk> 0.1.4-1
- New upstream release

* Mon Apr 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.3-1
- New upstream release 0.1.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.2-8
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-7
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-6
- Drop static lib from -devel package
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-5
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5, it seems this may have already
  been done, since the last rebuild was of March 16 and the Rebuild Request
  bug of March 19? Rebuilding anyway to be sure (bug 185876)
- Fix (remove) use of rpath

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 0.1.2-4.fc5
- rebuild

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.1.2-3
- rebuilt

* Mon Oct 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.2-0.fdr.1
- Update to 0.1.2.
- Use "make install DESTDIR=...", disable dependency tracking.
- Run tests during build.
- Drop fftw-devel build dep, it's only for an optional part of the test suite.

* Tue Jul 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.0.15-0.fdr.5
- Fix %%postun (#1665).

* Sat Jun 28 2003 Dams <anvil[AT]livna.org> 0:0.0.15-0.fdr.4
- Applied changes about doc from Michael Schwendt

* Sat Jun 28 2003 Dams <anvil[AT]livna.org> 0:0.0.15-0.fdr.3
- Modified doc inclusion way

* Wed Jun 25 2003 Dams <anvil[AT]livna.org> 0:0.0.15-0.fdr.2
- Added some more doc

* Thu May 22 2003 Dams <anvil[AT]livna.org>
- Initial build.
