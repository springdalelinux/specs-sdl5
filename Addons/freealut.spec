Name:           freealut
Version:        1.1.0
Release:        3%{?dist}
Summary:        Implementation of OpenAL's ALUT standard

Group:          System Environment/Libraries
License:        GPL
URL:            http://openal.org/
Source0:        http://openal.org/openal_webstf/downloads/freealut-1.1.0.tar.gz
Patch0:         freealut-openal.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openal-devel
BuildRequires:  libtool

%description
freealut is a free implementation of OpenAL's ALUT standard. See the file
AUTHORS for the people involved.

%package devel
Summary:        Development files for freealut
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} 
Requires:       pkgconfig
Requires:       openal-devel

%description devel
Development headers and libraries needed for freealut development

%prep
%setup -q
%patch0
autoreconf

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_libdir}/libalut.la

# don't have dsp devices in buildroot
#%check
#pushd test_suite
#./test_errorstuff || exit $?  
#./test_fileloader || exit $?  
#./test_memoryloader || exit $?
#./test_retrostuff || exit $?
#./test_version || exit $?  
#./test_waveforms || exit $?
#popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/libalut.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/* examples/*.c
%{_bindir}/freealut-config
%{_includedir}/AL
%{_libdir}/libalut.so
%{_libdir}/pkgconfig/freealut.pc

%changelog
* Mon Mar 12 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.1.0-3
- fix #231132

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.1.0-2
- FE6 rebuild

* Tue Jun 13 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.1.0-1
- version upgrade

* Fri Feb 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-3
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-2
- Add examples to devel doc
- Fix openal linking

* Sat Feb 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.0-1
- Initial release
