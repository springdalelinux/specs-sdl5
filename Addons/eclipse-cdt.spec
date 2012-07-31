Epoch: 1

%define gcj_support             1
%define major                   3
%define minor                   1       
%define majmin                  %{major}.%{minor}
%define micro                   2
%define eclipse_base            %{_datadir}/eclipse
%define eclipse_lib_base        %{_libdir}/eclipse

# All arches line up except i386 -> x86
%ifarch %{ix86}
%define eclipse_arch    x86
%else
%define eclipse_arch   %{_arch}
%endif

Summary:        Eclipse C/C++ Development Tools (CDT) plugin
Name:           eclipse-cdt
Version:        %{majmin}.%{micro}
Release:        6%{?dist}
License:        Eclipse Public License / CPL
Group:          Development/Tools
URL:            http://www.eclipse.org/cdt
Requires:       eclipse-platform

# The following tarball was generated like this:
#
# mkdir temp && cd temp
# mkdir home
# cvs -d:pserver:anonymous@dev.eclipse.org:/cvsroot/tools export -r CDT_3_1_2 \
#   org.eclipse.cdt-releng/org.eclipse.cdt.releng
# cd org.eclipse.cdt-releng/org.eclipse.cdt.releng/
# sed --in-place 's/@cdtTag@/CDT_3_1_2/' maps/cdt.map
# sed --in-place 's/home/cvsroot/' maps/cdt.map
# eclipse -nosplash -Duser.home=../../home \
#   -application org.eclipse.ant.core.antRunner \
#   -buildfile build.xml -DbaseLocation=/usr/share/eclipse \
#   -Dpde.build.scripts=/usr/share/eclipse/plugins/org.eclipse.pde.build/scripts \
#   -DdontUnzip=true fetch
# cd .. && tar jcf eclipse-cdt-fetched-src-3.1.2.tar.bz2 org.eclipse.cdt.releng

Source0: %{name}-fetched-src-%{version}.tar.bz2

Source1: http://sources.redhat.com/eclipse/autotools/eclipse-cdt-autotools-3_x-0.1.0.tar.gz

# The following tarball was generated thusly:
#
# mkdir temp && cd temp
# cvs -d:pserver:anonymous@dev.eclipse.org:/cvsroot/tools export -r CPPUnit_20061102 \
#   org.eclipse.cdt-cppunit/org.eclipse.cdt.cppunit \
#   org.eclipse.cdt-cppunit/org.eclipse.cdt.cppunit-feature
# cd org.eclipse.cdt-cppunit
# tar -czvf eclipse-cdt-cppunit-20061102.tar.gz org.eclipse.cdt.cppunit*

Source2: %{name}-cppunit-20061102.tar.gz

# Binary gif file that is currently missing from the CDT.  Since
# binary patches are not possible, the gif is included as a source file.

Source3: %{name}-target_filter.gif.gz

# Patch to add special "ForAllElements" targets to CDT sdk/customTargets.xml.
Patch1: %{name}-no-cvs2-patch
# Patch to remove tests from CDT build.xml.
Patch4: %{name}-no-tests.patch
# Patch to CDT to add the ability to specify a build subconsole.  The additional
# build console is # used by Autotools to display configuration output.
Patch5: %{name}-buildconsole.patch
# Patch to add new IScannerInfoPlus interface to CDT and add code to recognize it
# when opening header files via clicking on them in the outline view.  This
# stops multiple include paths from being shown when the true path is already
# known by calculation from the build's Makefile.
Patch6: %{name}-scannerinfoplus.patch
# Patch to CDT to add hover help for compiler defined symbols (i.e. -D flags).
Patch7: %{name}-definedsymbolhover.patch
# Patch to cppunit code to support double-clicking on file names, classes, and
# member names in the Hierarchy and Failure views such that the appropriate
# file will be opened and the appropriate line will be selected.
Patch8: %{name}-cppunit-ui.patch
# Patch to upgrade version number for cppunit feature.
Patch9: %{name}-cppunit-feature.patch
# Patch to fix default paths used by cppunit wizards to find header files and
# libraries.
Patch10: %{name}-cppunit-default-location.patch
# Patch to ManagedMake builder to prevent running make after Makefile generation
# failure.
Patch11: %{name}-managedbuild-failcheck.patch

BuildRequires: eclipse-pde
%if %{gcj_support}
BuildRequires:  gcc-java >= 4.0.2
BuildRequires:  java-gcj-compat-devel >= 1.0.64
Requires(post):   java-gcj-compat >= 1.0.64
Requires(postun): java-gcj-compat >= 1.0.64
%else
BuildRequires:  java-devel >= 1.4.2
%endif

Requires:       gdb make gcc-c++ autoconf automake
Requires:       eclipse-platform >= 1:3.2.0

# Currently, upstream CDT only supports building on the platforms listed here.
%if %{gcj_support}
ExclusiveArch: %{ix86} x86_64 ppc ia64
%else
ExclusiveArch: %{ix86} x86_64 ppc ia64
%endif
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%package sdk
Summary:        Eclipse C/C++ Development Tools (CDT) SDK plugin
Group:          Text Editors/Integrated Development Environments (IDE)
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description
The eclipse-cdt package contains Eclipse features and plugins that are
useful for C and C++ development.

%description sdk
Source for Eclipse CDT for use within Eclipse.

%prep
%setup -q -c 
pushd "org.eclipse.cdt.releng"
%patch1 -p0
# Only build the sdk
offset=0; 
for line in $(grep -no "value=.*platform" build.xml); do
  linenum=$(echo "$line" | cut -d : -f 1)
  sed --in-place -e "$(expr $linenum - 1 - $offset ),$(expr $linenum + 1 - $offset)d" build.xml 
  offset=$(expr $offset + 3) 
done
# Only build for the platform on which we're building
pushd sdk
sed --in-place -e "74,82d" build.properties
sed --in-place -e "s:configs=\\\:configs=linux,gtk,%{eclipse_arch}:" build.properties
popd
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch11 -p0
# Following is a patch to the CDT which is missing a b/w version
# of an icon.  This patch can be removed once fixed upstream.
pushd results/plugins/org.eclipse.cdt.make.ui/icons/dtool16
tar -xzf %{SOURCE3}
popd
popd

# Autotools stuff

mkdir autotools
pushd autotools
tar -xzf %{SOURCE1}
popd

# Cppunit stuff

mkdir cppunit
pushd cppunit
tar -xzf %{SOURCE2}
%patch8 -p0
%patch9 -p0
%patch10 -p0
popd

# Upstream CVS includes random .so files.  Let's remove them now.
# We actually remove the entire "os" directory since otherwise
# we wind up with some empty directories that we don't want.
#rm -r org.eclipse.cdt.releng/results/plugins/org.eclipse.cdt.core.linux/os

%build
export JAVA_HOME=%{java_home}
export PATH=%{java_bin}:/usr/bin:$PATH

