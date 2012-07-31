Name:		ocaml
Version:	3.09.3
Release: 	1%{?dist}

Summary:	Objective Caml compiler and programming environment

Group:		Development/Languages
License:	QPL/LGPL
URL:		http://www.ocaml.org
Source0:	http://caml.inria.fr/distrib/ocaml-3.09/ocaml-3.09.3.tar.bz2
Source1:	http://caml.inria.fr/distrib/ocaml-3.09/ocaml-3.09-refman.html.tar.gz
Source2:	http://caml.inria.fr/distrib/ocaml-3.09/ocaml-3.09-refman.pdf
Source3:	http://caml.inria.fr/distrib/ocaml-3.09/ocaml-3.09-refman.info.tar.gz
Patch0:		ocaml-rpath.patch
Patch1:		ocaml-user-cflags.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ncurses-devel
BuildRequires:  gdbm-devel
BuildRequires:	tcl-devel, tk-devel
BuildRequires:	emacs, perl
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXaw-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXt-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
Requires(post):	/sbin/install-info
Requires(preun): /sbin/install-info

%description
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler
and an optimizing native-code compiler), an interactive toplevel system,
parsing tools (Lex,Yacc,Camlp4), a replay debugger, a documentation generator,
and a comprehensive library.


%package -n labltk
Group:		Development/Languages
Summary:	Tk bindings for Objective Caml
Requires:	ocaml = %{version}-%{release}

%description -n labltk
A library for interfacing Objective Caml with the scripting language
Tcl/Tk. It include the OCamlBrowser code editor / library browser.


%package -n camlp4
Group:		Development/Languages
Summary:	Pre-Processor-Pretty-Printer for OCaml
Requires:	ocaml = %{version}-%{release}

%description -n camlp4
Camlp4 is a Pre-Processor-Pretty-Printer for OCaml, parsing a source
file and printing some result on standard output.


%package ocamldoc
Group:		Development/Languages
Summary:	Documentation generator for OCaml
Requires:	ocaml = %{version}-%{release}

%description ocamldoc
Documentation generator for Objective Caml.


%package emacs
Group:		Development/Languages
Summary:	Emacs mode for Objective Caml
Requires:	ocaml = %{version}-%{release}
Requires:	emacs

%description emacs
Emacs mode for Objective Caml.


%package docs
Group:		Development/Languages
Summary:	Documentation for OCaml
Requires:	ocaml = %{version}-%{release}

%description docs
Documentation for Objective Caml.


%prep
%setup -q -T -b 0
%setup -q -T -D -a 1
%setup -q -T -D -a 3
%patch0 -p1
%patch1 -p1 -b .cflags

cp %{SOURCE2} refman.pdf


%build
CFLAGS="$RPM_OPT_FLAGS" ./configure \
    -bindir %{_bindir} \
    -libdir %{_libdir}/ocaml \
    -x11lib %{_libdir} \
    -x11include %{_includedir} \
    -mandir %{_mandir}/man1
make world opt opt.opt
# %{?_smp_mflags} breaks the build
(cd emacs; make ocamltags)


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall BINDIR=$RPM_BUILD_ROOT%{_bindir} LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml MANDIR=$RPM_BUILD_ROOT%{_mandir}
perl -pi -e "s|^$RPM_BUILD_ROOT||" $RPM_BUILD_ROOT%{_libdir}/ocaml/ld.conf
(
    cd emacs;
    make install BINDIR=$RPM_BUILD_ROOT%{_bindir} EMACSDIR=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
    make install-ocamltags BINDIR=$RPM_BUILD_ROOT%{_bindir}
)
(
    mkdir -p $RPM_BUILD_ROOT%{_infodir};
    cd infoman; cp ocaml*.gz $RPM_BUILD_ROOT%{_infodir}
)


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info \
    --entry "* ocaml: (ocaml).	 The Objective Caml compiler and programming environment" \
    --section "Programming Languages" \
    %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :


%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/ocaml
%{_infodir}/*
%exclude %{_bindir}/camlp4*
%exclude %{_bindir}/mkcamlp4
%exclude %{_bindir}/ocpp
%exclude %{_bindir}/labltk
%exclude %{_bindir}/ocamltags
%exclude %{_bindir}/ocamlbrowser
%exclude %{_bindir}/ocamldoc*
%exclude %{_libdir}/ocaml/camlp4
%exclude %{_libdir}/ocaml/labltk
%exclude %{_libdir}/ocaml/ocamldoc
%exclude %{_mandir}/man1/camlp4*
%exclude %{_mandir}/man1/mkcamlp4*
%exclude %{_libdir}/ocaml/stublibs/dlllabltk.so
%exclude %{_libdir}/ocaml/stublibs/dlltkanim.so
%doc README LICENSE Changes


%files -n labltk
%defattr(-,root,root,-)
%{_bindir}/labltk
%{_bindir}/ocamlbrowser
%{_libdir}/ocaml/labltk
%{_libdir}/ocaml/stublibs/dlllabltk.so
%{_libdir}/ocaml/stublibs/dlltkanim.so
%doc otherlibs/labltk/examples_labltk
%doc otherlibs/labltk/examples_camltk


%files -n camlp4
%defattr(-,root,root,-)
%{_bindir}/camlp4*
%{_bindir}/mkcamlp4
%{_bindir}/ocpp
%{_libdir}/ocaml/camlp4
%{_mandir}/man1/camlp4*
%{_mandir}/man1/mkcamlp4*


%files ocamldoc
%defattr(-,root,root,-)
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc
%doc ocamldoc/Changes.txt


%files docs
%defattr(-,root,root,-)
%doc refman.pdf htmlman


%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/*
%{_bindir}/ocamltags
%doc emacs/README


%changelog
* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-1
- new version 3.09.3

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-2
- Rebuild for FE6

* Sun Apr 30 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-1
- new version 3.09.2

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-2
- Rebuild for Fedora Extras 5

* Thu Jan  5 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-1
- new version 3.09.1

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.0-1
- new version 3.09.0

* Sun Sep 11 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.4-1
- New Version 3.08.4

* Wed May 25 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-5
- Bump and re-release as last build failed due to rawhide syncing.

* Sun May 22 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-4
- Fix for gcc4 and the 32 bit assembly in otherlibs/num.
- Fix to allow compilation with RPM_OPT_FLAG defined -O level.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 3.08.3-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar 26 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.3-1
- New Version 3.08.3

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-2
- Added patch for removing rpath from shared libs

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-1
- New Version 3.08.2

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:3.07-6
- add -x11lib %%{_prefix}/X11R6/%%{_lib} to configure; fixes labltk build
  on x86_64

* Tue Dec  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.5
- ocamldoc -> ocaml-ocamldoc
- ocaml-doc -> ocaml-docs

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.4
- Make separate packages for labltk, camlp4, ocamldoc, emacs and documentation

* Thu Nov 27 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.2
- Changed license tag
- Register info files
- Honor RPM_OPT_FLAGS
- New Patch

* Fri Oct 31 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.1
- First Fedora release

* Mon Oct 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Updated to 3.07.

* Wed Apr  9 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Rebuilt for Red Hat 9.

* Tue Nov 26 2002 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Added %{_mandir}/mano/* entry
