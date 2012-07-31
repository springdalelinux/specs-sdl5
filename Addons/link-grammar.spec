Summary: A Grammar Checking library
Name: link-grammar
Version: 4.2.5
Release: 1%{?dist}
Group: System Environment/Libraries
License: BSD-style 
Source: http://www.abisource.com/downloads/link-grammar/%{version}/link-grammar-%{version}.tar.gz
URL: http://bobo.link.cs.cmu.edu/link/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A library that can perform grammar checking.

%package devel
Summary: Support files necessary to compile applications with liblink-grammar
Group: Development/Libraries
Requires: link-grammar = %{version}-%{release}

%description devel
Libraries, headers, and support files needed for using liblink-grammar.

%prep
%setup -q

%build
%configure
make
# currently the build system can not handle smp_flags properly
# make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%files
%defattr(-,root,root)
%doc LICENSE README
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_datadir}/link-grammar

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/link-grammar.pc
%{_includedir}/link-grammar

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Mon Nov 12 2007 Marc Maurer <uwog@uwog.net> 4.2.5-1
- New upstream version, fixes bug 371221.

* Mon Sep 11 2006 Marc Maurer <uwog@abisource.com> 4.2.2-2.fc6
- Rebuild for FC6

* Wed Apr 12 2006 Marc Maurer <uwog@abisource.com> 4.2.2-1
- New upstream version

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 4.2.1-2
- Rebuild

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 4.2.1-1
- New upstream version

* Wed Feb 15 2006 Marc Maurer <uwog@abisource.com> 4.1.3-4
- Rebuild for Fedora Extras 5
- Use %%{?dist} in the release name

* Wed Aug 10 2005 Marc Maurer <uwog@abisource.com> - 4.1.3-3
- Set the buildroot to the standard Fedora buildroot
- Make the package own the %{_datadir}/link-grammar
  directory (thanks go to Aurelien Bompard for both issues)

* Wed Aug 10 2005 Marc Maurer <uwog@abisource.com> - 4.1.3-2
- Remove epoch
- Make rpmlint happy

* Sun Aug 7 2005 Marc Maurer <uwog@abisource.com> - 1:4.1.3-1
- Initial version
