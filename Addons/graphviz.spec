# $Id: graphviz.spec.in,v 1.96 2006/10/24 13:46:11 ellson Exp $ $Revision: 1.96 $
# graphviz.spec.  Generated from graphviz.spec.in by configure.

# Note: graphviz requires gd with gif support (and other fixes), hence use
# internal one for now.

#-- graphviz src.rpm --------------------------------------------------------
Name:		graphviz
Version:	2.12
Release:	8%{?dist}

License:	CPL
URL:		http://www.graphviz.org/
Source:		http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-2.12.tar.gz
Patch0:		%{name}-php5.patch
Patch1:		%{name}-libcdt.patch

# graphviz is relocatable
#Prefix: /usr
# not until we can figure out why relocatabilty is broken

#-- feature and package selection -------------------------------------------
#	depends on %dist and %fedora (or %rhl or %rhel) which are set
#	in .rpmmacros on each build host

# Define a default set of features incase none of the conditionals apply
%define SHARP	0
%define GUILE	0
%define _IO	0
%define JAVA	0
%define LUA	0
%define OCAML	0
%define PERL	0
%define PHP	0
%define PYTHON	0
%define RUBY	0
%define TCL	1
%define IPSEPCOLA	--without-ipsepcola
%define MYLIBGD		--with-mylibgd
%define MING		--without-ming

# SuSE uses a different mechanism to generate BuildRequires
# norootforbuild
# neededforbuild  expat freetype2 freetype2-devel gcc libjpeg libpng-devel-packages tcl tcl-devel tk tk-devel x-devel-packages

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	zlib-devel libpng-devel libjpeg-devel expat-devel freetype-devel >= 2
BuildRequires:	/bin/ksh bison m4 flex tk tcl >= 8.3 swig

# This just indicates the requirement for tcl.h, tk.h, but doesn't identify
# where to get them from. In RH9 and earlier they were in the tcl, tk,
# base packages which are always BR'd anyway (above).
BuildRequires:	/usr/include/tcl.h /usr/include/tk.h

%if 0%{?rhl}
%define PERL	1
%define TCL	1
BuildRequires: XFree86-devel perl
%endif

%if 0%{?rhel}
%define PERL	1
%define TCL	1
BuildRequires: perl
%if "%rhel" < "4"
BuildRequires: XFree86-devel
%endif
%if "%rhel" >= "3"
%define IPSEPCOLA --with-ipsepcola
BuildRequires: fontconfig-devel tcl-devel tk-devel
%endif
%if "%rhel" == "4"
BuildRequires: xorg-x11-devel
%endif
%if "%rhel" >= "4"
%define PHP	1
%define RUBY	1
BuildRequires: php-devel ruby ruby-devel
%endif
%if "%rhel" >= "5"
BuildRequires: libtool-ltdl libtool-ltdl-devel libXaw-devel libSM-devel
BuildRequires: libICE-devel libXpm-devel libXt-devel libXmu-devel
BuildRequires: libXext-devel libX11-devel glib2-devel libtool
%endif
%endif

%if 0%{?fedora}
%define PERL	1
%define TCL	1
BuildRequires: fontconfig-devel tcl-devel tk-devel 
%if "%fedora" < "3"
BuildRequires: XFree86-devel
%endif
%if "%fedora" == "3"
BuildRequires: xorg-x11-devel
%endif
%if "%fedora" == "4"
BuildRequires: xorg-x11-devel
%endif
%if "%fedora" >= "3"
%define IPSEPCOLA --with-ipsepcola
%endif
%if "%fedora" >= "4"
%define PHP	1
%define RUBY	1
%define GUILE	1
BuildRequires: libtool-ltdl libtool-ltdl-devel php-devel ruby ruby-devel guile-devel
%endif
%if "%fedora" >= "5"
%define JAVA	1
%define PYTHON	1
BuildRequires: libXaw-devel libSM-devel libICE-devel libXpm-devel libXt-devel libXmu-devel libXext-devel libX11-devel libgcj-devel python-devel java-devel
%ifnarch ppc64
%define SHARP	1
%define OCAML	1
BuildRequires: mono-core ocaml
%endif
%endif
%if "%fedora" >= "6"
%define LUA	1
BuildRequires: cairo-devel >= 1.1.10 pango-devel gmp-devel lua-devel
%endif
%endif

#-- graphviz rpm --------------------------------------------------
Group:		Applications/Multimedia
Summary:	Graph Visualization Tools
Requires:	urw-fonts
Requires(post):	/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
A collection of tools for the manipulation and layout
of graphs (as in nodes and edges, not as in barcharts).

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.so.*
%{_libdir}/graphviz/*.so.*
%{_mandir}/man1/*.1*
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/lefty
%exclude %{_libdir}/graphviz/*/*
%exclude %{_libdir}/graphviz/libgvplugin_gd.*

# run "dot -c" to generate plugin config in %{_libdir}/graphviz/config
%post
%{_bindir}/dot -c
/sbin/ldconfig

# if there is no dot after everything else is done, the remove config
%postun
if ! test -x %{_bindir}/dot; then rm -f %{_libdir}/graphviz/config; fi
/sbin/ldconfig

#-- graphviz-gd rpm --------------------------------------------------
%package gd
Group:		Applications/Multimedia
Summary:	Graphviz plugin for renderers based on gd
Requires:	graphviz = %{version}-%{release}

%description gd
graphviz plugin for renderers based on gd

%files gd
%{_libdir}/graphviz/libgvplugin_gd.so.*

# run "dot -c" to generate plugin config in %{_libdir}/graphviz/config
%post gd
%{_bindir}/dot -c

# if there is not dot after everything else is done, the remove config
%postun gd
if ! test -x %{_bindir}/dot; then rm -f %{_libdir}/graphviz/config; fi

#-- graphviz-sharp rpm --------------------------------------------
%if %{SHARP}
%package sharp
Group:		Applications/Multimedia
Summary:	C# extension for graphviz
Requires:	graphviz = %{version}-%{release} mono-core

%description sharp
C# extension for graphviz.

