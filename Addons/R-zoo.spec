# This is the CRAN name
%global packname zoo
# This is the main package version
%global packver 1.7
# Note that some R packages do not use packrel
%global packrel 6

Name:             R-%{packname}
Version:          %{packver}.%{packrel}
Release:          2%{?dist}
Source0:          http://cran.r-project.org/src/contrib/%{packname}_%{packver}-%{packrel}.tar.gz
License:          GPLv2
URL:              http://cran.r-project.org/web/packages/zoo/index.html
Group:            Applications/Engineering
Summary:          Z's ordered observations for irregular time series
BuildRequires:    R-devel
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 5
BuildRequires:    tex(latex)
%else
BuildRequires:    tetex-latex
%endif
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         R-core


%description
An S3 class with methods for totally ordered indexed observations. It is
particularly aimed at irregular time series of numeric vectors/matrices and
factors. zoo's key design goals are independence of a particular index/date/
time class and consistency with with ts and base R by providing methods to
extend standard generics. 


%prep
%setup -q -c -n %{packname}
#Fix line endings
sed -i -e 's/\r//' zoo/inst/doc/zoo*.Rnw


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/R/library
%{_bindir}/R CMD INSTALL -l $RPM_BUILD_ROOT%{_libdir}/R/library %{packname}
# Clean up in advance of check
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -rf $RPM_BUILD_ROOT%{_libdir}/R/library/R.css
#Couple other doc files
cp -p zoo/THANKS zoo/WISHLIST $RPM_BUILD_ROOT%{_libdir}/R/library/%{packname}/


%check
#We have to use --no-install because we don't have all of the suggested
#dependencies
# Also, we can't run this test on el4 because tex is missing utf8.def
%if 0%{?rhel} >= 5
%{_bindir}/R CMD check --no-install %{packname}
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root, -)
%dir %{_libdir}/R/library/%{packname}
%doc %{_libdir}/R/library/%{packname}/demo
%doc %{_libdir}/R/library/%{packname}/doc
%doc %{_libdir}/R/library/%{packname}/html
%doc %{_libdir}/R/library/%{packname}/CITATION
%doc %{_libdir}/R/library/%{packname}/DESCRIPTION
%doc %{_libdir}/R/library/%{packname}/NEWS
%doc %{_libdir}/R/library/%{packname}/THANKS
%doc %{_libdir}/R/library/%{packname}/WISHLIST
%{_libdir}/R/library/%{packname}/INDEX
%{_libdir}/R/library/%{packname}/NAMESPACE
%{_libdir}/R/library/%{packname}/Meta
%{_libdir}/R/library/%{packname}/R
%{_libdir}/R/library/%{packname}/help
%{_libdir}/R/library/%{packname}/libs


%changelog
* Tue Nov 8 2011 Tom Callaway <spot@fedoraproject.org> 1.7.6-2
- disable tests on el4
- add el conditional for tex BR

* Tue Nov 8 2011 Tom Callaway <spot@fedoraproject.org> 1.7.6-1
- convert to new model
- rebuild for 2.14.0

* Mon Nov 7 2011 Orion Poplawski <orion@cora.nwra.com> 1.7-6
- Update to 1.7-6
- No longer noarch

* Tue Feb 8 2011 Orion Poplawski <orion@cora.nwra.com> 1.6-5
- Update to 1.6-4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 13 2010 Orion Poplawski <orion@cora.nwra.com> 1.6-3
- Update to 1.6-3

* Sun Jan 10 2010 Orion Poplawski <orion@cora.nwra.com> 1.6-2
- Update to 1.6-2

* Thu Nov 12 2009 Orion Poplawski <orion@cora.nwra.com> 1.5-9
- Rebuild for R 2.10.0

* Fri Oct 2 2009 Orion Poplawski <orion@cora.nwra.com> 1.5-8
- Update to 1.5-8

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 4 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-5
- Update to 1.5-4

* Tue May 20 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-4
- Add a couple more doc files

* Mon May 12 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-3
- Include time series in summary
- Fix up build requires for older versions

* Fri May 9 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-2
- Fix URL
- Fix line endings
- Change requires to tex(latex)

* Wed May 7 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-1
- Initial package creation
