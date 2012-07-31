%define shortname pgf
%define name latex-%{shortname}
%define version 1.10
%define release 2%{dist}

%define texmfdir /usr/local/share/texmf
%define texdir %{texmfdir}/tex
%define latexdir %{texmfdir}/latex
%define packagedir %{latexdir}/%{shortname}
%define lyxdir %{_datadir}/lyx
%define xemacsdir %{_datadir}/xemacs/xemacs-packages
%define emacsdir %{_datadir}/emacs/site-lisp

Summary: A LaTeX class for drawing
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://sourceforge.net/projects/latex-beamer/
Source0: %{shortname}-%{version}.tar.gz
License: GPL
Group: Publishing
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch
Requires: tetex >= 2.0.2, tetex-latex >= 2.0.2, latex-xkeyval >= 2.5

%description
PGF is a TeX macro package for generating graphics. It is platform- and format-independent and works together with the most important TeX backend drivers, including pdftex and dvips. It comes with a user-friedly syntax layer called TikZ.

%prep
%setup -n %{shortname}-%{version}

%build

%install
rm -rf "$RPM_BUILD_ROOT"
install --mode=0755 -d "$RPM_BUILD_ROOT%{texdir}"

cp -Rf ./latex "$RPM_BUILD_ROOT%{texdir}/"
cp -Rf ./plain "$RPM_BUILD_ROOT%{texdir}/"
cp -Rf ./generic "$RPM_BUILD_ROOT%{texdir}/"
cp -Rf ./context "$RPM_BUILD_ROOT%{texdir}/"

chmod -R ugo+rX "$RPM_BUILD_ROOT%{texdir}"

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
%dir %{texdir}
%{texdir}/latex
%{texdir}/plain
%{texdir}/generic
%{texdir}/context
%doc doc
%doc README

%changelog
* Tue Jan 30 2007 Thomas Uphill <uphill@ias.edu> 1.10
- first RPM version
