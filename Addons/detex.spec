%define texmfdir /texmf/tex/latex/graphics

Summary:	Removes (La)Tex commands from input, gives plain text output. 
Name:		detex
Version:	2.7
Release:	2%{?dist}
License:	distributable
URL: 		http://www.cs.purdue.edu/homes/trinkle/detex
Source:         http://www.cs.purdue.edu/homes/trinkle/detex/detex-%{version}.tar.gz
Group:		Applications/Publishing
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
DeTeX is a filter program that removes the LaTeX (or TeX) control sequences 
from the input so that the real content can be passed to a spell or diction 
checker. 

%prep
%setup 

%build
make DEFS="-DNO_MALLOC_DECL -DHAVE_STRING_H"

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 detex $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mv detex.1l detex.1
install -m 644 detex.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README 
%{_bindir}/detex
%{_mandir}/man1/*.1*

%changelog
* Fri Mar 30 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS 5

* Tue Feb 22 2005 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS 2WS

* Tue May 06 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS RH 9

* Thu Mar 20 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS

* Fri Feb 14 2003 Duncan Haldane <haldane@princeton.edu>
- initial rpm package

