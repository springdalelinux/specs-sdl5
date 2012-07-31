%define shortname xkeyval
%define name latex-%{shortname}
%define version 2.5f
%define release 2%{dist}

#%define texmfdir %{_datadir}/texmf
# move to localtexmf in PU_IAS 5
%define texmfdir /usr/local/share/texmf
%define texdir %{texmfdir}/tex
%define latexdir %{texdir}/latex
%define packagedir %{latexdir}/%{shortname}
%define lyxdir %{_datadir}/lyx
%define xemacsdir %{_datadir}/xemacs/xemacs-packages
%define emacsdir %{_datadir}/emacs/site-lisp

Summary: A LaTeX class for drawing
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://sourceforge.net/projects/latex-beamer/ 
Source0: %{shortname}.zip
License: GPL
Group: Publishing
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch
Requires: tetex >= 2.0.2, tetex-latex >= 2.0.2

%description
This package is an extension of the keyval package and offers additional macros for setting keys and declaring and setting class or package options. The package allows the programmer to specify a prefix to the name of the macros it defines for keys, and to define families of key definitions; these all help use in documents where several packages define their own sets of keys.

%prep
%setup -n %{shortname}

%build

%install
rm -rf "$RPM_BUILD_ROOT"
install --mode=0755 -d "$RPM_BUILD_ROOT%{texdir}"
install --mode=0755 -d "$RPM_BUILD_ROOT%{texdir}/generic/%{shortname}"
install --mode=0755 -d "$RPM_BUILD_ROOT%{latexdir}/%{shortname}"

cp -Rf ./run/*.tex "$RPM_BUILD_ROOT%{texdir}/generic/%{shortname}"
cp -Rf ./run/*.sty "$RPM_BUILD_ROOT%{latexdir}/%{shortname}"

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
%{texdir}/generic
%{latexdir}
%doc doc
%doc README

%changelog
* Tue Jan 30 2007 Thomas Uphill <uphill@ias.edu> 1.10
- first RPM version
