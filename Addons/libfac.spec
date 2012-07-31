
Summary: An extension to Singular-factory
Name:    libfac
Version: 2.0.5
Release: 7%{?dist}

License: GPL
Url:     http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Libfac/
# http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Libfac/libfac-2-0-5.tar,gz
Source:  libfac-2-0-5.tar.gz
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: factory-devel >= 2.0.5-7

%description
Singular-libfac is an extension to Singular-factory which implements
factorization of polynomials over finite fields and algorithms for
manipulation of polynomial ideals via the characteristic set methods
(e.g., calculating the characteristic set and the irreducible
characteristic series).

%package devel
Summary: An extension to Singular-factory
#Obsoletes: %{name} < %{version}-%{release}
#Provides:  %{name} = %{version}-%{release}
Group:   Development/Libraries
%description devel
Singular-libfac is an extension to Singular-factory which implements
factorization of polynomials over finite fields and algorithms for
manipulation of polynomial ideals via the characteristic set methods
(e.g., calculating the characteristic set and the irreducible
characteristic series).


%prep
%setup -q -n %{name}

# Rebuild configure with working 'const' test
#autoconf


%build
%configure --with-NOSTREAMIO

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

#make install DESTDIR=... fails
%makeinstall

# fix perms
chmod 644 $RPM_BUILD_ROOT%{_libdir}/lib*.a


%clean
rm -rf $RPM_BUILD_ROOT


%files devel
%defattr(-,root,root)
%doc 00README ChangeLog COPYING
%{_libdir}/lib*.a
%{_includedir}/*


%changelog
* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-7
- respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-6
- fc6 respin

* Thu Mar 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-4
- BR: factory-devel >= 2.0.5-7

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.0.5-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Oct 1 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-1
- 2.0.5

* Mon Nov 17 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.3.b
- update macros
- fix perms on %%_libdir/lib*.a
- try without --with-NOSTREAMIO

* Fri Nov 14 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.2.b
- License: GPL with restrictions
- fixup autoconf usage
- remove cvs tags

* Fri Oct 03 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.1.b
- fix autoconf
- update macros for Fecora Core support.

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.0.b
- first try.
- no shared libs, but make (only) -devel package to signify it's purpose

