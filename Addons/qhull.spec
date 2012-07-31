Summary: General dimension convex hull programs
Name: qhull
Version: 2003.1
Release: 6%{?dist}
License:  Distributable
Group: System Environment/Libraries
Source0: http://www.qhull.org/download/qhull-%{version}.tar.gz
URL: http://www.qhull.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%package devel
Group: Development/Libraries
Summary: Development files for qhull
Requires: %{name} = %{version}-%{release}

%description devel
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%prep
%setup -n %{name}-%{version}
sed -i -e "s,\"../html/,\"html/,g" src/*.htm

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT \
  docdir=%{_docdir}/%{name}-%{version} install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}
%_bindir/*
%_libdir/*.so.*
%_mandir/man1/*

%files devel
%defattr(-,root,root)
%_libdir/*.*a
%_libdir/*.so
%_includedir/*

%changelog
* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 2003.1-6
- Mass rebuild.

* Fri Feb 17 2006 Ralf Corsépius <rc040203@freenet.de>	- 2003.1-5
- Disable static libs.
- Fixup some broken links in doc.
- Add %%{?dist}.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2003.1-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Aug 08 2004 Ralf Corsepius <ralf[AT]links2linux.de>	- 2003.1-0.fdr.2
- Use default documentation installation scheme.

* Fri Jul 16 2004 Ralf Corsepius <ralf[AT]links2linux.de>	- 2003.1-0.fdr.1
- Initial Fedora RPM.
