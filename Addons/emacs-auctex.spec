Summary: 	Enhanced TeX modes for Emacs
Name: 		emacs-auctex
Version: 	11.86
Release: 	1%{?dist}
License: 	GPL
Group: 		Applications/Editors
URL: 		http://www.gnu.org/software/auctex/
Source0: 	ftp://ftp.gnu.org/pub/gnu/auctex/auctex-%{version}.tar.gz
BuildArch: 	noarch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: 	auctex
Provides: 	auctex
Conflicts: 	emacspeak < 18
Requires: 	emacs emacs-common ghostscript 
Requires: 	tetex-preview = %{version}-%{release}
Requires: 	/sbin/install-info
BuildRequires: 	emacs tetex-latex texinfo-tex ghostscript

%description 
AUCTeX is an extensible package that supports writing and formatting
TeX files for most variants of Emacs.

AUCTeX supports many different TeX macro packages, including AMS-TeX,
LaTeX, Texinfo and basic support for ConTeXt.  Documentation can be
found under /usr/share/doc, e.g. the reference card (tex-ref.pdf) and
the FAQ. The AUCTeX manual is available in Emacs info (C-h i d m
AUCTeX RET). On the AUCTeX home page, we provide manuals in various
formats.

AUCTeX includes preview-latex support which makes LaTeX a tightly
integrated component of your editing workflow by visualizing selected
source chunks (such as single formulas or graphics) directly as images
in the source buffer.

This package is for GNU Emacs.

%package el
Summary: 	Elisp source files for %{name}
Group: 		Applications/Editors
Requires: 	%{name} = %{version}

%description el
This package contains the source Elisp files for AUCTeX for Emacs.

%package doc
Summary:	Documentation in various formats for AUCTeX
Group:		Documentation

%description doc
Documentation for the AUCTeX package for emacs in various formats,
including HTML and PDF.

%package -n tetex-preview
Summary: 	Preview style files for LaTeX
Group: 		Applications/Publishing
Requires: 	tetex-latex tetex-fonts ghostscript

%description -n tetex-preview 
The preview package for LaTeX allows for the processing of selected
parts of a LaTeX input file.  This package extracts indicated pieces
from a source file (typically displayed equations, figures and
graphics) and typesets with their base point at the (1in,1in) magic
location, shipping out the individual pieces on separate pages without
any page markup.  You can produce either DVI or PDF files, and options
exist that will set the page size separately for each page.  In that
manner, further processing (as with Ghostscript or dvipng) will be
able to work in a single pass.

The main purpose of this package is the extraction of certain
environments (most notably displayed formulas) from LaTeX sources as
graphics. This works with DVI files postprocessed by either Dvips and
Ghostscript or dvipng, but it also works when you are using PDFTeX for
generating PDF files (usually also postprocessed by Ghostscript).

The tetex-preview package is generated from the AUCTeX package for
Emacs.

%prep
%setup -q -n auctex-%{version}

%build
%configure --with-emacs 
make

# Build documentation in various formats
pushd doc
make extradist
popd

%install
rm -rf %{buildroot}

%define startupdir %{_datadir}/emacs/site-lisp/site-start.d
%define startupfile %{startupdir}/auctex-init.el

mkdir -p %{buildroot}%{startupdir}

make DESTDIR=%{buildroot} install

# Startup file.
cat <<EOF > %{buildroot}%{startupfile}
;; This enables AUCTeX globally.
;; See (info "(auctex)Introduction") on how to disable AUCTeX.
;; Created for %{name}-%{version}-%{release}.noarch.rpm
(load "auctex.el" nil t t)

;; This enables preview-latex globally.
;; Created for %{name}-%{version}-%{release}.noarch.rpm
(load "preview-latex.el" nil t t)
EOF
rm -rf %{buildroot}%{_var}

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/auctex.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/preview-latex.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/auctex.info %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/preview-latex.info %{_infodir}/dir 2>/dev/null || :
fi

%post -n tetex-preview
/usr/bin/texhash > /dev/null 2>&1 || :

