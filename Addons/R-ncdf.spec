# This is the CRAN name
%define packname ncdf

Name:             R-%{packname}
Version:          1.6.6
Release:          2.1%{?dist}
Source0:          http://cran.r-project.org/src/contrib/%{packname}_%{version}.tar.gz
License:          GPLv2
URL:              http://cran.r-project.org/web/packages/ncdf/index.html
Group:            Applications/Engineering
Summary:          ncdf: Interface to Unidata netCDF data files
BuildRequires:    R-devel
BuildRequires:    tetex-latex
%if "%rhel" < "5"
BuildRequires:    netcdf-gcc-devel
Requires:	  netcdf-gcc
%define	extraconfig %{nil}
%else
BuildRequires:    netcdf-devel netcdf-static
Requires:         netcdf
%define extraconfig --configure-args="--with-netcdf-include=/usr/include/netcdf-3"
%endif
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post):   R-core libRmath
Requires(postun): R-core libRmath
Requires:         R-core libRmath


%description
This package provides a high-level R interface to Unidata's netCDF data files,
which are portable across platforms and include metadata information in 
addition to the data sets. Using this package netCDF files can be opened and 
data sets read in easily. It is also easy to create new netCDF dimensions, 
variables, and files, or manipulate existing netCDF files. This interface 
provides considerably more functionality than the old "netCDF" package for R, 
and is not compatible with the old "netCDF" package for R.

%prep
%setup -q -c -n %{packname}

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/R/library
export NETCDF_INCLUDE=/usr/include/netcdf-3
%{_bindir}/R CMD INSTALL -l $RPM_BUILD_ROOT%{_libdir}/R/library %{packname}
%{_bindir}/R CMD check %{packname}
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -rf $RPM_BUILD_ROOT%{_libdir}/R/library/R.css

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_R_make_search_index}

%postun
%{_R_make_search_index}

%files
%defattr(-, root, root, -)
%dir %{_libdir}/R/library/%{packname}
%doc %{_libdir}/R/library/%{packname}/html
%doc %{_libdir}/R/library/%{packname}/DESCRIPTION
%{_libdir}/R/library/%{packname}/NAMESPACE
%{_libdir}/R/library/%{packname}/INDEX
%{_libdir}/R/library/%{packname}/Meta
%{_libdir}/R/library/%{packname}/R
%{_libdir}/R/library/%{packname}/help
%{_libdir}/R/library/%{packname}/libs

%changelog
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
