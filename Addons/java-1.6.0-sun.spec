%define section         non-free

%define origin          sun
%define priority        1600
%define javaver         1.6.0
%define cvsver          6
%define buildver        31

%define name            java-%{javaver}-%{origin}
%define release         0.0.4%{?dist}

# TODO: Think about using conditionals for version variants.

%define version         %{javaver}.%{buildver}
#define version         %{javaver}

%define cvsversion	%{cvsver}u%{buildver}
#define cvsversion	%{cvsver}

%define javaws_ver      %{javaver}
%define javaws_version  %{cvsversion}

%define toplevel_dir    jdk%{javaver}_%{buildver}
#define toplevel_dir    jdk%{javaver}

%define sdklnk          java-%{javaver}-%{origin}
%define jrelnk          jre-%{javaver}-%{origin}
%define sdkdir          %{name}-%{version}
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define sdklibdir       %{_jvmdir}/%{sdklnk}/lib
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}

%define x11bindir       %{_bindir}
%define x11encdir       %{_datadir}/X11/fonts/encodings
%define fontconfigdir   %{_sysconfdir}/fonts
%define fontdir         %{_datadir}/fonts/java
%define xsldir          %{_datadir}/xml/%{name}-%{version}

%ifarch %ix86
%define target_cpu      i586
%define pluginname      %{_jvmdir}/%{jredir}/lib/i386/libnpjp2.so
%endif

%ifarch x86_64
%define pluginname      %{_jvmdir}/%{jredir}/lib/amd64/libnpjp2.so
%endif

%define cgibindir       %{_var}/www/cgi-bin

# Avoid RPM 4.2+'s internal dep generator, it may produce bogus
# Provides/Requires here.
%define _use_internal_dependency_generator 0

# This prevents aggressive stripping.
%define debug_package %{nil}

Name:           %{name}
Version:        %{version}
Release:        %{release}
Epoch:          0
Summary:        Java Runtime Environment for %{name}
License:        Sun Binary Code License
Group:          Development/Interpreters
Vendor:         JPackage Project
Distribution:   JPackage
URL:            http://java.sun.com/j2se/%{javaver}/
Source0:        jdk-%{cvsversion}-linux-i586.bin
Source10:       jdk-%{cvsversion}-linux-x64.bin
Source1:        %{name}-register-java-fonts.xsl
Source2:        %{name}-unregister-java-fonts.xsl
Provides:       jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{javaver}
Provides:       java-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java = %{epoch}:%{javaver}
Requires:       /usr/sbin/update-alternatives
Requires:       jpackage-utils >= 0:1.5.38
Requires(post):	coreutils, perl
Conflicts:      kaffe
BuildArch:      i586 x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  jpackage-utils >= 0:1.5.38, sed, %{_bindir}/perl
Provides:       javaws = %{epoch}:%{javaws_ver}
Provides:       jndi = %{epoch}:%{version}, jndi-ldap = %{epoch}:%{version}
Provides:       jndi-cos = %{epoch}:%{version}, jndi-rmi = %{epoch}:%{version}
Provides:       jndi-dns = %{epoch}:%{version}
Provides:       jaas = %{epoch}:%{version}
Provides:       jsse = %{epoch}:%{version}
Provides:       jce = %{epoch}:%{version}
Provides:       jdbc-stdext = %{epoch}:3.0, jdbc-stdext = %{epoch}:%{version}
Provides:       java-sasl = %{epoch}:%{version}
Obsoletes:      javaws-menu
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
This package contains the Java Runtime Environment for %{name}

%package        devel
Summary:        Java Development Kit for %{name}
Group:          Development/Compilers
Requires:       /usr/sbin/update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{javaver}, java-sdk = %{epoch}:%{javaver}
Provides:       java-devel-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-%{javaver}-devel, java-devel = %{epoch}:%{javaver}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
The Java(tm) Development Kit (JDK(tm)) contains the software and tools that
developers need to compile, debug, and run applets and applications
written using the Java programming language.

%package        src
Summary:        Source files for %{name}
Group:          Development/Interpreters
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    src
This package contains source files for %{name}.

%package        demo
Summary:        Demonstration files for %{name}
Group:          Development/Interpreters
Requires:       %{name} = %{epoch}:%{version}-%{release}
# Without this a requirement on libjava_crw_demo_g.so is added which
# is not in the main java package. libjava_crw_demo.so is but not "_g".
AutoReq:        0

%description    demo
This package contains demonstration files for %{name}.

