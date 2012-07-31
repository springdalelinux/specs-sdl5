Summary:	Validating XML Parser
Name:		xerces-c
Version:	2.7.0
Release:	8%{?dist}
License:	Apache Software License
Group:		System Environment/Libraries
URL:		http://xml.apache.org/xerces-c/
Source0:	http://www.apache.org/dist/xml/xerces-c/source/xerces-c-src_2_7_0.tar.gz
Patch0:		xerces-c--CVE-2009-1885.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Xerces-C is a validating XML parser written in a portable subset of
C++. Xerces-C makes it easy to give your application the ability to
read and write XML data. A shared library is provided for parsing,
generating, manipulating, and validating XML documents. Xerces-C is
faithful to the XML 1.0 recommendation and associated standards ( DOM
1.0, DOM 2.0. SAX 1.0, SAX 2.0, Namespaces).

%package	devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package doc
Group:		Documentation
Summary:	Documentation for Xerces-C++ validating XML parser

%description doc
Documentation for Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

#%package	samples
#Summary:	Sample applications using Xerces-C++
#Group:		Applications/Text
#Requires:	%{name} = %{version}-devel-%{release}

#%description	samples
#Sample applications using Xerces-C++.


%prep
%setup -q -n xerces-c-src_2_7_0
rm -rf doc/html/resources/.svn
find ./doc -type f -perm 755 -exec chmod 644 {} \;
find ./samples -type f -perm 755 -exec chmod 644 {} \;
%{__perl} -pi.orig -e 's|(PREFIX.)/lib\b|$1/%{_lib}|g' src/xercesc/configure */Makefile.in
%patch0 -p0 -b .CVE-2009-1885

%build
export XERCESCROOT="$PWD"

# Let Makefiles be verbose
find -name 'Makefile.*' | while read f; do
	sed -i -e 's/$Q//g' \
	-e 's/{MAKE} -s/(MAKE)/g' \
	-e '/echo \"  (/d' \
	$f
done

# Remove conflicting flags from runConfigure
find -name runConfigure | while read f; do
	sed -i -e 's/-w -O -DNDEBUG/-DNDEBUG/g' $f
done

cd $XERCESCROOT/src/xercesc
%ifarch alpha ppc64 s390x sparc64 x86_64
CXXFLAGS="${RPM_OPT_FLAGS}" CFLAGS="${RPM_OPT_FLAGS}" ./runConfigure -plinux -cgcc -xg++ -minmem -nsocket -tnative -rpthreads -b64 -P %{_prefix} -C --libdir="%{_libdir}"
%else
CXXFLAGS="${RPM_OPT_FLAGS}" CFLAGS="${RPM_OPT_FLAGS}" ./runConfigure -plinux -cgcc -xg++ -minmem -nsocket -tnative -rpthreads -b32 -P %{_prefix} -C --libdir="%{_libdir}"
%endif
# not smp safe
%{__make}
#cd $XERCESCROOT/samples
#CXXFLAGS="${RPM_OPT_FLAGS}" CFLAGS="${RPM_OPT_FLAGS}" ./runConfigure -plinux -cgcc -xg++
#%{__make}

%install
%{__rm} -rf $RPM_BUILD_ROOT
export XERCESCROOT="$PWD"
%{__make} install -C src/xercesc DESTDIR="$RPM_BUILD_ROOT"
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
#rm -rf $XERCESCROOT/samples/Projects
#cp -a $XERCESCROOT/samples $RPM_BUILD_ROOT%{_datadir}/%{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_libdir}/libxerces*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libxerces*.so
%{_includedir}/xercesc/

%files doc
%defattr(-,root,root,-)
%doc Readme.html LICENSE NOTICE STATUS credits.txt doc samples

#%files samples
#%defattr(-,root,root,-)
#%{_datadir}/%{name}/samples

%changelog
* Thu Aug  6 2009 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-8
- Fix CVE-2009-1885

* Wed Feb 27 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-7
- rebuild

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-6
- typo fix

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-5
- fixed some rpmlint warnings

* Fri Nov 24 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-4
- Added samples to docs-package

* Sat Nov 18 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-3
- improvements suggested by Aurelien Bompard

* Sat Oct 14 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-2
- Disabled package 'samples'

* Fri Oct 13 2006 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-1
- initial build for FE

* Fri Jan 06 2006 Dag Wieers <dag@wieers.com> - 2.7.0-1 - 3891/dag
- Cleaned SPEC file.

* Tue Jan 03 2006 Dries Verachtert <dries@ulyssis.org> - 2.7.0-1
- Updated to release 2.7.0.

* Thu Sep 22 2005 C.Lee Taylor <leet@leenx.co.za> 2.6.1-1
- Update to 2.6.1
- Build for FC4 32/64bit

* Sat Aug 20 2005 Che
- initial rpm release
