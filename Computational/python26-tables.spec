%define __python /usr/bin/python26
%{!?ython_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_siteinc: %define python_siteinc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")}

Name:           python26-tables
Version:        2.2.1
Release:        2%{?dist}
Summary:        Hierarchical datasets in Python

Group:          Development/Python
License:        BSD
URL:            http://www.pytables.org
Source0:        http://www.pytables.org/download/stable/tables-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python26-devel, python26-setuptools
BuildRequires:	bzip2-devel, lzo-devel
Requires: 	numpy26
Requires:	python26-numexpr >= 1.4.1
Provides:	python26-pytables = %{version}-%{release}
BuildRequires:	numpy26
BuildRequires:	python26-numexpr >= 1.4.1
BuildRequires: 	hdf5-devel >= 1.6.10
BuildRequires:	Cython26 >= 0.13, python26-Cython

%description
PyTables is a Python package for managing hierarchical datasets
designed to efficiently and easily cope with extremely large amounts
of data. It is built on top of the HDF5 library and the NumPy package
(numarray and Numeric are also supported). PyTables features an
object-oriented interface and performance-critical extensions coded in
C (generated using Pyrex) that make it a fast yet extremely
easy-to-use tool for interactively processing and searching through
very large amounts of data. PyTables also optimizes memory and disk
resources so that data occupies much less space than with other
solutions such as relational or object-oriented databases (especially
when compression is used).

%prep
%setup -q -n tables-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE* ANNOUNCE.txt RELEASE_NOTES.txt README.txt doc/* examples
%{_bindir}/*
%{python_sitearch}/tables/
%{python_sitearch}/tables-*.egg-info


%changelog
* Fri Aug 05 2011 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

