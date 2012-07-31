%define destdir /opt/pgi
%define modulesdestination /opt/share/Modules/modulefiles

# The name of the modules RPM
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}

%ifarch %{ix86}
%define pgibits 32
%define liblf liblf
%else
%define pgibits 64
%define liblf libso
%endif

Summary: PGI Workstation Compilers
Name: pgi-workstation90
Version: 9.0
%define shortversion 9
%define minorrelease 4
%define numversion 0%( echo %{version} | tr -d . )
Release: %{minorrelease}.5%{?dist}
Group: Development/Language
%define fileversion %( echo %{version}%{minorrelease} | tr -d . )
%ifarch %{ix86}
%define fulldir %{destdir}/linux86/%{version}-%{minorrelease}
%define fulldirv %{destdir}/linux86/%{version}
%endif
%ifarch x86_64
%define fulldir %{destdir}/linux86-64/%{version}-%{minorrelease}
%define fulldirv %{destdir}/linux86-64/%{version}
%endif
Source0: pgilinux-%{fileversion}.tar.gz
Source1: pthread.h
License: Commercial
URL: http://www.pgroup.com/
BuildRoot: %{_tmppath}/%{name}-root
# do not do anything to files, no stripping or debuginfo
%define __os_install_post %{nil}
%define debug_package %{nil}
AutoReqProv: 0
BuildRequires: numactl gcc perl symlinks
%if 0%{?rhel} && "%rhel" > "4"
BuildRequires: numactl-devel gcc-gfortran
Requires: numactl-devel gcc-gfortran
%endif
Requires: numactl gcc
Requires: %{name}-libs = %{version}-%{release}
Requires: pgi-license
Provides: pgi-workstation = %{version}-%{release}
Provides: pgi-workstation = %{version}-%{minorrelease}
Provides: %{name} = %{version}-%{minorrelease}

%description
PGI compilers and tools.

%package doc
Summary: PGI Workstation Compiler documentation
Group: Development/Language
AutoReqProv: 0
Requires: %{name} = %{version}-%{release}
Provides: %{name}-doc = %{version}-%{minorrelease}

%description doc
Documentation for PGI compilers and tools.

%package libs
Summary: PGI Workstation Compiler libraries
Group: Development/Language
#Provides: libpgbind.so libpgc.so libpgnuma.so
Requires: %{modules_rpm_name}
AutoReqProv: 0
Provides: pgi-workstation-libs = %{version}-%{release}
Provides: pgi-workstation-libs = %{version}-%{minorrelease}
Provides: %{name}-libs = %{version}-%{minorrelease}
%ifarch %{ix86}
Provides: gdix86.so libpgbind.so libpgc.so
%endif
%ifarch x86_64
Provides: gdix86-64.so()(64bit) libC.so()(64bit) libpgbind.so()(64bit) libpgc.so()(64bit)
Provides: libpgf90.so()(64bit) libpgf902.so()(64bit) libpgf90_prof.so()(64bit) libpgf90_rpm1.so()(64bit)
Provides: libpgf90_rpm1_p.so()(64bit) libpgf90rtl.so()(64bit) libpgftnrtl.so()(64bit) libpghpf.so()(64bit)
Provides: libpghpf2.so()(64bit) libpghpf_mpi.so()(64bit) libpghpf_mpi_p.so()(64bit) libpgmp.so()(64bit)
Provides: libpghpf_prof.so()(64bit) libpghpf_rpm.so()(64bit) libpghpf_rpm1.so()(64bit) libpghpf_rpm1_p.so()(64bit)
Provides: libpghpf_rpm_p.so()(64bit) libpghpf_smp.so()(64bit) libpghpf_smp_p.so()(64bit) libpgnod_prof.so()(64bit)
Provides: libpgnod_prof_g.so()(64bit) libpgnod_prof_papi.so()(64bit) libpgnod_prof_pfo.so()(64bit) 
Provides: libpgnod_prof_time.so()(64bit) libstd.so()(64bit)  
%endif

%description libs
Various shared libraries for PGI compilers.

%package acml
Summary: PGI Workstation Compiler ACML libraries
Group: Development/Language
Provides: libacml.a libacml_mp.a acml.h
%ifarch x86_64
Provides: libacml.so libacml_mv.so libacml_mp.so libacml_mv.a acml_mv.h acml_mv_m128.h
%endif
Requires: %{name}-libs = %{version}-%{release}
Provides: pgi-workstation-acml = %{version}-%{release}
Provides: pgi-workstation-acml = %{version}-%{minorrelease}
Provides: %{name}-acml = %{version}-%{minorrelease}
AutoReqProv: 0

%description acml
PGI Workstation Compiler ACML libraries

%prep
%setup -q -c -n %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT%{destdir}
mkdir -p $RPM_BUILD_ROOT%{destdir}
release=%{version}
build=%{minorrelease}
prerelease=0
%ifarch %{ix86}
	target=linux86
%endif
%ifarch x86_64
	target=linux86-64
%endif
SRC=`pwd`
COMMON="$SRC/.parts/common"
PART=`cat $SRC/.parts/$target`
INSTALL_DIR=$RPM_BUILD_ROOT%{destdir}

echo "Installing software into $INSTALL_DIR (this may take some time)."
cd $SRC
for i in $PART ; do
  tar cf - $i | ( cd $INSTALL_DIR; tar xf - )
  echo -n \#
done
# Install common components.
cd $SRC/common
if test -d $INSTALL_DIR/linux86 ; then
  for i in `cat $COMMON` ; do
    x=`basename $i`
    tar cf - $x | ( cd $INSTALL_DIR/linux86/$release-$build; tar xf - )
    echo -n \#
  done
fi
if test -d $INSTALL_DIR/linux86-64 ; then
  for i in `cat $COMMON` ; do
    x=`basename $i`
    tar cf - $x | ( cd $INSTALL_DIR/linux86-64/$release-$build; tar xf - )
    echo -n \#
  done
fi
echo 

# Make files writeable so script can make changes.

chmod -Rf u+w $INSTALL_DIR

# Install JAVA JRE from Sun.

JRE=$SRC/common/java_jre.tar.gz
if test -f $JRE; then 
  if test -d $INSTALL_DIR/linux86/$release-$build ; then
    (cd $INSTALL_DIR/linux86/$release-$build; gzip -c -d $JRE | tar xpf - )
  fi
  if test -d $INSTALL_DIR/linux86-64/$release-$build ; then
    (cd $INSTALL_DIR/linux86-64/$release-$build; gzip -c -d $JRE | tar xpf - )
  fi
fi

# Create $PGI/index.htm

if test -f $SRC/common/index.htm ; then
  if test -d $INSTALL_DIR/linux86/$release-$build ; then
    cp $SRC/common/index.htm $INSTALL_DIR/linux86/$release-$build/index.htm
  fi 
  if test -d $INSTALL_DIR/linux86-64/$release-$build ; then
    cp $SRC/common/index.htm $INSTALL_DIR/linux86-64/$release-$build/index.htm
  fi
    
fi


# Install distribution-dependent patches before makelocalrc runs.

PATCH=$SRC/$target/$release-$build/patches
if test -d "$SRC" ; then
  : # None currently.
fi

  if test -x $INSTALL_DIR/linux86/$release-$build/bin/makelocalrc ; then
    $INSTALL_DIR/linux86/$release-$build/bin/makelocalrc -x $INSTALL_DIR/linux86/$release-$build
  fi
  if test -x $INSTALL_DIR/linux86-64/$release-$build/bin/makelocalrc ; then
    $INSTALL_DIR/linux86-64/$release-$build/bin/makelocalrc -x $INSTALL_DIR/linux86-64/$release-$build
  fi

# Create REDIST and PORTABLE directories.

if test -x $SRC/postinstall ; then
  $SRC/postinstall $INSTALL_DIR 0
fi

# Support and ACML license files.

cp $SRC/INSTALL.txt $SRC/common/SUBSCRIPTION_SERVICE $INSTALL_DIR

# Make symlink to $INSTALL_DIR/linux86*/$release-$build

