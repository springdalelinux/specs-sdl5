%{!?_texmf: %define _texmf %(eval "echo `kpsewhich -expand-var '$TEXMFMAIN'`")}

%define emacs_sitelisp  %{_datadir}/emacs/site-lisp
%define xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp

Name:           asymptote
Version:        1.26
Release:        1%{?dist}
Summary:        Descriptive vector graphics language

Group:          Applications/Publishing
License:        GPL
URL:            http://asymptote.sourceforge.net/
Source:         http://dl.sourceforge.net/sourceforge/asymptote/asymptote-%{version}.src.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  fftw-devel >= 3.0
BuildRequires:  gc-devel >= 6.8
BuildRequires:  gsl-devel
BuildRequires:  tetex-latex
BuildRequires:  ghostscript
BuildRequires:  texinfo-tex
BuildRequires:  ImageMagick

Requires:       tetex-latex
Requires:       tkinter
Requires(post): /usr/bin/texhash /sbin/install-info
Requires(postun): /usr/bin/texhash /sbin/install-info

%define texpkgdir   %{_texmf}/tex/latex/%{name}

%description
Asymptote is a powerful descriptive vector graphics language for technical
drawings, inspired by MetaPost but with an improved C++-like syntax.
Asymptote provides for figures the same high-quality level of typesetting
that LaTeX does for scientific text.


%prep
%setup -q
%{__sed} -i 's|^#!/usr/bin/env python$|#!%{__python}|' xasy
%{__sed} -i 's/\r//' doc/CAD1.asy


%build
%configure --enable-gc=system --with-docdir=%{_defaultdocdir}/%{name}-%{version}/
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install-all DESTDIR=$RPM_BUILD_ROOT

install -p -m 644 BUGS ChangeLog LICENSE README ReleaseNotes TODO \
    $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/

# Emacs/Xemacs mode and init files
for dir in %{emacs_sitelisp} %{xemacs_sitelisp} ; do
  install -dm 755 $RPM_BUILD_ROOT$dir/site-start.d
  ln -s %{_datadir}/%{name}/asy-mode.el $RPM_BUILD_ROOT$dir
  touch $RPM_BUILD_ROOT$dir/asy-mode.elc
  ln -s %{_datadir}/%{name}/asy-init.el $RPM_BUILD_ROOT$dir/site-start.d
  touch $RPM_BUILD_ROOT$dir/site-start.d/asy-init.elc
done

# Vim syntax file
for vimver in 63 64 70 ; do
    install -dm 755 $RPM_BUILD_ROOT%{_datadir}/vim/vim$vimver/syntax
    ln -s %{_datadir}/%{name}/asy.vim $RPM_BUILD_ROOT%{_datadir}/vim/vim$vimver/syntax
done


%clean
rm -rf $RPM_BUILD_ROOT


%post
texhash >/dev/null 2>&1 || :
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :

%postun
texhash >/dev/null 2>&1 || :
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :
fi


%triggerin -- emacs-common
[ -d %{emacs_sitelisp} ] && \
    ln -sf %{_datadir}/%{name}/asy-mode.el %{emacs_sitelisp} || :
[ -d %{emacs_sitelisp}/site-start.d ] && \
    ln -sf %{_datadir}/%{name}/asy-init.el %{emacs_sitelisp}/site-start.d || :

%triggerin -- xemacs-common
[ -d %{xemacs_sitelisp} ] && \
    ln -sf %{_datadir}/%{name}/asy-mode.el %{xemacs_sitelisp} || :
[ -d %{xemacs_sitelisp}/site-start.d ] && \
    ln -sf %{_datadir}/%{name}/asy-init.el %{xemacs_sitelisp}/site-start.d || :

%triggerun -- emacs-common
[ $2 = 0 ] && rm -f %{emacs_sitelisp}/{asy-mode.el*,site-start.d/asy-init.el*} || :

%triggerun -- xemacs-common
[ $2 = 0 ] && rm -f %{xemacs_sitelisp}/{asy-mode.el*,site-start.d/asy-init.el*} || :


%triggerin -- vim-common
VIMVERNEW=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | tail -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
[ -d %{_datadir}/vim/vim${VIMVERNEW}/syntax ] && \
  ln -sf %{_datadir}/%{name}/asy.vim %{_datadir}/vim/vim${VIMVERNEW}/syntax || :

%triggerun -- vim-common
VIMVEROLD=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | head -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
[ $2 = 0 ] && rm -f %{_datadir}/vim/vim${VIMVEROLD}/syntax/asy.vim || :

%triggerpostun -- vim-common
VIMVEROLD=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | head -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
VIMVERNEW=`rpm -q --qf='%%{epoch}:%%{version}\n' vim-common | sort | tail -n 1 | sed -e 's/[0-9]*://' | sed -e 's/\.[0-9]*$//' | sed -e 's/\.//'`
if [ $1 = 1 ]; then
    rm -f %{_datadir}/vim/vim${VIMVEROLD}/syntax/asy.vim || :
    [ -d %{_datadir}/vim/vim${VIMVERNEW}/syntax ] && \
        ln -sf %{_datadir}/%{name}/asy.vim %{_datadir}/vim/vim${VIMVERNEW}/syntax || :
fi


%files
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}-%{version}/
%{_bindir}/*
%{_datadir}/%{name}/
%{texpkgdir}/
%{_mandir}/man1/*.1*
%{_infodir}/*.info*
%ghost %{_datadir}/*emacs
%ghost %{_datadir}/vim/


%changelog
* Wed Apr 25 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.26-1
- Update to 1.26.

* Tue Apr 10 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.25-1
- Update to 1.25.

* Sun Apr  1 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Sun Mar 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.23-1
- Update to 1.23.

* Tue Mar  6 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Sat Mar  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.21-1
- Update to 1.21.

* Fri Dec 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- Update to 1.20.

* Sat Dec 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.19-1
- Update to 1.19.

* Sun Nov  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-1
- Update to 1.18.

* Wed Nov  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-1
- Update to 1.17.

* Wed Oct 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Sun Oct 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-1
- Update to 1.13.

* Thu Aug  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Thu Jul  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Wed Jun 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Fri Jun 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.

* Thu Jun 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.
- Also installs the info file.

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-5
- Fedora Core 6: the texinfo package has been splitted (texinfo + texinfo-tex).

* Sat May 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-4
- Group: Development/Tools -> Applications/Publishing (#193154).

* Sat May 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-3
- Emacs/Xemacs init file (#193154 comment 6).

* Fri May 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-2
- Directories ownership (#193154).

* Wed May 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.
- Using triggers to install the Vim syntax file and the Emacs/Xemacs mode file.

* Mon May 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Sun May  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Fri Mar 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Thu Mar 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- First build.

# vim:set ai ts=4 sw=4 sts=4 et:
