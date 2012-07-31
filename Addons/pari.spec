Name:           pari
Version:        2.3.5
Release:        4%{?dist}
Summary:        Number Theory-oriented Computer Algebra System

Group:          System Environment/Libraries
# No version is specified.
License:        GPL+
URL:            http://pari.math.u-bordeaux.fr
Source:		http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-2.3.5.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	emacs
BuildRequires:	readline-devel
BuildRequires:	gmp-devel
BuildRequires:	tetex
BuildRequires:	tetex-dvips
BuildRequires:  desktop-file-utils
BuildRequires:	libX11-devel
Requires:       tetex-xdvi


%description
PARI is a widely used computer algebra system designed for fast
computations in number theory (factorizations, algebraic number
theory, elliptic curves...), but also contains a large number of other
useful functions to compute with mathematical entities such as
matrices, polynomials, power series, algebraic numbers, etc., and a
lot of transcendental functions.

PARI/GP is an advanced programmable calculator, which computes
symbolically as long as possible, numerically where needed, and
contains a wealth of number-theoretic functions.

%package devel
Summary:	Header files and libraries for PARI development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and libraries for PARI development.

%package emacs
Summary:	Emacs mode for PARI/GP
Group:		Applications/Engineering
Requires:	emacs-common
Requires:	%{name} = %{version}-%{release}

%description emacs
Emacs mode for PARI/GP.


%prep
%setup -q
sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld


%build
./Configure \
    --prefix=%{_prefix} \
    --share-prefix=%{_datadir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir}/man1 \
    --datadir=%{_datadir}/pari \
    --includedir=%{_includedir} \
    --with-gmp
make %{?_smp_mflags} gp CFLAGS="-fPIC $RPM_OPT_FLAGS -fno-strict-aliasing"


%check
make dobench
make dotest-compat
make dotest-intnum
make dotest-qfbsolve
make dotest-rfrac
make dotest-round4


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# we move pari.cfg to the docdir
rm -fr $RPM_BUILD_ROOT%{_prefix}/lib/pari

mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
cat >  $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/pari-init.el <<EOF
(add-to-list 'load-path "%{_datadir}/emacs/site-lisp/pari")
(autoload 'gp-mode "pari" nil t)
(autoload 'gp-script-mode "pari" nil t)
(autoload 'gp "pari" nil t)
(autoload 'gpman "pari" nil t)
EOF

cat > gp.desktop <<EOF
[Desktop Entry]
Name=PARI/GP
Comment=Programmable calculator based on PARI
Exec=gp
Icon=%{_datadir}/pari/misc/pari.xpm
Terminal=true
Type=Application
Categories=Application;Education;Math;
Encoding=UTF-8
X-Desktop-File-Install-Version=0.10
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
    --vendor fedora \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    gp.desktop

find $RPM_BUILD_ROOT -name xgp -exec rm '{}' ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES* COPYING COMPAT NEW README
%doc Olinux-*/pari.cfg
%{_libdir}/*.so.*
%{_bindir}/*
%{_datadir}/pari
%{_datadir}/applications/*
%{_mandir}/man*/*


%files devel
%defattr(-,root,root,-)
%{_includedir}/pari
%{_libdir}/*.so


%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/*


%changelog
* Wed Jun 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.3.4-4
- move Req: tetex-xdvi to -gp subpkg, drop on el6+ (#530565)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.4-1
- new release 2.3.4

* Wed Aug 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.3-2
- fix license tag

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.3-1
- new release 2.3.3

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-3
- corrected desktop file

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.1-2
- Autorebuild for GCC 4.3

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-1
- new version 2.3.1

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-5
- added -fno-strict-aliasing to CFLAGS and enabled ppc build

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-4
- Rebuild for FE6

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-3
- Exclude ppc for now, since test fails

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-2
- added %%check section
- use gmp

* Thu May 25 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-1
- new version 2.3.0

* Fri May 19 2006 Orion Poplawski <orion@cora.nwra.com> - 2.1.7-4
- Fix shared library builds

* Fri Dec  2 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-3
- Use none for architecture to guarantee working 64bit builds

* Fri Oct 21 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-2
- some cleanup

* Fri Sep 30 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-1
- New Version 2.1.7

* Sun Mar  6 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.6-1
- New Version 2.1.6

* Mon Nov 22 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.2
- Fixed problem with readline

* Wed Nov 12 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.x
- First Fedora release