%files sharp
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/sharp
%{_libdir}/graphviz/sharp/*
%endif

#-- graphviz-guile rpm --------------------------------------------
%if %{GUILE}
%package guile
Group:		Applications/Multimedia
Summary:	Guile extension for graphviz
Requires:	graphviz = %{version}-%{release} guile

%description guile
Guile extension for graphviz.

%files guile
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/guile
%{_libdir}/graphviz/guile/*
%endif

#-- graphviz-io rpm -----------------------------------------------
%if %{_IO}
%package io
Group:		Applications/Multimedia
Summary:	Io extension for graphviz
Requires:	graphviz = %{version}-%{release} io

%description io
Io extension for graphviz.

%files io
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/io
%{_libdir}/graphviz/io/*
%endif

#-- graphviz-java rpm ---------------------------------------------
%if %{JAVA}
%package java
Group:		Applications/Multimedia
Summary:	Java extension for graphviz
Requires:	graphviz = %{version}-%{release} java

%description java
Java extension for graphviz.

%files java
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/java
%{_libdir}/graphviz/java/*
%endif

#-- graphviz-lua rpm ----------------------------------------------
%if %{LUA}
%package lua
Group:		Applications/Multimedia
Summary:	Lua extension for graphviz
Requires:	graphviz = %{version}-%{release} lua

%description lua
Lua extension for graphviz.

%files lua
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/lua
%{_libdir}/graphviz/lua/*
%endif

#-- graphviz-ocaml rpm --------------------------------------------
%if %{OCAML}
%package ocaml
Group:		Applications/Multimedia
Summary:	Ocaml extension for graphviz
Requires:	graphviz = %{version}-%{release} ocaml

%description ocaml
Ocaml extension for graphviz.

%files ocaml
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/ocaml
%{_libdir}/graphviz/ocaml/*
%endif

#-- graphviz-perl rpm ---------------------------------------------
%if %{PERL}
%package perl
Group:		Applications/Multimedia
Summary:	Perl extension for graphviz
Requires:	graphviz = %{version}-%{release} perl

%description perl
Perl extension for graphviz.

%files perl
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/perl
%{_libdir}/graphviz/perl/*
%endif

#-- graphviz-php rpm ----------------------------------------------
%if %{PHP}
%package php
Group:		Applications/Multimedia
Summary:	PHP extension for graphviz
Requires:	graphviz = %{version}-%{release} php

%description php
PHP extension for graphviz.

%files php
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/php
%{_libdir}/graphviz/php/*
%endif

#-- graphviz-python rpm -------------------------------------------
%if %{PYTHON}
%package python
Group:		Applications/Multimedia
Summary:	Python extension for graphviz
Requires:	graphviz = %{version}-%{release} python

%description python
Python extension for graphviz.

%files python
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/python
%{_libdir}/graphviz/python/*
%endif

#-- graphviz-ruby rpm ---------------------------------------------
%if %{RUBY}
%package ruby
Group:		Applications/Multimedia
Summary:	Ruby extension for graphviz
Requires:	graphviz = %{version}-%{release} ruby

%description ruby
Ruby extension for graphviz.

%files ruby
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/ruby
%{_libdir}/graphviz/ruby/*
%endif

#-- graphviz-tcl rpm ----------------------------------------------
%if %{TCL}
%package tcl
Group:		Applications/Multimedia
Summary:	Tcl extension & tools for graphviz
Requires:	graphviz = %{version}-%{release} tcl >= 8.3 tk

%description tcl
Various tcl packages (extensions) for the graphviz tools.

%files tcl
%defattr(-,root,root,-)
%dir %{_libdir}/graphviz/tcl
%{_libdir}/graphviz/tcl/*
%{_libdir}/graphviz/pkgIndex.tcl
%{_datadir}/graphviz/demo
%{_mandir}/mann/*.n*
%endif

#-- graphviz-devel rpm --------------------------------------------
%package devel
Group:		Development/Libraries
Summary:	Development package for graphviz
Requires:	graphviz = %{version}-%{release} pkgconfig

%description devel
A collection of tools for the manipulation and layout
of graphs (as in nodes and edges, not as in barcharts).
This package contains development files for graphviz.

%files devel
%defattr(-,root,root,-)
%{_includedir}/graphviz
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*
%exclude %{_libdir}/graphviz/*/*
%exclude %{_libdir}/graphviz/libgvplugin*
%exclude %{_libdir}/graphviz/*.so

#-- graphviz-graphs rpm -------------------------------------------
%package graphs
Group:		Applications/Multimedia
Summary:	Demo graphs for graphviz

%description graphs
Some demo graphs for graphviz.

%files graphs
%defattr(-,root,root,-)
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/graphs

#-- graphviz-doc rpm ----------------------------------------------
%package doc
Group:		Documentation
Summary:	PDF and HTML documents for graphviz

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%files doc
%defattr(-,root,root,-)
%doc __doc/*

#-- building --------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# XXX ix86 only used to have -ffast-math, let's use everywhere
%{expand: %%define optflags %{optflags} -ffast-math}
# %%configure is broken in RH7.3 rpmbuild
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--datadir=%{_datadir} \
	--mandir=%{_mandir} \
	--with-x \
	--disable-static \
	--disable-dependency-tracking %{MYLIBGD} %{IPSEPCOLA} %{MING}
%__make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT __doc
%{__make} \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=$RPM_BUILD_ROOT%{_docdir}/%{name} \
	pkgconfigdir=%{_libdir}/pkgconfig \
	install
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
chmod -x $RPM_BUILD_ROOT%{_datadir}/%{name}/lefty/*
cp -a $RPM_BUILD_ROOT%{_datadir}/%{name}/doc __doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

#-- changelog --------------------------------------------------

%changelog
* Thu May 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-8
- Pulled spec from devel/
- Adapted spec to build for EL-5 (thanks to Christopher Stone)

* Sat May 05 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-7
- Patch to fix BZ#237496
- Disabling relocatability to work around BZ#237082
- Disabling -ocaml and -sharp subpackages for ppc64 to remedy BZ#239078

* Wed Feb 14 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-6
- Removed patch, as tcl/tk got rolled back to 8.4

* Wed Feb 07 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-5
- Added patch for slightly broken tk 8.5

* Thu Feb 01 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-4
- Bump-n-build due to tk upgrade

* Wed Jan 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-3
- Added running of /sbin/ldconfig in post/postun (and Reqs)
- Minor edit to -gd summary
- Removed explicit dependency on libgcj in -java
- Added BR for ruby (not pulled in by ruby-devel!)
- Cleanup of spaces/tabs to minimize rpmlint warnings

* Wed Dec 13 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-2
- Use of RPM_INSTALL_PREFIX0 in %%post requires Prefix: to be set

* Mon Dec 11 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.12-1
- Fixed dist tag
- Fixed minor typo in -lua description (BZ#218191)
- Added upstream-supplied "php5" patch (due to newer swig)
- Added BR: java-devel & R: java

* Tue Sep 13 2005 John Ellson <ellson@research.att.com>
- split out language bindings into their own rpms so that 
  main rpm doesn't depend on (e.g.) ocaml

* Sat Aug 13 2005 John Ellson <ellson@research.att.com>
- imported various fixes from the Fedora-Extras .spec by Oliver Falk <oliver@linux-kernel.at>

* Wed Jul 20 2005 John Ellson <ellson@research.att.com>
- release 2.4