%postun -n tetex-preview
/usr/bin/texhash > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc RELEASE COPYING README TODO FAQ CHANGES
%doc %{_infodir}/*.info*
%exclude %{_infodir}/dir
%{startupdir}
%dir %{_datadir}/emacs/site-lisp/auctex
%dir %{_datadir}/emacs/site-lisp/auctex/style
%{_datadir}/emacs/site-lisp/auctex/*.elc
%{_datadir}/emacs/site-lisp/auctex/style/*.elc
%{_datadir}/emacs/site-lisp/auctex/.nosearch
%{_datadir}/emacs/site-lisp/auctex/style/.nosearch
%{_datadir}/emacs/site-lisp/auctex/images
%{_datadir}/emacs/site-lisp/tex-site.el

%files doc
%doc doc/*.{dvi,ps,pdf}
%doc doc/html
%{_datadir}/doc/auctex/tex-ref.pdf

%files -n tetex-preview
%defattr(-,root,root,-)
%{_datadir}/texmf/tex/latex/preview
%{_datadir}/texmf/doc/latex/styles

%files el
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/auctex/*.el
%{_datadir}/emacs/site-lisp/auctex/style/*.el

%changelog
* Wed Oct 20 2010 Thomas Uphill <uphill@ias.edu> - 11.86-1
- update to 11.86

* Sat Jan 13 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-2
- Update BuildRequires for texinfo-tex package

* Sat Jan 13 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.84-1
- Update to version 11.84
- Build all documentation and package in a -doc package

* Mon Aug 28 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-7
- Bump release for FC-6 mass rebuild

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-6
- Remove debug patch entry

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-5
- Bump release

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-4
- Bump release

* Sun Jun 18 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-3
- Sync with FC-5 spec file which includes the following changes
- No longer use makeinstall macro
- No longer specify texmf-dir, tex-dir for configure
- Main package now owns the site-lisp auctex and styles directories
- Place preview.dvi in correct directory, and have tetex-preview own
  it
- General cleanups

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-4
- Bump release

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-3
- Bump release. Wrap descriptions at column 70.

* Sat Jun 10 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 11.83-1
- Update to 11.83
- Add specific release requirement to tetex-preview Requires of main package

* Wed May 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-12
- Bump version number.

* Wed May 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-11
- Fix up whitespace for Ed. Bump version number.

* Thu May 18 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-9
- Split out tetex-preview subpackage
- Split out source elisp files
- Update package descriptions

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-8
- Add tetex-latex to BuildRequires

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-7
- Add ghostscript to Requires and BuildRequires

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-6
- Leave .nosearch file in styles directory - this directory shouldn't be in the load-path

* Mon May  1 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-5
- Move installation of the preview style files out of the texmf tree for now

* Mon Apr 24 2006 Jonathan Underwood <jonathan.underwood@gmail.com> - 11.82-4
- Added preview-latex
- Removed INSTALL document from package (not necessary)
- Clean up generation of startup files from spec file

* Thu Apr 20 2006 Ed Hill <ed@eh3.com> - 11.82-3
- fix startup file per bug# 189488

* Sun Apr  9 2006 Ed Hill <ed@eh3.com> - 11.82-2
- rebuild

* Sun Apr  9 2006 Ed Hill <ed@eh3.com> - 11.82-1
- update to 11.82

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 11.81-2
- fix stupid tagging mistake

* Fri Sep 30 2005 Ed Hill <ed@eh3.com> - 11.81-1
- update to 11.81
- disable preview for now since it needs some packaging work

* Tue Sep  6 2005 Ed Hill <ed@eh3.com> - 11.55-5
- bugzilla 167439

* Tue Aug  9 2005 Ed Hill <ed@eh3.com> - 11.55-4
- call it BuildArch

* Tue Aug  9 2005 Ed Hill <ed@eh3.com> - 11.55-3
- add Requires and BuildRequires

* Mon Aug  8 2005 Ed Hill <ed@eh3.com> - 11.55-2
- modify for acceptance into Fedora Extras

* Fri Jan 21 2005 David Kastrup <dak@gnu.org>
- Conflict with outdated Emacspeak versions

* Fri Jan 14 2005 David Kastrup <dak@gnu.org>
- Install and remove auctex.info, not auctex

* Thu Aug 19 2004 David Kastrup <dak@gnu.org>
- Change tex-site.el to overwriting config file mode.  New naming scheme.

* Mon Aug 16 2004 David Kastrup <dak@gnu.org>
- Attempt a bit of SuSEism.  Might work if we are lucky.

* Sat Dec  7 2002 David Kastrup <David.Kastrup@t-online.de>
- Change addresses to fit move to Savannah.

* Mon Apr 15 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Adjusted TeX-macro-global and put autoactivation in preinstall
  script so that it can be chosen at install time.

* Tue Feb 19 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Added site-start.el support

* Sat Feb 16 2002 Jan-Ake Larsson <jalar@imf.au.dk>
- Prerelease 11.11
