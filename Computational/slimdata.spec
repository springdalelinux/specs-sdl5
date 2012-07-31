%define __python /usr/bin/python26
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           slimdata
Version:        2.6.4
Release:        1%{?dist}
Summary:        Tools and library for reading and writing slim compressed data

Group:          Development/Libraries
License:        GPLv3+
URL:            http://slimdata.sourceforge.net/
Source0:        http://dl.sf.net/sourceforge/%{name}/slim_2.6.4.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         slimdata-name-change.diff

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
BuildRequires:     python26
BuildRequires:     numpy26

#The current slim algorithm assumes little-endian.  Upstream is (slowly) working on this.
ExcludeArch: ppc64 ppc sparcv9 sparc64

%description
Slim is a data compression system for scientific data sets, both a binary and a
library with C linkage. Slim works with integer data from one or more channels
in a file, which it can compress more rapidly than general tools like gzip.

%package devel
Group:  Development/Libraries
Summary: Headers required when building programs against getdata
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Headers required when building projects that use the slimdata library.

%prep
%setup -q -n slim_2.6.4
%patch0 -p1

#Remove included 64-bit biniary
rm -f test/generate_random_data

%build
%configure
make %{?_smp_mflags}
#make doc

#Rebuild above binary.
#pushd test
#make
#popd

#%check
#make test

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} SUID_ROOT="" install

#delete static lib
rm -f %{buildroot}/%{_libdir}/libslim.a
chmod a+x %{buildroot}/%{_libdir}/libslim.so.0.0

#Rename binary to slimdata; upstream will follow in subsequent releases.
mv %{buildroot}/%{_bindir}/slim %{buildroot}/%{_bindir}/slimdata
rm %{buildroot}/%{_bindir}/unslim %{buildroot}/%{_bindir}/slimcat
#Don't forget the man page: BZ 506141
mv %{buildroot}/%{_mandir}/man1/slim.1 %{buildroot}/%{_mandir}/man1/slimdata.1
pushd .
cd %{buildroot}/%{_bindir}
ln -s slimdata unslim
ln -s slimdata slimcat
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS TODO VERSIONS
%{_bindir}/*slim*
%{_libdir}/libslim.so.0*
%{_mandir}/man1/*slim*

%files devel
%defattr(-,root,root,-)
#doc doc/slim_format.pdf doc/html/*
%{_includedir}/slim*.h
%{_libdir}/libslim.so

%changelog
* Wed Jun 01 2011 Jon Ciesla <limb@jcomserv.net> - 2.6.4-1
- New upstream. 
- Dropping check section as it fails in RPM build.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 7 2009 Matthew Truch <matt at truch.net> - 2.6.3-7
- Excluearch sparcv9 and sparc64 as slimdata doesn't work on bigendian machines

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Matthew Truch <matt at truch.net> - 2.6.3-5
- Change name of man page to slimdata as well (BZ 506141).

* Tue May 5 2009 Matthew Truch <matt at truch.net> - 2.6.3-4
- Change binary name to slimdata.
- Use symlinks for binaries unslim and slimcat

* Tue Apr 21 2009 Matthew Truch <matt at truch.net> - 2.6.3-3
- Correct license tag.
- Make tests run.
- Set exec bit on /usr/lib/libslim.so.0.0

* Sat Apr 4 2009 Matthew Truch <matt at truch.net> - 2.6.3-2
- Don't run tests since they don't seem to work.

* Sun Mar 22 2009 Matthew Truch <matt at truch.net> - 2.6.3-1
- Upstream 2.6.3.  Includes proper licensing.  

* Tue Feb 24 2009 Matthew Truch <matt at truch.net> - 2.6.1b-4
- Include patch to fix gcc-4.4 compilation from Lucian.

* Mon Feb 16 2009 Matthew Truch <matt at truch.net> - 2.6.1b-3
- Fix shared library generation.

* Sun Jan 18 2009 Matthew Truch <matt at truch.net> - 2.6.1b-2
- Properly include BR for building docs and include those docs
- Use better soname for shared library.

* Sat Jan 10 2009 Matthew Truch <matt at truch.net> - 2.6.1b-1
- Update to upstream 2.6.1b.
- Apply fixes to build to better follow Fedora guidelines.

* Tue Oct 28 2008 Matthew Truch <matt at truch.net> - 2.6.1a-1
- Update to upstream 2.6.1a release which includes fixes pushed upstream.

* Fri Oct 24 2008 Matthew Truch <matt at truch.net> - 2.6.1-1
- Initial Fedora build.

