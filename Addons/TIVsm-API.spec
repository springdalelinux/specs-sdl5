Summary: the API
Name: TIVsm-API
Version: 5.4.0
Release: 0.1%{?dist}
License: Commercial
Group: Utilities/Archiving
Vendor: IBM
URL: http://www-3.ibm.com/software/tivoli/products/storage-mgr/
BuildArch: i386
Prefix: /opt
Source: TIVsm-API-5.4.0-0.i386.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: /bin/sh, libcrypt.so.1, libcrypt.so.1(GLIBC_2.0), libc.so.6, libc.so.6(GLIBC_2.0), libc.so.6(GLIBC_2.1), libc.so.6(GLIBC_2.1.1), libc.so.6(GLIBC_2.1.2), libc.so.6(GLIBC_2.1.3), libc.so.6(GLIBC_2.2), libc.so.6(GLIBC_2.2.3), libc.so.6(GLIBC_2.3), libct_cu.so, libct_cu.so(Base), libdl.so.2, libdl.so.2(GLIBC_2.0), libdl.so.2(GLIBC_2.1), libdmapi.so, libgcc_s.so.1, libgcc_s.so.1(GCC_3.0), libgcc_s.so.1(GLIBC_2.0), libgpfs.so, libha_gs_r.so, libha_gs_r.so(Base), libm.so.6, libm.so.6(GLIBC_2.0), libpthread.so.0, libpthread.so.0(GLIBC_2.0), libpthread.so.0(GLIBC_2.1), libpthread.so.0(GLIBC_2.2), libpthread.so.0(GLIBC_2.3.2), librt.so.1, libstdc++.so.5, libstdc++.so.5(CXXABI_1.2), libstdc++.so.5(GLIBCPP_3.2), libstdc++.so.5(GLIBCPP_3.2.2)
Requires: coreutils
Provides: libApiDS.so, libcrypto.so.0.9.7, libct_cu.so, libct_cu.so(Base), libct_cu.so(libct_cu.so), libdmapi.so, libgpfs.so, libha_gs_r.so, libha_gs_r.so(Base), libha_gs_r.so(libha_gs_r.so), libicclib.so, libicclib.so(ICCLIB), libicclib.so(libicclib.so), TIVsm-API = 5.4.0-0
AutoReqProv: 0

%description
		IBM Tivoli Storage Manager API

Originally done with rpm version 4.1.1,
built on dumas.mainz.de.ibm.com at Tue Dec  5 11:22:21 2006
from TIVsm-5.4.0-0.src.rpm with opt flags -O2 -g -march=i486 -mcpu=i686

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
popd

%clean
rm -rf $RPM_BUILD_ROOT


%post
#!/bin/bash
echo "Postinstall of the API"
#echo "Installation directory is" $RPM_INSTALL_PREFIX

if [ -z $RPM_INSTALL_PREFIX ]; then
	RPM_INSTALL_PREFIX="/opt"
fi

CLIENTDIR=$RPM_INSTALL_PREFIX/tivoli/tsm/client
BUILDDATE=`cat $CLIENTDIR/api/bin/.buildDate`
# GUID dir
GUIDDIR=$RPM_INSTALL_PREFIX/tivoli/guid

#echo "CLIENTDIR =" $CLIENTDIR
#echo "BUILDDATE =" $BUILDDATE

# change the data to the builddate
touch -t $BUILDDATE $CLIENTDIR/api/bin/dsmtca
touch -t $BUILDDATE $CLIENTDIR/api/bin/libApiDS.so

#set the s-bit
chmod 4755 $CLIENTDIR/api/bin/dsmtca

# GUID verification
if [[ -f /etc/TIVGUID ]] && [[ -f $GUIDDIR ]]; then
   cd $GUIDDIR
   ./tivguid -show
   if [ $? != 0 ]; then
      ./tivguid -create
      if [ $? != 0 ]; then
#         echo "GUID was not found. A new one could not be generated."
         exit 1
      fi
   fi
else
   if [ -f $GUIDDIR ]; then
      cd $GUIDDIR
      ./tivguid -create
      if [ $? != 0 ]; then
#      echo "GUID was not found. A new one could not be generated."
         exit 1
      fi
   fi
fi

for f in libgpfs.so libdmapi.so libha_gs_r.so libct_cu.so
do
	if [ -f /usr/lib/$f ]
	then
	   if [[ $DEBUG_INSTALL == "1" ]]; then echo "File /usr/lib/$f found...";fi
	else 
	   if [[ $DEBUG_INSTALL == "1" ]]; then echo "File /usr/lib/$f not found... copy it!";fi
	   cp $CLIENTDIR/api/bin/$f /usr/lib
	fi
done