%package        plugin
Summary:        Browser plugin files for %{name}
Group:          Internet/WWW/Browsers
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{_bindir}/find, sed
Provides:       java-plugin = %{epoch}:%{javaver}, java-%{javaver}-plugin = %{epoch}:%{version}
Conflicts:      java-%{javaver}-ibm-plugin, java-%{javaver}-blackdown-plugin
Conflicts:      java-%{javaver}-bea-plugin
Obsoletes:      java-1.3.1-plugin, java-1.4.0-plugin, java-1.4.1-plugin, java-1.4.2-plugin

%description    plugin
This package contains browser plugin files for %{name}.
Note!  This package supports browsers built with GCC 3.2 and later.

%package        fonts
Summary:        TrueType fonts for %{origin} JVMs
Group:          Text Processing/Fonts
Requires:       %{name} = %{epoch}:%{version}-%{release}, %{_bindir}/ttmkfdir
Requires:       %{_sbindir}/chkfontpath, %{x11bindir}/mkfontdir, mktemp
Requires:       %{_bindir}/xsltproc, %{_bindir}/perl
Provides:       java-fonts = %{epoch}:%{javaver}, java-%{javaver}-fonts
Conflicts:      java-%{javaver}-ibm-fonts, java-%{javaver}-blackdown-fonts
Conflicts:      java-%{javaver}-bea-fonts
Obsoletes:      java-1.3.1-fonts, java-1.4.0-fonts, java-1.4.1-fonts, java-1.4.2-fonts
Requires:	fontconfig, coreutils

%description    fonts
This package contains the TrueType fonts for %{origin} JVMs.

%package        alsa
Summary:        ALSA support for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    alsa
This package contains Advanced Linux Sound Architecture (ALSA) support
libraries for %{name}.

%package        jdbc
Summary:        JDBC/ODBC bridge driver for %{name}
Group:          Development/Libraries/Java
AutoReq:        0
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{_libdir}/libodbc.so, %{_libdir}/libodbcinst.so

%description    jdbc
This package contains the JDBC/ODBC bridge driver for %{name}.


%prep
rm -rf $RPM_BUILD_DIR/%{toplevel_dir}
export MORE=10000
%ifnarch x86_64
OURSOURCE=%{SOURCE0}
%else
OURSOURCE=%{SOURCE10}
%endif
sh $OURSOURCE <<EOF >/dev/null
yes
EOF
%setup -T -D -n %{toplevel_dir}
chmod -R go=u-w *
chmod -R u+w *

# make sure the plugin exists
_OJI_PLUGIN=$(echo %pluginname | sed 's|%{_jvmdir}/%{jredir}|jre|')
if [ ! -f $_OJI_PLUGIN ]; then
  exit 1
fi

# Avoid bogus ODBC dependencies
%global reqfilt /bin/sh -c "%{__find_requires} | %{__grep} -Evx 'libodbc(inst)?\\.so([(][)][(]64bit[)])?'"
%global __find_requires %{reqfilt}
%build
# Nope.


%install
rm -rf $RPM_BUILD_ROOT

# fix up ControlPanel APPHOME and bin locations
perl -p -i -e 's|APPHOME=.*|APPHOME=%{_jvmdir}/%{jredir}|' jre/bin/ControlPanel
perl -p -i -e 's|/usr/bin/||g' jre/bin/ControlPanel

# fix up (create new) HtmlConverter
cat > bin/HtmlConverter << EOF
%{jrebindir}/java -jar %{sdklibdir}/htmlconverter.jar $*
EOF

%ifnarch x86_64
# fix up java-rmi.cgi PATH
perl -p -i -e 's|PATH=.*|PATH=%{jrebindir}|' bin/java-rmi.cgi

# install java-rmi-cgi
install -D -m 755 bin/java-rmi.cgi $RPM_BUILD_ROOT%{cgibindir}/java-rmi-%{version}.cgi
%endif

# main files
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

# extensions handling
install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
pushd $RPM_BUILD_ROOT%{jvmjardir}
   ln -s %{_jvmdir}/%{jredir}/lib/jsse.jar jsse-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/jce.jar jce-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-ldap-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-cos-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jndi-rmi-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jaas-%{version}.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar jdbc-stdext-%{version}.jar
   ln -s jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
   ln -s %{_jvmdir}/%{jredir}/lib/rt.jar sasl-%{version}.jar
   for jar in *-%{version}.jar ; do
      if [ x%{version} != x%{javaver} ]; then
         ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

# rest of the jre
cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
cp -a jre/javaws jre/plugin $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/endorsed

# jce policy file handling
install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{name}/jce/vanilla
for file in local_policy.jar US_export_policy.jar; do
  mv $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file \
    $RPM_BUILD_ROOT%{_jvmprivdir}/%{name}/jce/vanilla
  # for ghosts
  touch $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file
done