echo 
if test -d $INSTALL_DIR/linux86/$release-$build; then
  nosymlink=0
  echo "Making symbolic links in $INSTALL_DIR/linux86/$release" 
   mkdir -p $INSTALL_DIR/linux86/$release
   for i in `ls $INSTALL_DIR/linux86/$release-$build`; do
     if test -e "$INSTALL_DIR/linux86/$release/$i"; then
     if test ! -h "$INSTALL_DIR/linux86/$release/$i"; then
       nosymlink=1
       echo "$INSTALL_DIR/linux86/$release/$i is not a symbolic link."
       echo "No symbilic link is done."
       echo 
       break;
     fi
     fi
   done
   if test $nosymlink -eq 0; then
     for i in `ls $INSTALL_DIR/linux86/$release-$build`; do
       rm -f $INSTALL_DIR/linux86/$release/$i
       ln -s $INSTALL_DIR/linux86/$release-$build/$i $INSTALL_DIR/linux86/$release/$i
     done
    fi

fi

if test -d $INSTALL_DIR/linux86-64/$release-$build; then
  nosymlink=0
  echo "Making symbolic links in $INSTALL_DIR/linux86-64/$release" 
  mkdir -p $INSTALL_DIR/linux86-64/$release
  for i in `ls $INSTALL_DIR/linux86-64/$release-$build`; do
    if test -e "$INSTALL_DIR/linux86-64/$release/$i"; then
    if test ! -h "$INSTALL_DIR/linux86-64/$release/$i"; then
      nosymlink=1
      echo "$INSTALL_DIR/linux86-64/$release/$i is not a symbolic link."
      echo "No symbolic link is done."
      echo 
      break;
    fi
    fi
  done
  if test $nosymlink -eq 0; then
    for i in `ls $INSTALL_DIR/linux86-64/$release-$build`; do
      rm -f $INSTALL_DIR/linux86-64/$release/$i
      ln -s $INSTALL_DIR/linux86-64/$release-$build/$i $INSTALL_DIR/linux86-64/$release/$i
    done
  fi
fi
echo

# now fixup references to $RPM_BUILD_ROOT
perl -pi -e "s,$RPM_BUILD_ROOT,,g" `find $INSTALL_DIR -name localrc`

# remove .svn dirs
rm -rf `find $INSTALL_DIR -name .svn`

# compress by hand our man pages
find $RPM_BUILD_ROOT%{fulldir}/man/ -type f -exec gzip -9 {} \;

# some symlinks point to under $RPM_BUILD_ROOT, fix them
for i in `find $INSTALL_DIR -type l`; do
	j=`readlink $i | perl -pi -e "s|$RPM_BUILD_ROOT||"`
	rm -f $i
	ln -sf $j $i
done

# lots of duplicates for the following libs so make sure they are all hard linked
for i in `find $RPM_BUILD_ROOT%{fulldir} -type f -name libpgc.so -o -name libpgc.a`; do
	iinode=`stat -c '%i' $i`
	f=`basename $i`
        for j in `find $RPM_BUILD_ROOT%{fulldir} -type f -name $f`; do
           if [ -e "$j" ]; then
                jinode=`stat -c '%i' $j`
                if [ $iinode -ne $jinode ]; then
                        if cmp $i $j >/dev/null; then
                                echo $i $j are the same
                                rm -f $j
                                ln $i $j
                        fi
                fi
           fi
        done
done

# make links relative or else rpm freaks out
#symlinks -c $RPM_BUILD_ROOT%{fulldirv}

mv $RPM_BUILD_ROOT%{destdir}/INSTALL* $RPM_BUILD_ROOT%{destdir}/S* $RPM_BUILD_ROOT%{fulldir}

