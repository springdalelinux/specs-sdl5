%define shortname beamer
%define name latex-%{shortname}
%define version 3.07
%define release 3%{?dist}

%define texmfdir %{_datadir}/texmf
%define latexdir %{texmfdir}/tex/latex
%define beamerdir %{latexdir}/%{shortname}
%define xemacsdir %{_datadir}/xemacs/xemacs-packages
%define emacsdir %{_datadir}/emacs/site-lisp

%define build_xemacs 0
%define build_emacs 1

Summary: A LaTeX class for producing beamer presentations
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://sourceforge.net/projects/latex-beamer/
Source0: %{name}-%{version}.tar.gz
Source1: beamer.el
License: GPL
Group: Publishing
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch
Requires: tetex >= 2.0.2, tetex-latex >= 2.0.2, latex-pgf >= 0.63
Obsoletes: %{name}-lyx

%description
latex-beamer is a LaTeX class that allows you to create a presentation with a projector. It can also be used to create slides. It behaves similarly to other packages like prosper, but has the advantage that it works together directly with pdflatex, but also with dvips.

%if %{build_emacs}
%package emacs
Summary: Beamer's extension for emacs
Group: Publishing
Requires: %{name} = %{version}, emacs >= 21.3

%description emacs
This is the beamer's extension for emacs.
%endif

%if %{build_xemacs}
%package xemacs
Summary: Beamer's extension for Xemacs
Group: Publishing
Requires: %{name} = %{version}, xemacs >= 21.4.14

%description xemacs
This is the beamer's extension for Xemacs.
%endif

%prep
%setup

%build

%install
rm -rf "$RPM_BUILD_ROOT"
install --mode=0755 -d "$RPM_BUILD_ROOT%{beamerdir}"

cp -Rf ./base "$RPM_BUILD_ROOT%{beamerdir}/"
cp -Rf ./emulation "$RPM_BUILD_ROOT%{beamerdir}/"
cp -Rf ./extensions "$RPM_BUILD_ROOT%{beamerdir}/"
cp -Rf ./themes "$RPM_BUILD_ROOT%{beamerdir}/"
cp -Rf ./solutions "$RPM_BUILD_ROOT%{beamerdir}/"

cp -Rf ./doc "$RPM_BUILD_ROOT%{beamerdir}/"
cp -Rf ./examples "$RPM_BUILD_ROOT%{beamerdir}/"
cp -f ./AUTHORS "$RPM_BUILD_ROOT%{beamerdir}/"
cp -f ./ChangeLog "$RPM_BUILD_ROOT%{beamerdir}/"

%if %{build_emacs}
mkdir -p $RPM_BUILD_ROOT%{emacsdir}/beamer
install -m 644 %{SOURCE1} "$RPM_BUILD_ROOT%{emacsdir}/beamer"
%endif

%if %{build_xemacs}
mkdir -p $RPM_BUILD_ROOT%{xemacsdir}/beamer
install -m 644 %{SOURCE1} "$RPM_BUILD_ROOT%{xemacsdir}/beamer"
%endif

chmod -R ugo+rX "$RPM_BUILD_ROOT%{beamerdir}"

%post
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%dir %{beamerdir}
%{beamerdir}/base
%{beamerdir}/emulation
%{beamerdir}/extensions
%{beamerdir}/themes
%{beamerdir}/solutions
%doc %{beamerdir}/doc
%doc %{beamerdir}/examples
%doc %{beamerdir}/AUTHORS
%doc %{beamerdir}/ChangeLog

%if %{build_emacs}
%files emacs
%defattr(-,root,root)
%{emacsdir}/beamer
%endif

%if %{build_xemacs}
%files xemacs
%defattr(-,root,root)
%{xemacsdir}/beamer
%endif

%changelog
* Tue May 01 2007 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to version 3.07 and remove -lyx

* Sat Nov 13 2004 Stephane <galland@arakhne.org> 3.1-1mdk
- This is mainly a bugfix release, but it includes much improved 
  verbatim management (you can now mix overlays and verbatims).

* Thu Oct 21 2004 Stephane <galland@arakhne.org> 3.0-1mdk
- first Mandrake's RPM version

* Tue Sep 21 2004 Stephane <galland@arakhne.org> 2.21-1
- first RPM version
