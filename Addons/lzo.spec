Name:           lzo
Version:        2.02
Release:        2%{?dist}.1
Summary:        Data compression library with very fast (de)compression
Group:          System Environment/Libraries
License:        GPL
URL:            http://www.oberhumer.com/opensource/lzo/
Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
Patch0:         lzo-2.02-configure.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package devel
Summary:        Development files for the lzo library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.


%prep
%setup -q
%patch0 -p1 -z .configure
# mark asm files as NOT needing execstack
for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/liblzo2.la


%check
make check test


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING THANKS NEWS
%{_libdir}/liblzo2.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/liblzo2.so


%changelog
* Sun May 06 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- rebuilt for RHEL5 final

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-2
- FE6 Rebuild

* Wed Jul 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-1
- New upstream release 2.02, soname change!

* Mon Jul 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.08-7
- Taking over as maintainer since Anvil has other priorities
- Add a patch to fix asm detection on i386 (bug 145882, 145893). Thanks to
  Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe> for the initial patch.
- Removed unused build dependency on nasm
- Remove static lib
- Cleanup %%doc a bit

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.08-6.fc5
- Rebuild for new gcc

* Tue Jan 17 2006 Dams <anvil[AT]livna.org> - 1.08-5.fc5
- Bumped release for gcc 4.1 rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.08-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.08-0.fdr.2
- Typo un devel description
- Added post and postun scriptlets
- Added URL in Source0

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.
