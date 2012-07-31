%define gmthome %{_datadir}/GMT
%define gmtconf %{_sysconfdir}/GMT

%{!?octave_api: %define octave_api %(octave-config -p API_VERSION 2>/dev/null || echo 0)}
%define octave_mdir %(octave-config -p LOCALAPIFCNFILEDIR || echo)
%define octave_octdir %(octave-config -p LOCALAPIOCTFILEDIR || echo)

Name:           GMT
Version:        4.3.1
Release:        2%{?dist}
Summary:        Generic Mapping Tools

Group:          Applications/Engineering
License:        GPLv2
URL:            http://gmt.soest.hawaii.edu/
Source0:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_src.tar.bz2
Source1:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_share.tar.bz2
Source2:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_suppl.tar.bz2
Source3:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_scripts.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libXt-devel libXaw-devel libXmu-devel libXext-devel
BuildRequires:  netcdf-devel
BuildRequires:  GMT-coastlines
BuildRequires:  octave-devel
BuildRequires:  ncurses-devel
# less is detected by configure, and substituted in GMT.in
BuildRequires:  less
Requires:       less
Requires:       GMT-coastlines
Provides:       gmt = %{version}-%{release}

%description
GMT is an open source collection of ~60 tools for manipulating geographic and
Cartesian data sets (including filtering, trend fitting, gridding, projecting,
etc.) and producing Encapsulated PostScript File (EPS) illustrations ranging
from simple x-y plots via contour maps to artificially illuminated surfaces
and 3-D perspective views.  GMT supports ~30 map projections and transforma-
tions and comes with support data such as coastlines, rivers, and political
boundaries.

GMT is developed and maintained by Paul Wessel and Walter H. F.  Smith with
help from a global set of volunteers, and is supported by the National
Science Foundation.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       gmt-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        static
Summary:        Static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Provides:       gmt-static = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries for developing
applications that use %{name}.


%package        octave
Summary:        Octave libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       octave(api) = %{octave_api}
Provides:       gmt-octave = %{version}-%{release}

%description    octave
The %{name}-octave package contains and Octave interface for developing
applications that use %{name}.


%package        examples
Summary:        Generic Mapping Tools (Examples)
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
Provides:       gmt-examples = %{version}-%{release}

%description    examples
Example scripts for the Generic Mapping Tools.


# X11 application in a subpackage. No .desktop file since it
# requires a file name as argument
%package -n      xgridedit
Summary:         GMT grid code graphical editor
Group:           Applications/Engineering

%description -n xgridedit
XGridEdit is an application for viewing and editing the numerical values in
GMT 2 dimensional grids.


%prep
%setup -q -b1 -b2 -b3 -n GMT%{version}
#We don't care about .bat files
find -name \*.bat | xargs rm
#Fix permissions
find -name \*.c | xargs chmod a-x

%build
#So we execute do_examples.sh instead of do_examples.csh
export CSH=sh
export CFLAGS="$RPM_OPT_FLAGS -fPIC -I%{_includedir}/netcdf-3"
export NETCDF_LIB="%{_libdir}/netcdf-3"
%configure --datadir=%{gmthome} \
           --enable-shared \
           --enable-octave --enable-mex-mdir=%{octave_mdir} \
           --enable-mex-xdir=%{octave_octdir} \
           --disable-rpath --enable-www=%{_docdir}/%{name}-%{version}
make
make suppl


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -c -p'  install-all
#Setup configuration files 
mkdir -p $RPM_BUILD_ROOT%{gmtconf}/{mgg,dbase,mgd77,conf}
pushd $RPM_BUILD_ROOT%{gmthome}/
# put conf files in %{gmtconf} and do links in %{gmthome}
for file in conf/*.conf conf/gmtdefaults_* mgg/gmtfile_paths dbase/grdraster.info \
    mgd77/mgd77_paths.txt; do
  mv $file $RPM_BUILD_ROOT%{gmtconf}/$file
  ln -s ../../../../../%{gmtconf}/$file $RPM_BUILD_ROOT%{gmthome}/$file
done
popd
#Install examples
cp -pr examples $RPM_BUILD_ROOT/%{gmthome}
#Don't bring in csh for the csh examples
find $RPM_BUILD_ROOT/%{gmthome}/examples -name \*.csh | 
  xargs chmod a-x
# separate the README files that are associated with gmt main package
rm -rf __package_docs
mkdir __package_docs
cp -p src/*/README.* __package_docs
rm __package_docs/README.xgrid __package_docs/README.mex


%check
#Cleanup from previous runs
rm -f $RPM_BUILD_DIR/GMT%{version}/share/coast

#Setup environment for the tests
export GMT_SHAREDIR=$RPM_BUILD_DIR/GMT%{version}/share
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}

#Link in the coastline data
ln -s %{gmthome}/coast $RPM_BUILD_DIR/GMT%{version}/share

#Run the examples - not that this doesn't return errors if any fail, check logs!
make run-examples


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README __package_docs/* COPYING ChangeLog www/gmt/doc/html gmt_bench-marks
%dir %{gmtconf}
%dir %{gmtconf}/mgg
%dir %{gmtconf}/dbase
%dir %{gmtconf}/mgd77
%dir %{gmtconf}/conf
%config(noreplace) %{gmtconf}/conf/*
%config(noreplace) %{gmtconf}/mgg/gmtfile_paths
%config(noreplace) %{gmtconf}/dbase/grdraster.info 
%config(noreplace) %{gmtconf}/mgd77/mgd77_paths.txt
%{_bindir}/*
%exclude %{_bindir}/xgridedit
%{_libdir}/*.so.*
%dir %{gmthome}
%{gmthome}/*
%exclude %{gmthome}/examples
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*.3*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files octave
%defattr(-,root,root,-)
%{octave_mdir}/*.m
%{octave_octdir}/*.mex

%files examples
%defattr(-,root,root,-)
%doc %{gmthome}/examples

%files -n xgridedit
%defattr(-,root,root,-)
%doc src/xgrid/README.xgrid
%{_bindir}/xgridedit


%changelog
* Tue May 27 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-2
- Fix lowercase provides (bug #448263)

* Wed May 21 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-1
- Update to 4.3.1, drop upstreamed patches
- Remove other install fixes upstreamed

* Mon May 12 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.0-2
- Add patch to link libraries properly
- Run ldconfig in %%post, dummy
- Don't ship .bat file
- Don't ship .in files
- Don't make .csh examples executable
- Drop execute bit on .m files

* Tue May 6 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.0-1
- Update to 4.3.0, drop many upsreamed patches
- Add patch to install octave files in DESTDIR
- Add patch to fix segfaults due to uninitialized memory
- Add patch to fix a possible buffer overflow warning
- Remove duplicate html directory from examples package
- Create __package_docs directory for main package docs

* Tue Apr 28 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-3
- Remove unfree source
- Split out xgridedit into sub-package
- Add BR and R on less
- Redirect octave-config stderr to /dev/null
- Move config files to /etc/GMT
- Use install -c -p to preserve timestamps
- Use cp -pr to copy share data
- Add sonames to shared libraries

* Mon Mar 24 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-2
- Drop -doc sub-package, will have separate -docs package
- Add lower case name provides
- Build Octave files

* Mon Mar 17 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-1
- Initial version
