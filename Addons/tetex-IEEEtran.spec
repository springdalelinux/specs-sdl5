%{!?_texmf: %define _texmf %(eval "echo `kpsewhich -expand-var '$TEXMFMAIN'`")}

%define texpkg      IEEEtran
%define texpkgdir   %{_texmf}/tex/latex/%{texpkg}
%define texpkgdoc   %{_texmf}/doc/latex/%{texpkg}
%define bibpkgdir   %{_texmf}/bibtex/bib/%{texpkg}
%define bstpkgdir   %{_texmf}/bibtex/bst/%{texpkg}
%define bibpkgdoc   %{_texmf}/doc/bibtex/%{texpkg}

Name:           tetex-%{texpkg}
Version:        1.6.3
Release:        2%{?dist}
Summary:        Official LaTeX class for IEEE transactions journals and conferences

Group:          Applications/Publishing
License:        Artistic
URL:            http://www.ctan.org/tex-archive/help/Catalogue/entries/ieeetran.html
Source0:        ftp://ftp.dante.de/tex-archive/macros/latex/contrib/IEEEtran.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  tetex-latex
Requires:       tetex-latex
Requires(post): /usr/bin/texhash
Requires(postun): /usr/bin/texhash

%description
The IEEEtran class is the official LaTeX class for authors of the
Institute of Electrical and Electronics Engineers (IEEE) transactions
journals and conferences. 

%prep
%setup -q -n %{texpkg}
mv extras/tux.eps .
mv bibtex/README README_BIBTEX
mv tools/README README_TOOLS

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT{%{texpkgdir},%{texpkgdoc}}
install -p -m 644 IEEEtran.cls $RPM_BUILD_ROOT%{texpkgdir}/
install -p -m 644 tools/IEEEtrantools.sty $RPM_BUILD_ROOT%{texpkgdir}/
install -p -m 644 IEEEtran_HOWTO.pdf $RPM_BUILD_ROOT%{texpkgdoc}/
install -p -m 644 tools/IEEEtrantools_doc.txt $RPM_BUILD_ROOT%{texpkgdoc}/

install -d -m 755 $RPM_BUILD_ROOT{%{bibpkgdir},%{bstpkgdir},%{bibpkgdoc}}
install -p -m 644 bibtex/*.bib $RPM_BUILD_ROOT%{bibpkgdir}/
install -p -m 644 bibtex/*.bst $RPM_BUILD_ROOT%{bstpkgdir}/
install -p -m 644 bibtex/IEEEtran_bst_HOWTO.pdf $RPM_BUILD_ROOT%{bibpkgdoc}/

%clean
rm -rf $RPM_BUILD_ROOT


%post
texhash >/dev/null 2>&1 || :

%postun
texhash >/dev/null 2>&1 || :

%triggerin -- lyx
if [ $2 -gt 1 ]; then
cd %{_datadir}/lyx && \
  ./configure --without-latex-config > /dev/null 2>&1 ||:
fi

%triggerun -- lyx
if [ $2 -eq 0 ]; then
cd %{_datadir}/lyx && \
  ./configure --without-latex-config > /dev/null 2>&1 ||:
fi


%files
%defattr(-,root,root,-)
%doc README README_BIBTEX README_TOOLS bare_conf.tex bare_jrnl.tex tux.eps
%{texpkgdir}/
%{texpkgdoc}/
%{bibpkgdir}/
%{bstpkgdir}/
%{bibpkgdoc}/


%changelog
* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.6.3-2
- Bump release for mass rebuild

* Tue Jul 25 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.6.3-1
- Removed alpha character from version
- Added lyx triggers provided by Rex Dieter
- Removed notice for Lyx users
- Did some minor cleanup of the sources

* Fri Jul 21 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.6c-3
- Added note to Lyx users in description

* Wed Jun 21 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.6c-2
- Changed License tag from Perl Artistic License to Artistic
- Added IEEEtrantools to package
- Put full URL into source

* Sun Jun 18 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.6c-1
- Initial release based on tetex-bytefield