#for f in libsrc.so libsrcdb.so
#do
#	if [ -f /lib/$f ]
#	then
#	   if [[ $DEBUG_INSTALL == "1" ]]; then echo "File /lib/$f found...";fi
#	else 
#	   if [[ $DEBUG_INSTALL == "1" ]]; then echo "File /lib/$f not found... copy it!";fi
#	   cp $CLIENTDIR/api/bin/$f /lib
#	fi
#done

# remove buildDate
rm -f $CLIENTDIR/api/bin/.buildDate
rm -f $CLIENTDIR/lang/.buildDate

# create links for en_US-messages
ln -s ../../lang/en_US $CLIENTDIR/api/bin/en_US

echo
echo "TSM Linux API installation complete."
echo
echo "Be sure to set up the configuration files!"
echo


%preun
if [ -d /usr/lpp/mmfs ]
then
  if [[ $DEBUG_INSTALL == "1" ]]; then echo "GPFS-Packages are installed... deleting nothing!";fi
else 
  if [[ $DEBUG_INSTALL == "1" ]]; then echo "Deleting /usr/lib/libgpfs.so and /usr/lib/libdmapi.so !!!";fi
  rm /usr/lib/libgpfs.so
  rm /usr/lib/libdmapi.so
fi

if [ -d /usr/sbin/rsct ]
then
  if [[ $DEBUG_INSTALL == "1" ]]; then echo "RSCT-Pakages are installed... deleting nothing!";fi
else 
  if [[ $DEBUG_INSTALL == "1" ]]; then echo "Deleting /usr/lib/libha_gs_r.so and /usr/lib/libct_cu.so !!!";fi
  rm /usr/lib/libha_gs_r.so
  rm /usr/lib/libct_cu.so
fi

#if [ -d /usr/bin/lssrc ]
#then
#  if [[ $DEBUG_INSTALL == "1" ]]; then echo "SRC-Pakages are installed... deleting nothing!";fi
#else
#  if [[ $DEBUG_INSTALL == "1" ]]; then echo "Deleting /lib/libsrc.so and /lib/libsrcdb.so !!!";fi
#  rm /lib/libsrc.so
#  rm /lib/libsrcdb.so
#fi

# recover '.buildDate' to satisfy rpm
touch /opt/tivoli/tsm/client/api/bin/.buildDate
touch /opt/tivoli/tsm/client/lang/.buildDate

# remove links for messages
rm -f /opt/tivoli/tsm/client/api/bin/??_??


%files
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/api
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/NOTICES.TXT
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/README_api_enu.htm
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/README_enu.htm
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/api/bin
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/.buildDate
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/dsm.opt.smp
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/dsm.sys.smp
%attr(04755,root,bin) /opt/tivoli/tsm/client/api/bin/dsmtca
%attr(0555,root,bin) /opt/tivoli/tsm/client/api/bin/libApiDS.so
%attr(0755,root,bin) /opt/tivoli/tsm/client/api/bin/libct_cu.so
%attr(0755,root,bin) /opt/tivoli/tsm/client/api/bin/libdmapi.so
%attr(0755,root,bin) /opt/tivoli/tsm/client/api/bin/libgpfs.so
%attr(0755,root,bin) /opt/tivoli/tsm/client/api/bin/libha_gs_r.so
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/api/bin/sample
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/callbuff.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/callevnt.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/callhold.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/callmt1.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/callmt2.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/callret.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapibkup.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapidata.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapiinit.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapint64.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapint64.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapipref.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapiproc.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapiproc.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapipw.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapiqry.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapirc.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapismp.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapitype.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapiutil.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dapiutil.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dpsthread.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dpsthread.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dsmapifp.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dsmapips.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dsmapipw.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dsmapitd.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dsmgrp.c
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/dsmrc.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/makesmp.linux86
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/release.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/tsmapifp.h
%attr(0444,root,bin) /opt/tivoli/tsm/client/api/bin/sample/tsmapitd.h
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/icc32
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/icc32/icc
%attr(0444,root,bin) /opt/tivoli/tsm/client/icc32/icc/ReadMe.txt
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/icc32/icc/icclib
%attr(0555,root,bin) /opt/tivoli/tsm/client/icc32/icc/icclib/libicclib.so
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/icc32/icc/osslib
%attr(0555,root,bin) /opt/tivoli/tsm/client/icc32/icc/osslib/libcrypto.so.0.9.7
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/lang
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/.buildDate
%dir %attr(0755,root,bin) /opt/tivoli/tsm/client/lang/en_US
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/dscjres.txt
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/dsmc.hlp
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/dsmclientV3.cat
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/dsmig.hlp
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/hsmhelp.jar
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/tsmhelp.jar
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/uil_nls.jar
%attr(0444,root,bin) /opt/tivoli/tsm/client/lang/en_US/wchelp.htl
%attr(-,root,bin) /usr/lib/libApiDS.so

%changelog
* Mon Apr 30 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt it to include the dependency on coreutils so that
  post install scripts do not fail during installation
