%define __python /usr/bin/python26
%{!?ython_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_siteinc: %define python_siteinc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")}

%define	module	numexpr

# hacks to work around spurious interpreter.so provides
%define my_provides %{_builddir}/my_provides
%define _use_internal_dependency_generator 0

Summary:	Fast numerical array expression evaluator for Python and NumPy
Name:		python26-%{module}
Version:	1.4.1
Release:	4%{?dist}
Source0:	http://numexpr.googlecode.com/files/%{module}-%{version}.tar.gz
License:	MIT
Group:		Development/Languages
URL:		http://numexpr.googlecode.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	numpy26 >= 1.4.1
BuildRequires:	numpy26 >= 1.4.1
BuildRequires:	python26-devel


%description
The numexpr package evaluates multiple-operator array expressions many
times faster than NumPy can. It accepts the expression as a string,
analyzes it, rewrites it more efficiently, and compiles it to faster
Python code on the fly. It's the next best thing to writing the
expression in C and compiling it with a specialized just-in-time (JIT)
compiler, i.e. it does not require a compiler at runtime.

%prep
%setup -q -n %{module}-%{version}

sed -i "s|/usr/bin/env python|%{__python}|" %{module}/cpuinfo.py

%{__cat} <<EOF >%{my_provides}
#!/bin/sh
%{__find_provides} | egrep -v '^interpreter.so$'
exit 0
EOF
chmod +x %{my_provides}
%define __find_provides %{my_provides}

%build
%{__python} setup.py build 

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build  --root=%{buildroot}
#This could be done more properly ?
chmod 0755 %{buildroot}%{python_sitearch}/%{module}/cpuinfo.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ANNOUNCE.txt LICENSE.txt RELEASE_NOTES.txt README.txt
%{python_sitearch}/numexpr/
%{python_sitearch}/numexpr-%{version}-py*.egg-info/

%changelog
* Fri Apr 29 2011 Thibault North <tnorth@fedoraproject.org> - 1.4.1-3
- Fix buildroot issue

* Tue Dec 21 2010 Thibault North <tnorth@fedoraproject.org> - 1.4.1-2
- Fixes for the review process

* Wed Nov 05 2010 Thibault North <tnorth@fedoraproject.org> - 1.4.1-1
- Initial package based on Mandriva's one

