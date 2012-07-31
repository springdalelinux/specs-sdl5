Name:           ncarg
Version:        4.4.1
Release:        9%{?dist}
Summary:        A Fortran and C based software package for scientific visualization
Group:          Development/Libraries
License:        GPL
URL:            http://ngwww.ucar.edu/ng4.4/index.html
Source0:        http://ngwww.ucar.edu/ngbin/ncarg-%{version}.src.tar.gz
Source1:        Site.local
Source2:        ncarg.csh
Source3:        ncarg.sh
Patch1:         ncarg-4.4.1-config.patch
Patch2:         ncarg-4.4.1-include.patch
Patch3:         ncarg-4.4.1-rpmroot.patch
Patch4:         ncarg-4.4.1-deps.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  /bin/csh, gcc-gfortran >= 4.1.0, hdf-devel, libjpeg-devel
BuildRequires:  imake, libXt-devel, libXaw-devel, libXext-devel, libXpm-devel

%description
NCAR Graphics is a Fortran and C based software package for scientific
visualization.

%package devel
Summary:        A Fortran and C based software package for scientific visualization
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Include files and libraries for NCAR Graphics

%prep
%setup -q
%patch1 -p 1 -b .config
%patch2 -p 1 -b .include
%patch3 -p 1 -b .rpmroot
%patch4 -p 1 -b .deps
cp %{SOURCE1} config
#Fix up the lib install dir
cp %{SOURCE2} %{SOURCE3} .
sed -i -e s,/LIB/,/%{_lib}/, config/Site.local ncarg.csh ncarg.sh


%build
export NCARG=`pwd`
echo n | ./Configure
make %{?_smp_mflags} Build


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install ncarg.csh ncarg.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
# Don't conflict with allegro-devel (generic API names)
for manpage in $RPM_BUILD_ROOT%{_mandir}/man3/*
do
   manname=`basename $manpage`
   mv $manpage $RPM_BUILD_ROOT%{_mandir}/man3/%{name}_$manname
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING Copyright README
%{_sysconfdir}/profile.d/ncarg.*sh
%{_bindir}/ConvertMapData
%{_bindir}/WriteLineFile
%{_bindir}/WriteNameFile
%{_bindir}/WritePlotcharData
%{_bindir}/cgm2ncgm
%{_bindir}/ctlib
%{_bindir}/ctrans
%{_bindir}/ezmapdemo
%{_bindir}/fcaps
%{_bindir}/findg
%{_bindir}/fontc
%{_bindir}/gcaps
%{_bindir}/graphc
%{_bindir}/ictrans
%{_bindir}/idt
%{_bindir}/med
%{_bindir}/ncargfile
%{_bindir}/ncargpath
%{_bindir}/ncargrun
%{_bindir}/ncargversion
%{_bindir}/ncargworld
%{_bindir}/ncarlogo2ps
%{_bindir}/ncarvversion
%{_bindir}/ncgm2cgm
%{_bindir}/ncgmstat
%{_bindir}/nnalg
%{_bindir}/pre2ncgm
%{_bindir}/pre2ncgm.prog
%{_bindir}/psblack
%{_bindir}/psplit
%{_bindir}/pswhite
%{_bindir}/pwritxnt
%{_bindir}/ras2ccir601
%{_bindir}/rascat
%{_bindir}/rasgetpal
%{_bindir}/rasls
%{_bindir}/rassplit
%{_bindir}/rasstat
%{_bindir}/rasview
%{_bindir}/tdpackdemo
%{_bindir}/tgks0a
%{_bindir}/tlocal
%dir %{_libdir}/ncarg
%dir %{_libdir}/ncarg/ncarg
%{_libdir}/ncarg/ncarg/database/
%{_libdir}/ncarg/ncarg/fontcaps/
%{_libdir}/ncarg/ncarg/graphcaps/
%{_libdir}/ncarg/ncarg/ngwww/
%{_libdir}/ncarg/ncarg/robj/
%{_libdir}/ncarg/ncarg/xapp/
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz

%files devel
%{_bindir}/ncargcc
%{_bindir}/ncargex
%{_bindir}/ncargf90
%{_includedir}/ncarg/
%{_libdir}/ncarg/libcgm.a
%{_libdir}/ncarg/libncarg.a
%{_libdir}/ncarg/libncarg_c.a
%{_libdir}/ncarg/libncarg_gks.a
%{_libdir}/ncarg/libncarg_ras.a
%{_libdir}/ncarg/libngmath.a
%{_libdir}/ncarg/ncarg/examples/
%{_libdir}/ncarg/ncarg/tests/
%{_libdir}/ncarg/ncarg/tutorial/
%{_mandir}/man3/*.gz


%changelog
* Mon Feb 12 2007 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-9
- Fix up the source files that were modified then checked in :-(.

* Fri Feb 09 2007 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-8
- Don't modify SOURCE files directly

* Fri Jan 26 2007 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-7
- Bump release to try to get fixed version out for bug #223420

* Mon Jan 22 2007 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-6
- Revert to 4.4.1, no 4.4.2 ever was released into the wild.
- Add patch to fix NCARG_ROOT in binaries.
- Add patch to fix dependency in fontcap.
- Tweak compile defines

* Fri Jan 19 2007 - Orion Poplawski <orion@cora.nwra.com> - 4.4.2-3
- Never seemed to make it into FC6

* Wed Oct  3 2006 - Orion Poplawski <orion@cora.nwra.com> - 4.4.2-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 - Orion Poplawski <orion@cora.nwra.com> - 4.4.2-1
- Update to 4.4.2
- Use RPM_OPT_FLAGS during compile

* Thu Sep 21 2006 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-5
- Add NCARG_LIB to ncarg.sh/ncarg.csh profile so ncargpath points to the right
  place (bug #207498).

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-4
- Rebuild for FC6

* Mon Feb 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-3
- Rename man3 manpages to not conflict with allegro-devel

* Wed Feb  1 2006 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-2
- Move tutorial to -devel
- Move libraries to ncarg subdir

* Fri Jul 15 2005 - Orion Poplawski <orion@cora.nwra.com> - 4.4.1-1
- Initial Fedora Extras build