# See comments in the script to understand this.
%if 0%{?rhel} == 5
/bin/sh -x %{_libdir}/eclipse/buildscripts/copy-platform SDK %{eclipse_base}
%else
/bin/sh -x %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base}
%endif
SDK=$(cd SDK >/dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home

homedir=$(cd home > /dev/null && pwd)

pushd org.eclipse.cdt.releng/results/plugins/org.eclipse.cdt.core.linux/library
make JAVA_HOME="%{java_home}" ARCH=%{eclipse_arch} CC='gcc -D_GNU_SOURCE'
popd

# Call eclipse headless to process CDT releng build scripts
pushd org.eclipse.cdt.releng 
java -cp $SDK/startup.jar \
    -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration                        \
    -Duser.home=$homedir                        \
     org.eclipse.core.launcher.Main             \
    -application org.eclipse.ant.core.antRunner \
    -DjavacFailOnError=true \
    -DdontUnzip=true \
    -DbaseLocation=$SDK \
    -Dpde.build.scripts=%{eclipse_base}/plugins/org.eclipse.pde.build/scripts \
    -DdontFetchAnything=true
popd

# Autotools has dependencies on CDT so we must add these to the SDK directory
tar -C $SDK --strip-components=1 -zxvf org.eclipse.cdt.releng/results/I.*/org.eclipse.cdt.sdk-*.tar.gz

# Autotools build
pushd autotools
java -cp $SDK/startup.jar \
     -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration                        \
     -Duser.home=$homedir                        \
     org.eclipse.core.launcher.Main             \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=com.redhat.eclipse.cdt.autotools.feature         \
     -DsourceDirectory=$(pwd)                          \
     -DbaseLocation=$SDK                               \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml 

popd

# Cppunit build
pushd cppunit
java -cp $SDK/startup.jar \
     -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration                        \
     -Duser.home=$homedir                        \
     org.eclipse.core.launcher.Main             \
     -application org.eclipse.ant.core.antRunner       \
     -Dtype=feature                                    \
     -Did=org.eclipse.cdt.cppunit                      \
     -DsourceDirectory=$(pwd)                          \
     -DbaseLocation=$SDK                               \
     -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
     -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml

popd
%install
rm -rf ${RPM_BUILD_ROOT}

install -d -m755 ${RPM_BUILD_ROOT}/%{eclipse_base}

tar -C ${RPM_BUILD_ROOT}/%{eclipse_base} --strip-components=1 -zxvf \
  org.eclipse.cdt.releng/results/I.*/org.eclipse.cdt.sdk-*.tar.gz

# We move arch-specific plugins to libdir.
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/eclipse
pushd ${RPM_BUILD_ROOT}
mkdir -p .%{_libdir}/eclipse/plugins
for archplugin in $(find .%{eclipse_base}/plugins -name \*%{eclipse_arch}_%{version}\*); do
  mv $archplugin .%{_libdir}/eclipse/plugins
  chmod -R 755 .%{_libdir}/eclipse/plugins/$(basename $archplugin)
done
popd

# These are in the SDK packages
rm ${RPM_BUILD_ROOT}%{eclipse_base}/epl-v10.html
rm ${RPM_BUILD_ROOT}%{eclipse_base}/notice.html

# Autotools install
pushd autotools
unzip -qq -d $RPM_BUILD_ROOT%{eclipse_base}/.. build/rpmBuild/com.redhat.eclipse.cdt.autotools.feature.zip
popd

# Cppunit install
pushd cppunit
unzip -qq -d $RPM_BUILD_ROOT%{eclipse_base}/.. build/rpmBuild/org.eclipse.cdt.cppunit.zip
popd

%if %{gcj_support}
aot-compile-rpm
%endif

%clean 
rm -rf ${RPM_BUILD_ROOT}

%if %{gcj_support}
%post
%{_bindir}/rebuild-gcj-db

%postun
%{_bindir}/rebuild-gcj-db
%endif

%files
%defattr(-,root,root)
%{eclipse_base}/features/org.eclipse.cdt_*
%{eclipse_base}/features/com.redhat.eclipse.cdt*
%{eclipse_base}/features/org.eclipse.cdt.cppunit_*
%{eclipse_base}/plugins/org.eclipse.cdt_*
%{eclipse_base}/plugins/org.eclipse.cdt.core*
%{eclipse_base}/plugins/org.eclipse.cdt.cppunit*
%{eclipse_base}/plugins/org.eclipse.cdt.debug*
%{eclipse_base}/plugins/org.eclipse.cdt.doc*
%{eclipse_base}/plugins/org.eclipse.cdt.launch*
%{eclipse_base}/plugins/org.eclipse.cdt.make*
%{eclipse_base}/plugins/org.eclipse.cdt.managedbuilder*
%{eclipse_base}/plugins/org.eclipse.cdt.refactoring*
%{eclipse_base}/plugins/org.eclipse.cdt.ui*
%{eclipse_base}/plugins/com.redhat.eclipse.cdt*
%{_libdir}/eclipse/plugins/org.eclipse.cdt.core*
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif
%doc %{eclipse_base}/features/org.eclipse.cdt.cppunit_*/cpl-v10.html
%doc %{eclipse_base}/features/org.eclipse.cdt_*/epl-v10.html

%files sdk
%defattr(-,root,root)
%{eclipse_base}/features/org.eclipse.cdt.sdk*
%{eclipse_base}/features/org.eclipse.cdt.source*
%{eclipse_base}/plugins/org.eclipse.cdt.source*
%{eclipse_base}/plugins/org.eclipse.cdt.sdk*
%{_libdir}/eclipse/plugins/org.eclipse.cdt.source*
%doc %{eclipse_base}/features/org.eclipse.cdt.sdk_*/epl-v10.html

%changelog
* Tue Jul 17 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-6
- Rebase autotools to 0.1.0
- Change automake editor to embed if/else constructs in outline view

* Wed Jul 11 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-5
- Resolves #247518, #246153, #246783, #246134, #245820
- Resolves #245611, #243184, #241782, #241612, #239620
- Resolves #238173. #239886
- Rebase autotools to 0.0.9.
- Multiple fixes to automake editor
- Multiple fixes to autoconf editor
- Autotools editor preferences added

* Fri Jun 22 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-4.1
- Fix typo in spec file.
- Add EPEL support.

* Tue May 01 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-4
- Add patch to fix backwards text entry in new configure files.
- Resolves: #238493

* Mon Apr 16 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-3
- Add missing gif to org.eclipse.cdt.make.ui.
- Resolves: #236558

* Tue Feb 27 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-2
- Resolves: #229891, #230253, #205310, #229893
- Rebase autotools to 0.0.8.1 source.

* Wed Feb 21 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.2-1
- Rebase CDT to 3.1.2.
- Rebase autotools to 0.0.8 source.
- Replace subconsole patch with new build console patch.

* Mon Jan 29 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.1-8
- Resolves: #214624, #224644
- Rebase autotools to 0.0.7 source.

* Wed Jan 17 2007 Jeff Johnston <jjohnstn@redhat.com> 3.1.1-7
- Resolves: #222350
- Rebase autotools to 0.0.6.1 source.
- Add comments.
- Put arch-specific jars in library dir.

* Mon Dec 11 2006 Jeff Johnston <jjohnstn@redhat.com> 3.1.1-6
- Rebase autotools to 0.0.6 source.

* Wed Nov 15 2006 Jeff Johnston <jjohnstn@redhat.com> 3.1.1-5
- Add cppunit support.

* Mon Nov 06 2006 Andrew Overholt <overholt@redhat.com> 3.1.1-4
- Use the new location of copy-platform.

* Thu Oct 19 2006 Ben Konrath <bkonrath@redhat.com> 3.1.1-3
- Remove work-around for gcc bug # 20198.
- Do not include notice.html and epl-v10.html because these files are already
  included in the SDK.
- Put JNI libraries in %%{_libdir}/eclipse.
- Only build the CDT SDK.
- Fix build issue on non-x86 systems.
- Resolves: #208622

* Mon Oct 16 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.1-2
- Replace build patches with sed commands
- Resolves: #208622

* Mon Oct 16 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.1-2
- Fix build so only single platform is built at a time
- Bugzilla 208622

* Thu Sep 28 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.1-1
- Rebase autotools to 0.0.5 source.
- Rebase CDT to 3.1.1 source.
- Bugzilla 206719, 206359, 206164

* Mon Sep 11 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-3
- Add hover help for defined symbols
- Fix bug with defined symbol calculation on file that compilation
  string cannot be fetched for

* Fri Sep 01 2006 Ben Konrath <bkonrath@redhat.com> 3.1.0-2
- Remove jpp in release.
- Require java-gcj-compat >= 1.0.64.

* Tue Aug 29 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_13fc
- Rebase autotools to 0.0.4 source.
- Use ScannerInfoProvider extension instead of DynamicScannerInfoProvider.
- Add sub-console support to CDT.

* Mon Aug 21 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_12fc
- Fix build special targets when project hasn't configured yet.
- Fix to fully reconfigure after configuration options change.
- Fix configuration problem whereby config.sub complains.
- Bugzilla 200000, 201270, 203440

* Tue Aug 08 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_11fc
- Fix Build Special Targets bug when importing a CVS project and
  using ManagedMake Project Wizard.
- Bugzilla 201269

* Mon Jul 31 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_10fc
- Fix bug with library hover help.

* Tue Jul 25 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_9fc
- Remove redundant runtime packages from sdk.

* Tue Jul 25 2006 Ben Konrath <bkonrath@redhat.com> 3.1.0-1jpp_8fc
- Add epoch to sdk requires.

* Mon Jul 24 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_8fc
- Update autotools sources.
- Rebuild.

* Mon Jul 24 2006 Ben Konrath <bkonrath@redhat.com> 3.1.0-1jpp_7fc
- Rebuld.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> 3.1.0-1jpp_6fc
- Rebuilt

* Thu Jul 20 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_5fc
- Split into main package and sdk sub-package.

* Thu Jul 20 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_4fc
- Add Autotools plug-ins via additional source tarball.

* Wed Jul 19 2006 Igor Foox  <ifoox@redhat.com> 3.1.0-1jpp_3fc
- Rebuild.

* Wed Jul 12 2006 Jeff Johnston  <jjohnstn@redhat.com> 3.1.0-1jpp_2fc
- Add dynamic scannerinfo extension used by Autotools plug-in.

* Mon Jul 10 2006 Andrew Overholt <overholt@redhat.com> 3.1.0-1jpp_1fc
- 3.1.0.

* Thu Jun 08 2006 Andrew Overholt <overholt@redhat.com> 3.1.0-0jpp_0fc.3.1.0RC2 
- 3.1.0 RC2.
- Remove unused hover patch.
- Use newly-created versionless pde.build symlink.
- Remove no-sdkbuild patch.

* Mon Apr 03 2006 Andrew Overholt <overholt@redhat.com> 3.0.2-1jpp_3fc
- Add ia64.

* Tue Mar 07 2006 Andrew Overholt <overholt@redhat.com> 3.0.2-1jpp_2fc
- Bump release.

* Mon Feb 13 2006 Andrew Overholt <overholt@redhat.com> 3.0.2-1jpp_1fc
- 3.0.2.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.1-1jpp_8fc
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_7fc
- Use Epoch in Requires (rh#180915).
- Require >= 3.1.2 but < 3.1.3 to ensure we get 3.1.2.

* Thu Feb 09 2006 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_6fc
- Make it Require >= 3.1.2.

* Thu Feb 09 2006 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_5fc
- Build against SDK 3.1.2.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.1-1jpp_5fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_4fc
- Rebuild against latest gcc.

* Fri Dec 30 2005 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_3fc
- Fix %%files section to not be x86-specific.

* Fri Dec 16 2005 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_2fc
- Build against gcc 4.1.

* Mon Nov 14 2005 Andrew Overholt <overholt@redhat.com> 3.0.1-1jpp_1fc
- 3.0.1.

* Fri Oct 21 2005 Andrew Overholt <overholt@redhat.com> 3.0.0_fc-2
- Rebuild against gcc 4.0.2

* Tue Aug 23 2005 Andrew Overholt <overholt@redhat.com> 3.0.0_fc-1
- Import new upstream version (3.0).

* Thu Jul 14 2005 Andrew Overholt <overholt@redhat.com> 3.0.0_fc-0.RC2.1
- Import new upstream version (3.0RC2).
- Use gbenson's new aot-compile-rpm and change requirements appropriately.
- Re-enable native compilation - let's see what happens.

* Wed Jun 22 2005 Andrew Overholt <overholt@redhat.com> 3.0.0_fc-0.M7.1
- Import new upstream version (3.0M7).
- Remove refactoring/build.properties patch (now unneeeded).

* Fri Jun 03 2005 Jeff Pound <jpound@redhat.com> 3.0.0_fc-0.M6.8
- Patch refactoring/build.properties to include plugin.properties.
- Temporarily move all *.so's to *.so.bak due to native compilation bug.
- Temporarily remove gcj .jar -> .so db population.

* Mon May 23 2005 Andrew Overholt <overholt@redhat.com> 3.0.0_fc-0.M6.7
- Bring in new I-build to enable jump to Eclipse 3.1M7 and fix some critical
  issues.

* Wed May 11 2005 Ben Konrath <bkonrath@redhat.com> 3.0.0_fc-0.M6.6
- Temporarily disable org.eclipse.cdt.managedbuilder.core_3.0.0/libmngbuildcore.jar.so.

* Wed Apr 27 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0_fc-0.M6.5
- Changed to find-and-aot-compile build usage
- Added "if gcj_support" toggle
- Fixed installing all arch fragments (now only installs one (correct) arch)
- Redid BuildRequires and Requires to remove old/unneeded dependencies
- Cleaned %%eclipse_arch declares.

* Thu Apr 21 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0_fc-0.M6.4
- Added Chris Moller's libhover patch

* Sat Apr 16 2005 Ben Konrath <bkonrath@redhat.com> 3.0.0_fc-0.M6.3
- Clean up spec file (remove references to old patches and rh docs).

* Fri Apr 15 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0_fc-0.M6.2
- Generated tarball from official final tagged M6 build

* Mon Apr 11 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0_fc-0.M6.1
- Fixed db path in java -cp
- Regenerated tarball from M6 canditate build
- Reworked patches for M6 canditate Build

* Thu Apr 07 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0_fc-0.M5.4
- Changed Requires eclipse-ui to eclipse-platform
- Added Requires java-1.4.2-gcj-compat >= 1.4.2.0-40jpp_14rh
- Added Requires gcc-java >= 4.0.0-0.35

* Mon Apr 04 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0_fc-0.M5.3
- Added eclipse-cdt-no-sdkbuild.patch to build for platform only (fc4 space crunch)

* Sun Apr 03 2005 Andrew Overholt <overholt@redhat.com> 3.0.0_fc-0.M5.2
- Make use of rebuild-gcj-db.
- Use system-wide classmap.db.

* Wed Mar 23 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.0-1
- Updated to upstream CDT 3.0.0 M5 sources
- Removed Source1 (rhdocs) for now
- Removed libhover patch until updated
- Added eclipse-cdt-platform-build-linux.patch
- Added eclipse-cdt-sdk-build-linux.patch
- Stopped tests build for now (Added eclipse-cdt-no-tests.patch)
- Added Requires gcc-java (bz# 151866)
- Added new central db logic

* Fri Mar 4 2005 Phil Muldoon <pmuldoon@redhat.com> 2.0.2-3
- Added x86_64 to ExclusiveArch

* Thu Mar 3 2005 Phil Muldoon <pmuldoon@redhat.com> 2.0.2-2
- Moved upstream sources back to 2.0.2
- Revered back to releng build
- Added native build sections to spec file

* Tue Jan 11 2005 Ben Konrath <bkonrath@redhat.com> 2.1.0-1
- add devel rpm and use the patched sources for it
- update sources to 2.1.0
- new build method that does not require pre-fetched sources

* Sun Nov 07 2004 Ben Konrath <bkonrath@redhat.com> 2.0.2-1
- Update sources to 2.0.2
- Change which files are unzipped in the install phase - this changed in 2.0.2
- Update Red Hat documentation sources
- Remove no-cvs-patch as it is no longer needed (no-cvs2-patch is still needed)
- Update ui-libhover-patch 
- Add how-to document for doc and source tarball generation
- Add fetch-tests-patch for tarball generation

* Mon Jul 26 2004 Jeremy Handcock <handcock@redhat.com> 2.0-11
- Update Red Hat documentation sources

* Fri Jul 23 2004 Tom Tromey <tromey@redhat.com> 2.0-10
- Set user.home on all java invocations

* Fri Jul 23 2004 Tom Tromey <tromey@redhat.com> 2.0-9
- Pass dontFetchAnything to the build

* Fri Jul 23 2004 Tom Tromey <tromey@redhat.com> 2.0-8
- Patch from Phil Muldoon to avoid cvs operations

* Fri Jul 23 2004 Jeremy Handcock <handcock@redhat.com> 2.0-7
- Don't build on ppc64
- Require eclipse-ui, not eclipse-platform

* Fri Jul 23 2004 Tom Tromey <tromey@redhat.com> 2.0-6
- Set user.home when building

* Wed Jul 21 2004 Tom Tromey <tromey@redhat.com> 2.0-5
- Make .so files executable

* Wed Jul 21 2004 Chris Moller <cmoller@redhat.com> 2.0-4
- Add texthover

* Tue Jul 20 2004 Jeremy Handcock <handcock@redhat.com> 2.0-4
- Update Red Hat documentation sources

* Fri Jul 16 2004 Tom Tromey <tromey@redhat.com> 2.0-3
- Make platform symlink tree before building

* Fri Jul 16 2004 Jeremy Handcock <handcock@redhat.com> 2.0-3
- Add Red Hat-specific documentation
- Use `name' macro in source and patch names
- Correct BuildRequires to eclipse-platform

* Tue Jul 13 2004 Jeremy Handcock <handcock@redhat.com> 2.0-2
- Don't require ant
- Prevent possible `build' section overload

* Mon Jul 12 2004 Tom Tromey <tromey@redhat.com> 2.0-2
- Document source fetching process
- Update to CDT 2.0 final
- Set -D_GNU_SOURCE when building

* Fri Jul  9 2004 Tom Tromey <tromey@redhat.com> 2.0-2
- Don't define prefix
- Don't require pango

* Fri Jul  9 2004 Jeremy Handcock <handcock@redhat.com> 2.0-2
- Update sources to include tests from upstream
- Add new build patch for CDT tests
- Build CDT tests, but don't install them

* Thu Jul  8 2004 Tom Tromey <tromey@redhat.com> 2.0-1
- Removed unused patch

* Thu Jul  8 2004 Jeremy Handcock <handcock@redhat.com> 2.0-1
- Revert previous patch; don't unset javacVerbose

* Thu Jul  8 2004 Jeremy Handcock <handcock@redhat.com> 2.0-1
- Unset javacVerbose

* Tue Jun 15 2004 Tom Tromey <tromey@redhat.com> 2.0-1
- Updated to 2.0 M8

* Mon Jan 19 2004 Tom Tromey <tromey@redhat.com> 1.2.1-1
- Initial version