# versionless symlinks
pushd $RPM_BUILD_ROOT%{_jvmdir}
ln -s %{jredir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

pushd $RPM_BUILD_ROOT%{_jvmjardir}
ln -s %{sdkdir} %{jrelnk}
ln -s %{sdkdir} %{sdklnk}
popd

# ControlPanel freedesktop.org menu entry
perl -p -i -e 's|INSTALL_DIR/JRE_NAME_VERSION|%{_jvmdir}/%{jredir}|g' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Name=.*|Name=Java Plugin Control Panel \(%{name}\)|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Icon=.*|Icon=%{name}.png|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Terminal=0|Terminal=false|' jre/plugin/desktop/sun_java.desktop
perl -p -i -e 's|Categories=Application|Categories=System|' jre/plugin/desktop/sun_java.desktop

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
install -m 644 jre/plugin/desktop/sun_java.desktop  $RPM_BUILD_ROOT%{_datadir}/applications/jpackage-%{name}-control-panel.desktop
install -m 644 jre/plugin/desktop/sun_java.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png

# javaws freedesktop.org menu entry
cat >> $RPM_BUILD_ROOT%{_datadir}/applications/jpackage-%{name}-javaws.desktop << EOF
[Desktop Entry]
Name=Java Web Start (%{name})
Comment=Java Application Launcher
Exec=%{_jvmdir}/%{jredir}/bin/javaws
Icon=%{name}.png
Terminal=false
Type=Application
MimeType=application/x-java-jnlp-file;
Categories=Settings;X-Sun-Supported;X-Red-Hat-Base;System;
EOF

# man pages
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
for manpage in man/man1/*; do
  install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/`basename $manpage .1`-%{name}.1
done

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a demo $RPM_BUILD_ROOT%{_datadir}/%{name}

# ghost plugin installation lists
for i in mozilla firefox ; do
  touch $RPM_BUILD_ROOT%{_datadir}/%{name}/$i-plugin-dirs
done

### font handling

pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib

   # Remove font.properties and use the system-wide one -- NiM
   rm -f font.properties
   ln -fs %{_sysconfdir}/java/font.properties .

   # remove supplied fonts.dir in preference of the one to be dynamically generated -- Rex
   rm fonts/fonts.dir

   # These %ghost'd files are created properly in %post  -- Rex
   touch fonts/{fonts.{alias,dir,scale,cache-1},XftCache,encodings.dir}

   if [ "%{fontdir}" != "%{jredir}/lib/fonts" ] ; then
      install -d -m 755 $RPM_BUILD_ROOT%{fontdir}
      mv fonts/* $RPM_BUILD_ROOT%{fontdir}
      rmdir fonts
      ln -fs %{fontdir} fonts
   fi

popd

# font registration/unregistration
install -d -m 755 $RPM_BUILD_ROOT%{xsldir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{xsldir}/register-java-fonts.xsl
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{xsldir}/unregister-java-fonts.xsl

# Most of this shamelessly stolen from redhat's kdebase-2.2.2 specfile

find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' >  %{name}-%{version}-all.files
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | sed 's|'$RPM_BUILD_ROOT'||'      >> %{name}-%{version}-all.files

grep plugin  %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-plugin.files
grep Jdbc    %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-jdbc.files
grep -F alsa.so %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-alsa.files
cat %{name}-%{version}-all.files \
  | grep -v plugin \
  | grep -v Jdbc \
  | grep -v lib/fonts \
  | grep -vF alsa.so \
  | grep -v jre/lib/security \
  > %{name}-%{version}.files

# PU_IAS addition, do not mess with trigger scripts, just carry plugin file in appropriate directory
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins/
ln -sf %{pluginname} $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins/

%clean
rm -rf $RPM_BUILD_ROOT


%preun fonts
[ $1 -eq 0 ] || exit 0

 # Unregister self in fontconfig aliases
if [ -w %{fontconfigdir}/fonts.conf ] ; then
   TMPFILE=$(/bin/mktemp -q /tmp/fonts.conf.XXXXXX) && \
   %{_bindir}/xsltproc --novalid %{xsldir}/unregister-java-fonts.xsl \
        %{fontconfigdir}/fonts.conf > $TMPFILE && \
   /bin/cat $TMPFILE > %{fontconfigdir}/fonts.conf && /bin/rm $TMPFILE
fi


%post
ext=
[ -f %{_mandir}/man1/java-%{name}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/java-%{name}.1.gz ] && ext=".gz"

update-alternatives --install %{_bindir}/java java %{jrebindir}/java %{priority} \
--slave %{_bindir}/ControlPanel            ControlPanel                %{jrebindir}/ControlPanel \
--slave %{_datadir}/javaws                 javaws                      %{jrebindir}/javaws \
--slave %{_jvmdir}/jre                     jre                         %{_jvmdir}/%{jrelnk} \
--slave %{_jvmjardir}/jre                  jre_exports                 %{_jvmjardir}/%{jrelnk} \
--slave %{_bindir}/keytool                 keytool                     %{jrebindir}/keytool \
--slave %{_bindir}/orbd                    orbd                        %{jrebindir}/orbd \
--slave %{_bindir}/policytool              policytool                  %{jrebindir}/policytool \
--slave %{_bindir}/rmid                    rmid                        %{jrebindir}/rmid \
--slave %{_bindir}/rmiregistry             rmiregistry                 %{jrebindir}/rmiregistry \
--slave %{_bindir}/servertool              servertool                  %{jrebindir}/servertool \
--slave %{_bindir}/tnameserv               tnameserv                   %{jrebindir}/tnameserv \
--slave %{_mandir}/man1/java.1$ext         java.1$ext                  %{_mandir}/man1/java-%{name}.1$ext \
--slave %{_mandir}/man1/keytool.1$ext      keytool.1$ext               %{_mandir}/man1/keytool-%{name}.1$ext \
--slave %{_mandir}/man1/orbd.1$ext         orbd.1$ext                  %{_mandir}/man1/orbd-%{name}.1$ext \
--slave %{_mandir}/man1/policytool.1$ext   policytool.1$ext            %{_mandir}/man1/policytool-%{name}.1$ext \
--slave %{_mandir}/man1/rmid.1$ext         rmid.1$ext                  %{_mandir}/man1/rmid-%{name}.1$ext \
--slave %{_mandir}/man1/rmiregistry.1$ext  rmiregistry.1$ext           %{_mandir}/man1/rmiregistry-%{name}.1$ext \
--slave %{_mandir}/man1/servertool.1$ext   servertool.1$ext            %{_mandir}/man1/servertool-%{name}.1$ext \
--slave %{_mandir}/man1/tnameserv.1$ext    tnameserv.1$ext             %{_mandir}/man1/tnameserv-%{name}.1$ext \
--slave %{_mandir}/man1/javaws.1$ext       javaws.1$ext                %{_mandir}/man1/javaws-%{name}.1$ext \
--slave %{_mandir}/man1/kinit.1$ext        kinit.1$ext                 %{_mandir}/man1/kinit-%{name}.1$ext \
--slave %{_mandir}/man1/klist.1$ext        klist.1$ext                 %{_mandir}/man1/klist-%{name}.1$ext \
--slave %{_mandir}/man1/ktab.1$ext         ktab.1$ext                  %{_mandir}/man1/ktab-%{name}.1$ext

update-alternatives --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{origin}        jre_%{origin}_exports     %{_jvmjardir}/%{jrelnk}

update-alternatives --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_exports      %{_jvmjardir}/%{jrelnk}

if [ -d %{_jvmdir}/%{jrelnk}/lib/security ]; then
  # Need to remove the old jars in order to support upgrading, ugly :(
  # update-alternatives fails silently if the link targets exist as files.
  rm -f %{_jvmdir}/%{jrelnk}/lib/security/{local,US_export}_policy.jar
fi
update-alternatives \
  --install \
    %{_jvmdir}/%{jrelnk}/lib/security/local_policy.jar \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{name}/jce/vanilla/local_policy.jar \
    %{priority} \
  --slave \
    %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar \
    jce_%{javaver}_%{origin}_us_export_policy \
    %{_jvmprivdir}/%{name}/jce/vanilla/US_export_policy.jar

if [ -f %{_sysconfdir}/mime.types ]; then
   perl -p -i -e 's|application/x-java-jnlp-file.*||g' %{_sysconfdir}/mailcap.bak 2>/dev/null
   echo "type=application/x-java-jnlp-file; description=\"Java Web Start\"; exts=\"jnlp\"" >> %{_sysconfdir}/mailcap 2>/dev/null

   perl -p -i -e 's|application/x-java-jnlp-file.*||g' %{_sysconfdir}/mime.types 2>/dev/null
   echo "application/x-java-jnlp-file      jnlp" >> %{_sysconfdir}/mime.types 2>/dev/null
fi


%post devel
ext=
[ -f %{_mandir}/man1/javac-%{name}.1.bz2 ] && ext=".bz2"
[ -f %{_mandir}/man1/javac-%{name}.1.gz ] && ext=".gz"

update-alternatives --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
--slave %{_jvmdir}/java                     java_sdk                    %{_jvmdir}/%{sdklnk} \
--slave %{_jvmjardir}/java                  java_sdk_exports            %{_jvmjardir}/%{sdklnk} \
--slave %{_bindir}/appletviewer             appletviewer                %{sdkbindir}/appletviewer \
--slave %{_bindir}/extcheck                 extcheck                    %{sdkbindir}/extcheck \
--slave %{_bindir}/idlj                     idlj                        %{sdkbindir}/idlj \
--slave %{_bindir}/jar                      jar                         %{sdkbindir}/jar \
--slave %{_bindir}/jarsigner                jarsigner                   %{sdkbindir}/jarsigner \
--slave %{_bindir}/javadoc                  javadoc                     %{sdkbindir}/javadoc \
--slave %{_bindir}/javah                    javah                       %{sdkbindir}/javah \
--slave %{_bindir}/javap                    javap                       %{sdkbindir}/javap \
--slave %{_bindir}/jdb                      jdb                         %{sdkbindir}/jdb \
--slave %{_bindir}/native2ascii             native2ascii                %{sdkbindir}/native2ascii \
--slave %{_bindir}/rmic                     rmic                        %{sdkbindir}/rmic \
--slave %{_bindir}/serialver                serialver                   %{sdkbindir}/serialver \
--slave %{_bindir}/jconsole                 jconsole                    %{sdkbindir}/jconsole \
--slave %{_bindir}/pack200                  pack200                     %{sdkbindir}/pack200 \
--slave %{_bindir}/unpack200                unpack200                   %{sdkbindir}/unpack200 \
--slave %{_bindir}/HtmlConverter            HtmlConverter               %{sdkbindir}/HtmlConverter \
--slave %{_bindir}/apt                      apt                         %{sdkbindir}/apt \
--slave %{_bindir}/jinfo                    jinfo                       %{sdkbindir}/jinfo \
--slave %{_bindir}/jmap                     jmap                        %{sdkbindir}/jmap \
--slave %{_bindir}/jps                      jps                         %{sdkbindir}/jps \
--slave %{_bindir}/jsadebugd                jsadebugd                   %{sdkbindir}/jsadebugd \
--slave %{_bindir}/jstack                   jstack                      %{sdkbindir}/jstack \
--slave %{_bindir}/jstat                    jstat                       %{sdkbindir}/jstat \
--slave %{_bindir}/jstatd                   jstatd                      %{sdkbindir}/jstatd \
--slave %{_mandir}/man1/appletviewer.1$ext  appletviewer.1$ext          %{_mandir}/man1/appletviewer-%{name}.1$ext \
--slave %{_mandir}/man1/extcheck.1$ext      extcheck.1$ext              %{_mandir}/man1/extcheck-%{name}.1$ext \
--slave %{_mandir}/man1/idlj.1$ext          idlj.1$ext                  %{_mandir}/man1/idlj-%{name}.1$ext \
--slave %{_mandir}/man1/jar.1$ext           jar.1$ext                   %{_mandir}/man1/jar-%{name}.1$ext \
--slave %{_mandir}/man1/jarsigner.1$ext     jarsigner.1$ext             %{_mandir}/man1/jarsigner-%{name}.1$ext \
--slave %{_mandir}/man1/javac.1$ext         javac.1$ext                 %{_mandir}/man1/javac-%{name}.1$ext \
--slave %{_mandir}/man1/javadoc.1$ext       javadoc.1$ext               %{_mandir}/man1/javadoc-%{name}.1$ext \
--slave %{_mandir}/man1/javah.1$ext         javah.1$ext                 %{_mandir}/man1/javah-%{name}.1$ext \
--slave %{_mandir}/man1/javap.1$ext         javap.1$ext                 %{_mandir}/man1/javap-%{name}.1$ext \
--slave %{_mandir}/man1/jdb.1$ext           jdb.1$ext                   %{_mandir}/man1/jdb-%{name}.1$ext \
--slave %{_mandir}/man1/native2ascii.1$ext  native2ascii.1$ext          %{_mandir}/man1/native2ascii-%{name}.1$ext \
--slave %{_mandir}/man1/rmic.1$ext          rmic.1$ext                  %{_mandir}/man1/rmic-%{name}.1$ext \
--slave %{_mandir}/man1/serialver.1$ext     serialver.1$ext             %{_mandir}/man1/serialver-%{name}.1$ext \
--slave %{_mandir}/man1/jconsole.1$ext      jconsole.1$ext              %{_mandir}/man1/jconsole-%{name}.1$ext \
--slave %{_mandir}/man1/pack200.1$ext       pack200.1$ext               %{_mandir}/man1/pack200-%{name}.1$ext \
--slave %{_mandir}/man1/unpack200.1$ext     unpack200.1$ext             %{_mandir}/man1/unpack200-%{name}.1$ext \
--slave %{_mandir}/man1/apt.1$ext           apt.1$ext                   %{_mandir}/man1/apt-%{name}.1$ext \
--slave %{_mandir}/man1/jinfo.1$ext         jinfo.1$ext                 %{_mandir}/man1/jinfo-%{name}.1$ext \
--slave %{_mandir}/man1/jmap.1$ext          jmap.1$ext                  %{_mandir}/man1/jmap-%{name}.1$ext \
--slave %{_mandir}/man1/jps.1$ext           jps.1$ext                   %{_mandir}/man1/jps-%{name}.1$ext \
--slave %{_mandir}/man1/jsadebugd.1$ext     jsadebugd.1$ext             %{_mandir}/man1/jsadebugd-%{name}.1$ext \
--slave %{_mandir}/man1/jstack.1$ext        jstack.1$ext                %{_mandir}/man1/jstack-%{name}.1$ext \
--slave %{_mandir}/man1/jstat.1$ext         jstat.1$ext                 %{_mandir}/man1/jstat-%{name}.1$ext \
--slave %{_mandir}/man1/jstatd.1$ext        jstatd.1$ext                %{_mandir}/man1/jstatd-%{name}.1$ext

update-alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{origin}        java_sdk_%{origin}_exports     %{_jvmjardir}/%{sdklnk}

update-alternatives --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}       java_sdk_%{javaver}_exports      %{_jvmjardir}/%{sdklnk}


# We do not care if all/any of this actually succeeds
# Therefore errors are caught but messages are allowed
%post fonts
{
    # Legacy font handling

    %{_bindir}/ttmkfdir -d %{fontdir} -o %{fontdir}/fonts.scale

    # Mandrake workaround
    %{_bindir}/perl -pi -e 's@0-c-0@0-p-0@g' %{fontdir}/fonts.scale

    %{x11bindir}/mkfontdir -e %{x11encdir} -e %{x11encdir}/large %{fontdir}

    %{_sbindir}/chkfontpath -q -a %{fontdir}

    # The following commands will be executed on upgrade by their respective
    # packages

    # Late legacy font handling
    if [ -x %{_bindir}/redhat-update-gnome-font-install ] ; then
        %{_bindir}/redhat-update-gnome-font-install
    fi

    if [ -x %{_bindir}/redhat-update-gnome-font-install2 ] ; then
        %{_bindir}/redhat-update-gnome-font-install2
    fi

    # Modern font handling
    if [ -x %{_bindir}/fc-cache ] ; then
        %{_bindir}/fc-cache -f %{_datadir}/fonts
    fi
} || :


%triggerin fonts -- fontconfig, %{fontconfigdir}/fonts.conf

TMPFILE=$(/bin/mktemp -q /tmp/fonts.conf.XXXXXX) && \
%{_bindir}/xsltproc --novalid %{xsldir}/register-java-fonts.xsl \
   %{fontconfigdir}/fonts.conf > $TMPFILE && \
/bin/cat $TMPFILE > %{fontconfigdir}/fonts.conf && /bin/rm $TMPFILE


%postun
if [ $1 -eq 0 ]; then
  update-alternatives --remove java %{jrebindir}/java
  update-alternatives --remove \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{name}/jce/vanilla/local_policy.jar
  update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk}
  update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi


%postun devel
if [ $1 -eq 0 ]; then
  update-alternatives --remove javac %{sdkbindir}/javac
  update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
  update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi


# We do not care if all/any of this actually succeeds
# Therefore errors are catched but messages allowed
%postun fonts
{
   # Rehash the font dir to keep only stuff manually installed
   [ $1 -eq 0 ] || exit 0

   if [ -d %{fontdir} ] && [ $(%{_bindir}/find %{fontdir} \
        -follow -type f -iname "*.ttf" -printf "\b\b\b\btrue") ] ; then

        %{_bindir}/ttmkfdir -d %{fontdir} -o %{fontdir}/fonts.scale
        %{x11bindir}/mkfontdir -e %{x11encdir} -e %{x11encdir}/large %{fontdir}

   else
        %{_sbindir}/chkfontpath -q -r %{fontdir}
   fi

   if [ -x %{_bindir}/redhat-update-gnome-font-install ] ; then
        %{_bindir}/redhat-update-gnome-font-install
   fi

   if [ -x %{_bindir}/redhat-update-gnome-font-install2 ] ; then
        %{_bindir}/redhat-update-gnome-font-install2
   fi

   if [ -x %{_bindir}/fc-cache ] ; then
        %{_bindir}/fc-cache -f %{_datadir}/fonts
   fi

} || :


%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%doc jre/COPYRIGHT jre/README
%doc jre/Welcome.html
%dir %{_jvmdir}/%{sdkdir}
%{jvmjardir}
%{_jvmdir}/%{jredir}/lib/fonts
%dir %{_jvmdir}/%{jredir}/lib/security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/javaws.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/blacklist
%ghost %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%ghost %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%{_jvmdir}/%{jredir}/lib/security/trusted.libraries
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{_mandir}/man1/java-%{name}.1*
%{_mandir}/man1/keytool-%{name}.1*
%{_mandir}/man1/orbd-%{name}.1*
%{_mandir}/man1/policytool-%{name}.1*
%{_mandir}/man1/rmid-%{name}.1*
%{_mandir}/man1/rmiregistry-%{name}.1*
%{_mandir}/man1/servertool-%{name}.1*
%{_mandir}/man1/tnameserv-%{name}.1*
%{_mandir}/man1/javaws-%{name}.1*
%{_mandir}/man1/jvisualvm-%{name}.1*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png

%files devel
%defattr(-,root,root,-)
%doc COPYRIGHT README.html
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_mandir}/man1/appletviewer-%{name}.1*
%{_mandir}/man1/extcheck-%{name}.1*
%{_mandir}/man1/idlj-%{name}.1*
%{_mandir}/man1/jar-%{name}.1*
%{_mandir}/man1/jarsigner-%{name}.1*
%{_mandir}/man1/javac-%{name}.1*
%{_mandir}/man1/javadoc-%{name}.1*
%{_mandir}/man1/javah-%{name}.1*
%{_mandir}/man1/javap-%{name}.1*
%{_mandir}/man1/jdb-%{name}.1*
%{_mandir}/man1/native2ascii-%{name}.1*
%{_mandir}/man1/rmic-%{name}.1*
%{_mandir}/man1/serialver-%{name}.1*
%{_mandir}/man1/jconsole-%{name}.1*
%{_mandir}/man1/pack200-%{name}.1*
%{_mandir}/man1/unpack200-%{name}.1*
%{_mandir}/man1/apt-%{name}.1*
%{_mandir}/man1/jinfo-%{name}.1*
%{_mandir}/man1/jmap-%{name}.1*
%{_mandir}/man1/jps-%{name}.1*
%{_mandir}/man1/jsadebugd-%{name}.1*
%{_mandir}/man1/jstack-%{name}.1*
%{_mandir}/man1/jstat-%{name}.1*
%{_mandir}/man1/jstatd-%{name}.1*
%{_mandir}/man1/jhat-%{name}.1.gz
%{_mandir}/man1/jrunscript-%{name}.1.gz
%{_mandir}/man1/schemagen-%{name}.1.gz
%{_mandir}/man1/wsgen-%{name}.1.gz
%{_mandir}/man1/wsimport-%{name}.1.gz
%{_mandir}/man1/xjc-%{name}.1.gz
%ifnarch x86_64
%{cgibindir}/java-rmi-%{version}.cgi
%endif

%files src
%defattr(-,root,root,-)
%{_jvmdir}/%{sdkdir}/src.zip

%files demo
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/demo

%files alsa -f %{name}-%{version}-alsa.files
%defattr(-,root,root,-)

%files jdbc -f %{name}-%{version}-jdbc.files
%defattr(-,root,root,-)

%files plugin -f %{name}-%{version}-plugin.files
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%ghost %{_datadir}/%{name}/*-plugin-dirs
%{_libdir}/mozilla/plugins/*

%files fonts
%defattr(0644,root,root,0755)
%dir %{fontdir}
%dir %{xsldir}
%{fontdir}/*.ttf
%{xsldir}/*.xsl
%config(noreplace) %{fontdir}/fonts.alias
%ghost %{fontdir}/fonts.dir
%ghost %{fontdir}/fonts.scale
%ghost %{fontdir}/fonts.cache-1
%ghost %{fontdir}/XftCache
%ghost %{fontdir}/encodings.dir


%changelog
* Mon Feb 09 2009 Josko Plazonic <plazonic@math.princeton.edu>
- add plugin for 64 bit - now present in u12

* Wed Apr 18 2007 Josko Plazonic <plazonic@math.princeton.edu>
- fix up X11 path, add coreutils as one of required apps - needed
  during install

* Mon Apr  2 2007 Lyle Dietz <derritter@optusnet.com.au> 0:1.6.0.0-0.0.ld.0
- Upgrade to 1.6.0 update 1

* Thu Dec 21 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.10-2jpp
- respin, no changes

* Wed Dec 20 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.10-1jpp
- Upgrade to 1.5.0_10

* Mon Oct  2 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.09-1jpp
- Upgrade to 1.5.0_09... stupid Sun :-P (submitted by Henning Schmiedehausen)

* Fri Sep 29 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.08-1jpp
- Upgrade to 1.5.0_08

* Fri Jun 8 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.07-1jpp
- Upgrade to 1.5.0_07

* Fri Feb 3 2006 Jason Corley <jason.corley@gmail.com> 0:1.5.0.06-1jpp
- Upgrade to 1.5.0_06

* Wed Sep 28 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.05-1jpp
- Upgrade to 1.5.0_05

* Mon Jun 27 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.04-1jpp
- Upgrade to 1.5.0_04

* Wed May 04 2005 David Walluck <david@jpackage.org> 0:1.5.0.03-1jpp
- 1.5.0_03

* Wed Mar 16 2005 Jason Corley <jason.corley@gmail.com> 0:1.5.0.02-1jpp
- Upgrade to 1.5.0_02

* Tue Feb 08 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.5.0.01-3jpp
- Support for x86_64 (amd64); no javaws, no plugins

* Wed Jan 19 2005 David Walluck <david@jpackage.org> 0:1.5.0.01-1jpp
- 1.5.0_01

* Thu Jan 06 2005 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0.01-0.cte.1
- Updated to Upstream 1.5.0_01.
- Added long cvsversion definition.
- Rearranged defintiions that are sensitive to buildver.

* Sat Nov 13 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.0-3jpp
- Provide java-sasl.
- Fix build failure when no previous java-1.5.0 package is installed
  (%%{jvmjardir}/*.jar are dangling symlinks at build time).
- Minor spec cleanups and consistency tweaks.

* Sun Oct 17 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-2jpp.cte.1
- Switched off rpm internal dependency generator. This fixes the bogus
  devel package provides noted in 1.5.0-0.beta2.4jpp.
- Changed auto requires/provides for all packages to be the same as
  java-1.4.2-sun (all on except jdbc due to libodbc name variability).
- AutoReq off for demo package as it still looks for libjava_crw_demo_g.so.

* Mon Oct  4 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.0-2jpp
- Update to 1.5.0, thanks to Carwyn Edwards.
- Fix alternative priority (1500 -> 1503, where "3" is Sun).

* Fri Oct 1 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.cte.1
- Added missing Obsoletes for java-1.4.2-plugin.
- Modified release version to use fedora.us style 0. so jpp packages
  will override mine.

* Thu Sep 30 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-1jpp
- Updated to 1.5.0 final.

* Thu Sep 02 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.rc.1jpp
- Updated to J2SE 1.5.0 rc.
- Added alternatives slaves for new tools (and their man pages):
  apt, jinfo, jmap, jps, jsadebugd, jstack, jstat and jstatd.

* Mon Aug 02 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.beta2.4jpp
- Switch off AutoReq for demo package (breaks on: libjava_crw_demo.so).
- Switch off AutoReqProv for devel package (Provides: lib.so!?).

* Thu Jul 29 2004 Carwyn Edwards <carwyn@carwyn.com> 0:1.5.0-0.beta2.3jpp
- Corrected Requires and BuildRequires for jpackage-utils (1.5.38).

* Sun Jul 25 2004 Carwyn Edwards <carwyn@carwyn.com> - 0:1.5.0-0.beta2.2jpp
- Use %%{_datadir}/xml for XSL's per FHS.
- Change plugin handling to be the same as 1.4.2.05-3jpp(sun)
  (adds firefox support).
- Remove dependency on %%{_bindir}/mozilla.
- Change manpage extension management to be the same as 1.4.2.05-3jpp(sun)
  (also supports uncompressed man pages).
- Rollback javaws alternative location to _datadir location so that concurrent
  jdk installation works again.
- Fixed freedesktop.org menu entry - Exec line was incorrect.
- Corrected the way the jconsole, pack200 and unpack200 man pages were added
  (use macros, added slave links).
- Actaully add jconsole, pack200, unpack200 and their alternatives links.

* Fri Jul 23 2004 Carwyn Edwards <carwyn@carwyn.com> 0:1.5.0-0.beta2.1jpp
- Updated to J2SE 1.5.0 Beta 2.
- Upstream filenames have changed, string replacement: "j2sdk" -> "jdk".
- Remove attempt to copy jre/.systemPrefs (it isn't there any more).
- Added man pages for jconsole, pack200 and unpack200

* Wed Feb 25 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.3jpp
- remove some unused code from the spec file

* Fri Feb 20 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.2jpp
- find man extension based on distribution
- ensure correct plugin installation
- Obsoletes: java-1.4.2-fonts
- install java-rmi.cgi
- move ControlPanel back to main so that we can use update-alternatives
- fix ControlPanel, HtmlConverter, and java-rmi.cgi bash scripts
- use included .desktop file for ControlPanel and modify included .desktop file for javaws

* Mon Feb 09 2004 David Walluck <david@anti-microsoft.org> 0:1.5.0-0.beta1.1jpp
- J2SE 1.5.0 Beta 1
- change javaws alternative to point to %%{_bindir}/javaws and only edit
  %%{_sysconfdir}/mime.types if it exists
- add javaws menu into main package (still looking for icon)
- fix installing extensions when %%{version} = %%{javaver}
- add epochs to all requires and provides
- really turn off automatic dependency generation
