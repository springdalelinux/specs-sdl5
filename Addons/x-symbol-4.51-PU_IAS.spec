Summary:     X-Symbol package for XEmacs (semi WYSIWYG for LaTeX, HTML)
Name:        x-symbol
Version:     4.51
Release:     4%{?dist}
License:   GPL
Group:       Applications/Publishing
Source:      %{name}-%{version}-src.tar.gz
Source1:     %{name}-init.el
Patch:      %{name}-PU_IAS.patch
URL:         http://x-symbol.sourceforge.net/
BuildArch:   noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: perl texinfo emacs texinfo-tex tetex tetex-dvips texi2html
Packager:	Thomas Uphill <uphill@ias.edu>

%description
X-Symbol is a package for XEmacs which provide some WYSIWYGness in an area
where it greatly enhance the readability of your LaTeX or HTML source: using
"real" characters for "tokens" like \oplus or &#trade;.

%package xemacs
Summary: An XEmacs mode providing WYSIWYG features.
Group: Applications/Editors
Requires: xemacs >= 20.4, ImageMagick
                                                                                                               
%description xemacs
When you edit LaTeX, HTML, BibTeX or TeXinfo sources in Emacs, package
X-Symbol provides some kind of WYSIWYG by using real characters for
tokens like \oplus or &trade;. It also provides various input methods
to insert these characters. Thumbnails for included images and real
super-/subscripts and are also supported.
                                                                                                               
This package contains the files needed by XEmacs.

To turn on x-symbol by default install %{name}-init.el from x-symbol doc dir
to %{_datadir}/xemacs/site-packages/lisp/site-start.d/%{name}-init.el
or add following lines to your .xemacs/init.el file:
(load-library "x-symbol")
(x-symbol-initialize)

%package emacs
Summary: An Emacs mode providing WYSIWYG features.
Group: Applications/Editors
Requires: emacs >= 21.1, ImageMagick
Requires: /sbin/install-info

%description emacs
When you edit LaTeX, HTML, BibTeX or TeXinfo sources in Emacs, package
X-Symbol provides some kind of WYSIWYG by using real characters for
tokens like \oplus or &trade;. It also provides various input methods
to insert these characters. Thumbnails for included images and real
super-/subscripts and are also supported.

This package contains the files needed by Emacs.

To turn on x-symbol by default install %{name}-init.el from x-symbol doc dir
to %{_datadir}/emacs/site-lisp/site-start.d/%{name}-init.el
or add following lines to your .emacs file:
(load-library "x-symbol")
(x-symbol-initialize)

#want to build in %{name}-%{version}, not %{name}, but someone disagrees
%prep
%setup -q -c -n %{name}-%{version}
mv %{name}/* .
rm -r %{name}
%patch -p1
cp %{SOURCE1} .
# we do not have xemacs hence fix references to it in docs
perl -pi -e 's|xemacs|emacs|' man/Makefile

%build
#with STAGING set, we can rebuild for emacs in the build dir and overwrite the elc's
#make -k binkit BUILD_MULE=t \
#	STAGING=${RPM_BUILD_ROOT}%{_prefix}/share/xemacs/xemacs-packages

#make emacs (patched Makefile.emacs, should work now)
make -f Makefile.emacs

#docs
cd man
make all
gzip *.ps

%install
install -d %{buildroot}%{_prefix}/share/emacs/site-lisp/%{name}
install -d %{buildroot}%{_prefix}/share/emacs/etc/%{name}
install lisp/*.el* %{buildroot}%{_prefix}/share/emacs/site-lisp/%{name}
install etc/* %{buildroot}%{_prefix}/share/emacs/etc/%{name}
rm -rf %{buildroot}%{_prefix}/share/xemacs

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_prefix}/share/doc/%{name}-%{version}/%{name}.info %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
	/sbin/install-info --delete %{_prefix}/share/doc/%{name}-%{version}/%{name}.info %{_infodir}/dir
fi

%files 
%defattr(-,root,root)
%doc README ChangeLog
%doc man/x-symbol/*.html
%doc man/*.info
%doc man/*.pdf
%doc man/*.ps.gz
%doc %{name}-init.el

#files xemacs
#defattr(-,root,root)
#dir %{_prefix}/share/xemacs/xemacs-packages/etc/x-symbol
#{_prefix}/share/xemacs/xemacs-packages/etc/x-symbol/*
#{_prefix}/share/xemacs/xemacs-packages/info/*
#dir %{_prefix}/share/xemacs/xemacs-packages/lisp/x-symbol
#{_prefix}/share/xemacs/xemacs-packages/lisp/x-symbol/*
#dir %{_prefix}/share/xemacs/xemacs-packages/man/x-symbol
#{_prefix}/share/xemacs/xemacs-packages/man/x-symbol/*
#{_prefix}/share/xemacs/xemacs-packages/pkginfo/*

%files emacs
%defattr(-,root,root)
%{_prefix}/share/emacs/site-lisp/x-symbol
%{_prefix}/share/emacs/etc/x-symbol

#---------------------------------------------------------------------
%changelog
* Fri Apr  6 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for and drop all use of xemacs in the build

* Thu Feb 24 2005 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for 2WS but because xemacs has it already, drop that part

* Sun Jun 15 2003 Thomas Uphill <uphill@ias.edu>
- 
* Wed Oct 23 2002 Ryurick M. Hristev <ryurick.hristev@canterbury.ac.nz>
- get rid of the '/usr/local/bin/perl' patch, no longer required

* Sat Oct 19 2002 Ryurick M. Hristev <ryurick.hristev@canterbury.ac.nz>
- up2date for 4.43
- minor fixes and improvements

* Mon Sep 3 2001 Ryurick M. Hristev <r.hristev@phys.canterbury.ac.nz>
- wrote first spec file

