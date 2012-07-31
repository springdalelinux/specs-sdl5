%define texmfdir /texmf/tex/latex/graphics

Summary:	"Purifies" eps files for use by both dvips and pdflatex 
Name:		purifyeps
Version:	1.0
Release:	2%{?dist}
License:	distributable
Source: 	ftp://ftp.ctan.org/tex-archive/support/purifyeps.tar.gz
URL:            http://www.ctan.org/tex-archive/support/purifyeps
Source1:        eps2mps.tex
Group:		Applications/Graphics
Requires:	pstoedit >= 3.10 perl >= 5.006 tetex 
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildArch:      noarch

%description
purifyeps is a perl script that uses pstoedit and mpost to 'purify' (modify) 
*.eps graphics files used by dvips so that they can also be used by pdflatex.
This removes the need to maintain graphics files in two different formats when 
both *.ps and *.pdf documents must be produced.   A preamble to the LaTeX file 
that tells pdflatex to interpret the purified *.eps files as 'mps' format is 
all that is needed for pdflatex to work (see the purifyeps manpage for the 
text of this preamble, or add '\include{eps2mps}' to the preamble of the 
LaTeX document).  See the pstoedit website http://www.pstoedit.net/pstoedit 
for details of the required pstoedit tool. 

%prep
%setup -n purifyeps

%build
cp $RPM_SOURCE_DIR/eps2mps.tex .

%install
rm -rf  $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 purifyeps $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 purifyeps.1 $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}%{texmfdir}
install -m 644 eps2mps.tex $RPM_BUILD_ROOT%{_datadir}%{texmfdir}

%post
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
[ -x /sbin/restorecon ] && /sbin/restorecon -R /usr/share/texmf/ 2> /dev/null

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README purifyeps.pdf eps2mps.tex
%{_bindir}/purifyeps
%{_datadir}%{texmfdir}/*
%{_mandir}/man1/*.1*

%changelog
* Thu Apr 05 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for 5

* Thu May 01 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for 9

* Thu Mar 20 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS

* Fri Feb 14 2003 Duncan Haldane <haldane@princeton.edu>
- initial rpm package

