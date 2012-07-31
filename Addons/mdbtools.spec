%define prever pre1

Name:           mdbtools
Version:        0.6
Release:        0.3.cvs20051109%{?dist}
Summary:        Access data stored in Microsoft Access databases
Group:          Applications/Databases
License:        GPLv2+
URL:            http://mdbtools.sourceforge.net/
Source0         http://downloads.sourceforge.net/%{name}/%{name}-%{version}%{prever}.tar.gz
Source1:        gmdb2.desktop
Patch0:         mdbtools-0.6pre1-cvs20051109.patch.gz
Patch1:         ftp://ftp.nluug.nl/pub/os/Linux/distr/debian/pool/main/m/mdbtools/mdbtools_0.5.99.0.6pre1.0.20051109-4.diff.gz
Patch2:         mdbtools-0.6-crashes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  unixODBC-devel libgnomeui-devel readline-devel
BuildRequires:  bison flex desktop-file-utils
Requires:       %{name}-libs = %{version}-%{release}

%description
MDB Tools is a suite of programs for accessing data stored in Microsoft
Access databases.


%package libs
Summary:        Library for accessing data stored in Microsoft Access databases
Group:          System Environment/Libraries
License:        LGPLv2+

%description libs
This package contains the MDB Tools library, which can be used by applications
to access data stored in Microsoft Access databases.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
License:        LGPLv2+
Requires:       %{name}-libs = %{version}-%{release}, glib2-devel, pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package gui
Summary:        Graphical interface for MDB Tools
Group:          Applications/Databases
License:        GPLv2+ 
Requires:       %{name}-libs = %{version}-%{release}

%description gui
The mdbtools-gui package contains the gmdb2 graphical user interface
for MDB Tools


%prep
%setup -q -n %{name}-%{version}%{prever}
%patch0 -p1
%patch1 -p1
pushd debian/patches
for i in *; do
  echo $i
  case "$i" in
    015-allsyms.patch|038-removals.patch|045-aboutdialog.patch|056-libmdb-data.patch)
      patch -d ../.. -p0 < $i
      ;;
    *)
      patch -d ../.. -p1 < $i
  esac
done
popd
%patch2 -p1 -z .crash
chmod -x COPYING.LIB


%build
%configure --disable-static --enable-sql --with-unixodbc="%{_prefix}"
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
rm $RPM_BUILD_ROOT%{_libdir}/libmdb*.la
# remove some headers which should not be installed / exported
rm $RPM_BUILD_ROOT%{_includedir}/{connectparams.h,gmdb.h,mdbodbc.h}
rm $RPM_BUILD_ROOT%{_includedir}/{mdbprivate.h,mdbver.h}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/mdb-*
%{_mandir}/man1/mdb-*.1.gz

%files libs
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.LIB NEWS README TODO doc/faq.html
%{_libdir}/libmdb*.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_libdir}/libmdb*.so
%{_libdir}/pkgconfig/libmdb*.pc
%{_includedir}/mdb*.h

%files gui
%defattr(-,root,root,-)
%{_bindir}/gmdb2
%{_datadir}/gmdb
%{_datadir}/gnome/help/gmdb
%{_datadir}/applications/fedora-gmdb2.desktop


%changelog
* Tue Aug 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6-0.3.cvs20051109
- Stop gmdb from crashing when selecting close without a file being open
  (bz 251419)
- Change release field from 0.x.pre1 to 0.x.cvs20051109, as that more acurately
  reflects our upstream base (bz 251419)

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6-0.2.pre1
- Stop gmdb from crashing when selecting file->properties without having a file
  loaded (bz 251419)
- Don't install headers used to build tools (install only those of libmdb)
- Add glib2-devel to the -devel Requires

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6-0.1.pre1
- There were lots of compile warnings, looking for a fix I found that upstream
  is dead, but that Debian has sort of continued as upstream based on the
  0.6pre1 release; Switching to Debian "upstream" release 0.6pre1 (20051109-4)

* Wed Aug  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5-1
- Initial Fedora package (based on specfile by Dag Wieers, thanks!)