# Modules stuff
PGIUNLOAD="intel/"
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{version}
cat > $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{version}/%{pgibits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{compiler} %{intelversion} %{inteltype} %{pgibits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using PGI Workstation compilers %{version} %{pgibits} bits"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

# We check to see if any incompatible intel compilers are loaded
if {[module-info mode load] && ![module-info mode remove]} {
  if {[info exists env(LOADEDMODULES)]} {
    set envloaded [split \$env(LOADEDMODULES) ":"]
    foreach mod [lsort -decreasing \$envloaded] {
      set mmod "\$mod/"
      # only consider intel modules
      if {[string first "intel/" \$mmod] == 0 && [string first "pgi/%{version}/%{pgibits}" \$mmod] != 0 } {
        puts stderr "Conflicting PGI module \$mod - removing before inserting requested module pgi/%{version}/%{pgibits}"
        module unload \$mod
      }
    }
    foreach conflicts [ split "$PGIUNLOAD" " " ] {
      set envloaded [split \$env(LOADEDMODULES) ":"]
      foreach mod [lsort -decreasing \$envloaded] {
        set mmod "\$mod/"
        if {[string first \$conflicts \$mmod] == 0} {
          puts stderr "Conflicting module \$mmod - removing before inserting requested module pgi/%{version}/%{pgibits}"
          module unload \$mod
          }
      }
    }
  }
}

module-whatis   "Loads settings for the PGI Workstation compilers %{version} %{pgibits} bits"
prepend-path    PATH            %{fulldirv}/bin
prepend-path    MANPATH         %{fulldirv}/man
prepend-path    LD_LIBRARY_PATH %{fulldirv}/lib:%{fulldirv}/%{liblf}
set     version      "3.2.3"
ENDDEFAULT

cat > $RPM_BUILD_ROOT%{modulesdestination}/pgi/.modulerc-pgi-%{numversion}-%{pgibits} <<ENDGENERIC
#%Module
module-alias pgi/%{shortversion} pgi/%{version}
ENDGENERIC
mkdir $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{shortversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/pgi/%{shortversion}/.modulerc-pgi-%{numversion}-%{pgibits} <<ENDMOREGENERIC
#%Module
module-alias pgi/%{shortversion}/%{pgibits} pgi/%{version}/%{pgibits}
ENDMOREGENERIC

# finally install the pthread.h workaround in the includedir
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{fulldir}/include/

# make sure files can be read
chmod -R a+rX,og-w,u+w $INSTALL_DIR

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc %{fulldir}/*LICENSE*
%doc %{fulldir}/man/*
%{fulldir}/bin/*
%{fulldir}/bin/.p*
%{fulldir}/etc
%{fulldir}/include 
%{fulldir}/jre
%{fulldir}/lib*/*
%{fulldir}/src
# the following are packaged in other subrpms
%exclude %{fulldir}/lib*/*.so
%exclude %{fulldir}/include/acml*
%exclude %{fulldir}/lib/libacml*
%ifarch x86_64
%exclude %{fulldir}/libso/libacml*
%{fulldir}/cray
%endif
# more complicated stuff
%{fulldirv}/*
%exclude %{fulldirv}/bin
%exclude %{fulldirv}/man
%exclude %{fulldirv}/lib*
%exclude %{fulldirv}/doc
%exclude %{fulldirv}/EXAMPLES
%exclude %{fulldirv}/index.htm
%exclude %{fulldirv}/REDIST
%ifarch %{ix86}
%exclude %{fulldirv}/PORTABLE
%endif

%files libs
%defattr(-,root,root)
%dir %{destdir}
%dir %{destdir}/linux*
%dir %{fulldirv}
%dir %{fulldir}
%ifarch %{ix86}
%{fulldir}/PORTABLE
%endif
%{fulldir}/REDIST
%dir %{fulldir}/lib*
%{fulldir}/lib*/*.so
%dir %{fulldir}/bin
%dir %{fulldir}/man
%dir %{modulesdestination}/pgi
%dir %{modulesdestination}/pgi/%{version}
%{modulesdestination}/pgi/%{version}/%{pgibits}
%dir %{modulesdestination}/pgi/%{shortversion}
%{modulesdestination}/pgi/.modulerc-pgi-%{numversion}-%{pgibits}
%{modulesdestination}/pgi/%{shortversion}/.modulerc-pgi-%{numversion}-%{pgibits}
%{fulldirv}/bin
%{fulldirv}/man
%{fulldirv}/lib*
%ifarch %{ix86}
%{fulldirv}/PORTABLE
%endif
%{fulldirv}/REDIST
%exclude %{fulldir}/lib*/libacml*

%files doc
%defattr(-,root,root)
%doc %{fulldir}/doc
%doc %{fulldir}/index.htm
%doc %{fulldir}/EXAMPLES
%doc %{fulldir}/INSTALL.txt 
%doc %{fulldir}/SUBSCRIPTION_SERVICE
%{fulldirv}/doc
%{fulldirv}/EXAMPLES
%{fulldirv}/index.htm

%files acml
%defattr(-,root,root)
%{fulldir}/include/acml*
%{fulldir}/lib/libacml*
%ifarch x86_64
%{fulldir}/libso/libacml*
%endif

%changelog
* Tue Jul 07 2005 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
