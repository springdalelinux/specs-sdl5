%define name          xscreensaver

%define version       5.01
%define beta_ver      %{nil}
%define fedora_rel    6

%define default_text  %{_datadir}/eula/eula.en_US

%define pam_ver       0.80-7
%define autoconf_ver  2.53

%define update_po     1
%define allow_non_passwd    0

Buildroot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary:         X screen saver and locker
Name:            %{name}
Version:         %{version}
Release:         %{fedora_rel}%{?dist}%{?extrarel}
Epoch:           1
License:         BSD
Group:           Amusements/Graphics
URL:             http://www.jwz.org/xscreensaver/
Source0:         http://www.jwz.org/xscreensaver/xscreensaver-%{version}%{?beta_ver}.tar.gz
Patch1:          xscreensaver-5.00b5-sanitize-hacks.patch
Patch8:          xscreensaver-5.00b5-include-directory.patch
Patch21:         xscreensaver-5.01-webcollage-default-nonet.patch
Patch114:        xscreensaver-5.01a1-pam-popup-passwindow.patch
Requires:        xscreensaver-base = %{epoch}:%{version}-%{release}
Requires:        xscreensaver-extras = %{epoch}:%{version}-%{release}
Requires:        xscreensaver-gl-extras = %{epoch}:%{version}-%{release}

%package base
Summary:         A minimal installation of xscreensaver
Group:           Amusements/Graphics
BuildRequires:   gettext
BuildRequires:   desktop-file-utils
%if %{allow_non_passwd}
BuildRequires:   autoconf >= %{autoconf_ver}
%endif
BuildRequires:   sed
BuildRequires:   libtool
BuildRequires:   bc
BuildRequires:   pam-devel > %{pam_ver}
BuildRequires:   xorg-x11-proto-devel
BuildRequires:   libX11-devel, libXScrnSaver-devel, libXext-devel
BuildRequires:   libXinerama-devel
BuildRequires:   libXmu-devel
BuildRequires:   libXpm-devel
BuildRequires:   libXt-devel
BuildRequires:   libXxf86misc-devel
BuildRequires:   libXxf86vm-devel
BuildRequires:   libjpeg-devel
BuildRequires:   gtk2-devel libglade2-devel
BuildRequires:   PU_IAS-release
Requires:        /etc/pam.d/system-auth
Requires:        pam > %{pam_ver}
Requires:        xorg-x11-resutils

%package extras
Summary:         An enhanced set of screensavers
Group:           Amusements/Graphics
BuildRequires:   desktop-backgrounds-basic
Requires:        xscreensaver-base

%package gl-extras
Summary:         An enhanced set of screensavers that require OpenGL
Group:           Amusements/Graphics
Provides:        xscreensaver-gl = %{epoch}:%{version}-%{release}
Obsoletes:       xscreensaver-gl
BuildRequires:   libGLU-devel, libGL-devel
Requires:        xscreensaver-base

%package extras-gss
Summary:         Desktop files of extras for gnome-screensaver
Group:           Amusements/Graphics
Requires:        %{name}-extras = %{epoch}:%{version}-%{release}
Requires:        gnome-screensaver

%package gl-extras-gss
Summary:         Desktop files of gl-extras for gnome-screensaver
Group:           Amusements/Graphics
Requires:        %{name}-gl-extras = %{epoch}:%{version}-%{release}
Requires:        gnome-screensaver


%description
A modular screen saver and locker for the X Window System.
More than 200 display modes are included in this package.

This is a metapackage for installing all default packages
related to XScreenSaver.

%description -l fr
Un économiseur d'écran modulaire pour le système X Window.
Plus de 200 modes d'affichages sont inclus dans ce paquet.

This is a metapackage for installing all default packages
related to XScreenSaver.

%description base
A modular screen saver and locker for the X Window System.
This package contains the bare minimum needed to blank and
lock your screen.  The graphical display modes are the
"xscreensaver-extras" and "xscreensaver-gl-extras" packages.

%description -l fr base 
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient le minimum vital pour éteindre et verouiller
votre écran. Les modes d'affichages graphiques sont inclus
dans les paquets "xscreensaver-extras" et "xscreensaver-gl-extras".

%description extras
A modular screen saver and locker for the X Window System.
This package contains a variety of graphical screen savers for
your mind-numbing, ambition-eroding, time-wasting, hypnotized
viewing pleasure.

%description -l fr extras
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient une pléthore d'économiseurs d'écran graphiques
pour votre plaisir des yeux.

%description gl-extras
A modular screen saver and locker for the X Window System.
This package contains a variety of OpenGL-based (3D) screen
savers for your mind-numbing, ambition-eroding, time-wasting,
hypnotized viewing pleasure.

%description -l fr gl-extras
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient une pléthore d'économiseurs d'écran basés sur OpenGL (3D)
pour votre plaisir des yeux.

%description extras-gss
This package contains desktop files of extras screensavers
for gnome-screensaver compatibility.

%description gl-extras-gss
This package contains desktop files of gl-extras screensavers
for gnome-screensaver compatibility.



%prep
%setup -q -n %{name}-%{version}%{?beta_ver}

%patch1 -p1 -b .sanitize-hacks
%patch8 -p1 -b .include-dir
%patch21 -p1 -b .nonet
# don't apply for now
%if %{allow_non_passwd}
%patch114 -p1 -b .non-passwd
%endif

change_option(){
   set +x
   ADFILE=$1
   if [ ! -f ${ADFILE}.opts ] ; then
      cp -p $ADFILE ${ADFILE}.opts
   fi
   shift

   for ARG in "$@" ; do
      TYPE=`echo $ARG | sed -e 's|=.*$||'`
      VALUE=`echo $ARG | sed -e 's|^.*=||'`

      eval sed -i \
         -e \'s\|\^\\\(\\\*$TYPE\:\[ \\t\]\[ \\t\]\*\\\)\[\^ \\t\]\.\*\$\|\\1$VALUE\|\' \
         $ADFILE
   done
   set -x
}

silence_hack(){
   set +x
   ADFILE=$1
   if [ ! -f ${ADFILE}.hack ] ; then
      cp -p $ADFILE ${ADFILE}.hack
   fi
   shift

   for hack in "$@" ; do
      eval sed -i \
         -e \'\/\^\[ \\t\]\[ \\t\]\*$hack\/s\|\^\|-\|g\' \
         -e \'s\|\^@GL_\.\*@.*\\\(GL\:\[ \\t\]\[ \\t\]\*$hack\\\)\|-\\t\\1\|g\' \
         $ADFILE
   done
   set -x
}

# change some options
change_option driver/XScreenSaver.ad.in \
   passwdTimeout=0:00:15 \
   grabDesktopImages=False \
   lock=True \
   splash=False \
   ignoreUninstalledPrograms=True \
   textProgram=fortune\ -s \
   passwd.heading.label=Screen\ Locked

# silence the following hacks by default
silence_hack driver/XScreenSaver.ad.in \
   bsod flag

# record time, version
eval sed -i.ver \
   -e \'s\|version \[45\]\.\[0-9a-z\]\[0-9a-z\]\*\|version %{version}-`echo \
      %{release} | sed -e 's|\.[a-z][a-z0-9].*$||'`\|\' \
      driver/XScreenSaver.ad.in

eval sed -i.date \
   -e \'s\|\[0-9\].\*-.\*-20\[0-9\]\[0-9\]\|`LANG=C date -u +'%%d-%%b-%%Y'`\|g\' \
   driver/XScreenSaver.ad.in

eval sed -i.ver \
   -e \'s\|\(\[0-9\].\*-.\*-20\[0-9\]\[0-9\]\)\|\(`LANG=C \
      date -u +'%%d-%%b-%%Y'`\)\|g\' \
   -e \'s\|\\\(5.\[0-9\]\[0-9\]\\\)[a-z]\[0-9\]\[0-9\]\*\|\\\1\|\' \
   -e \'s\|5.\[0-9\]\[0-9\]\|%{version}-`echo %{release} | \
      sed -e 's|\.[a-zA-Z][a-zA-Z0-9].*$||'`\|\' \
   utils/version.h

# move man entry to 6x.
for f in `find hacks -name Makefile.in` ; do
   sed -i.mansuf \
      -e '/^mansuffix/s|6|6x|'\
      $f
done

# search first 6x entry, next 1 entry for man pages
sed -i.manentry -e 's@man %%s@man 6x %%s 2>/dev/null || man 1 %%s @' \
   driver/XScreenSaver.ad.in

# suppress rpmlint booing.
# suppress about pam config (although this is 
# not the fault of xscreensaver.pam ......).
sed -i.rpmlint -n -e '1,5p' driver/xscreensaver.pam 

if [ -x %{_datadir}/libtool/config.guess ]; then
  # use system-wide copy
   cp -p %{_datadir}/libtool/config.{sub,guess} .
fi

%build
%if %{allow_non_passwd}
autoconf
%endif
archdir=`./config.guess`
mkdir $archdir
cd $archdir

export CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}"

CONFIG_OPTS="--prefix=%{_prefix} --with-pam --without-shadow --without-kerberos"
CONFIG_OPTS="$CONFIG_OPTS --without-setuid-hacks"
CONFIG_OPTS="$CONFIG_OPTS --with-text-file=%{default_text}"
CONFIG_OPTS="$CONFIG_OPTS --with-x-app-defaults=%{_datadir}/X11/app-defaults"
CONFIG_OPTS="$CONFIG_OPTS --disable-root-passwd"
CONFIG_OPTS="$CONFIG_OPTS --with-browser=htmlview"
%if %{allow_non_passwd}
CONFIG_OPTS="$CONFIG_OPTS --disable-non-passwd"
%endif

# This is flaky:
# CONFIG_OPTS="$CONFIG_OPTS --with-login-manager"

ln -s ../configure .
%configure $CONFIG_OPTS
rm -f configure

%if %{update_po}
( cd po ; make generate_potfiles_in update-po )
%endif

make %{?_smp_mflags}

%install
archdir=`./config.guess`
cd $archdir

rm -rf ${RPM_BUILD_ROOT}

make install_prefix=$RPM_BUILD_ROOT INSTALL="install -c -p" install

desktop-file-install --vendor gnome --delete-original    \
   --dir $RPM_BUILD_ROOT%{_datadir}/applications         \
   --add-only-show-in GNOME                              \
   --add-category X-Red-Hat-Base                         \
   $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# This function prints a list of things that get installed.
# It does this by parsing the output of a dummy run of "make install".
list_files() {
   echo "%%defattr(-,root,root)"
   make -s install_prefix=${RPM_BUILD_ROOT} INSTALL=true "$@"  \
      | sed -e 's|directory* \([^ ][^ ]*\)$|/%%dir\1|'         \
      | sed -n -e 's@.* \(/[^ ]*\)$@\1@p'                      \
      | sed    -e "s@${RPM_BUILD_ROOT}@@"                      \
               -e "s@/[a-z][a-z]*/\.\./@/@"                    \
      | sed    -e '/%%dir/!s@\(.*/man/.*\)@\1\*@'              \
               -e '/%%dir/!s@\(.*/pam\.d/\)@%%config(noreplace) \1@'  \
               -e 's|/%%dir\([^ ][^ ]*\)$|%%dir \1|'           \
      | sort  \
      | uniq
}

# Generate three lists of files for the three packages.
#
dd=%{_builddir}/%{name}-%{version}%{?beta_ver}
(  cd hacks     ; list_files install ) >  $dd/extras.files
(  cd hacks/glx ; list_files install ) >  $dd/gl-extras.files
(  cd driver    ; list_files install ) >  $dd/base.files

# add documents
pushd $dd &> /dev/null
for f in README* ; do
   echo "%%doc $f" >> $dd/base.files
done
popd

%find_lang %{name}
cat %{name}.lang | uniq >> $dd/base.files

# suppress rpmlint booing
# remove directories explicitly included in filesystem rpm
for f in \
   %{_sysconfdir}/pam.d \
   %{_bindir} \
   %{_datadir}/applications \
   %{_datadir}/pixmaps \
   %{_datadir}/X11/app-defaults \
   %{_mandir}/man[1-9] \
   ; do
   :
   ff=`echo $f | sed -e 's|\/|\\\\\\\\\/|g'`
   for g in $dd/*.files ; do
      eval sed -i -e \/$ff\$\/d $g
   done
done

# sanitize path in script file
for f in ${RPM_BUILD_ROOT}%{_bindir}/xscreensaver-getimage-* \
   ${RPM_BUILD_ROOT}%{_libexecdir}/xscreensaver/vidwhacker \
   ${RPM_BUILD_ROOT}%{_bindir}/xscreensaver-text ; do
   if [ -f $f ] ; then
      sed -i -e 's|%{_prefix}//bin|%{_bindir}|g' $f
   fi
done

# create desktop entry for gnome-screensaver
create_desktop(){
   COMMAND=`cat $1 | sed -n -e 's|^<screen.*name=\"\([^ ][^ ]*\)\".*$|\1|p'`
   NAME=`cat $1 | sed -n -e 's|^<screen.*_label=\"\(.*\)\">.*$|\1|p'`
   ARG=`cat $1 | sed -n -e 's|^.*<command arg=\"\([^ ][^ ]*\)\".*$|\1|p'`
   ARG=`echo $ARG`
   COMMENT="`cat $1 | sed -e '1,/_description/d' | \
     sed -e '/_description/q' | sed -e '/_description/d'`"
   COMMENT=`echo $COMMENT`

# webcollage treatment
   if [ "x$COMMAND" = "xwebcollage" ] ; then
      ARG="$ARG -directory %{_datadir}/backgrounds/images"
   fi

   if [ "x$NAME" = "x" ] ; then NAME=$COMMAND ; fi

   rm -f $2
   echo "[Desktop Entry]" >> $2
   echo "Encoding=UTF-8" >> $2
   echo "Name=$NAME" >> $2
   echo "Comment=$COMMENT" >> $2
   echo "TryExec=$COMMAND" >> $2
   echo "Exec=$COMMAND $ARG" >> $2
   echo "StartupNotify=false" >> $2
   echo "Type=Application" >> $2
   echo "Categories=Screensaver" >> $2
}

cd $dd

SAVERDIR=%{_datadir}/applications/screensavers
mkdir -p ${RPM_BUILD_ROOT}${SAVERDIR}

for list in *extras.files ; do

   glist=gnome-$list
   rm -f $glist

   echo "%%defattr(-,root,root)" > $glist
   echo "%%dir $SAVERDIR" >> $glist

   set +x
   for xml in `cat $list | grep xml$` ; do
      file=${RPM_BUILD_ROOT}${xml}
      desktop=xscreensaver-`basename $file`
      desktop=${desktop%.xml}.desktop

      echo + create_desktop $file  ${RPM_BUILD_ROOT}${SAVERDIR}/$desktop
      create_desktop $file  ${RPM_BUILD_ROOT}${SAVERDIR}/$desktop
      echo ${SAVERDIR}/$desktop >> $glist
   done
   set -x
done

# Make sure all files are readable by all, and writable only by owner.
#
chmod -R a+r,u+w,og-w ${RPM_BUILD_ROOT}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)

%files -f base.files base
%defattr(-,root,root)

%files -f extras.files extras
%defattr(-,root,root)

%files -f gl-extras.files gl-extras
%defattr(-,root,root)

%files -f gnome-extras.files extras-gss
%defattr(-,root,root)

%files -f gnome-gl-extras.files gl-extras-gss
%defattr(-,root,root)

%changelog
* Sat Feb  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-6
- Make hack packages require base package (#227017)
- Create xscreensaver metapackage

* Mon Nov 20 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-5
- Require xorg-x11-resutils (#216245)

* Sun Nov  5 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-4
- No net connection by default for webcollage (possibly fix #214095 ?)

* Fri Sep 29 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-3
- Fix the arguments of desktop files (#208560)

* Tue Sep 26 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-2
- Finally move man pages to 6x (#205796)
- Fix the ownership of directories (#187892)

* Tue Sep 19 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-1
- 5.01
- Revert non-passwd auth patch and disable it for now (see bug #205669)

* Sun Sep 17 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.01-0.a1.2
- 5.01a1
- Revert lang related patch (still needing some works)
- Disable small scale window (patch from upstream)
- Disable non-password authentication.

* Sun Sep 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-22
- Fix Patch114.

* Sun Sep 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-21
- Try to support non-password PAM authentication (bug #205669)

* Sat Sep  9 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-20
- Change default document.
- Again man entry fix.

* Tue Sep  5 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-19
- Create desktop files for gnome-screensaver (bug #204944)

* Mon Aug 28 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-18
- Unify locale releated patches.

* Mon Aug 28 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-17.1
- Rebuild.

* Fri Aug 18 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-17
- Very nasty segv problem was brought by me. Fixing......
 
* Thu Aug 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-16
- Move man entry to 6x (bug #197741)

* Fri Jul 28 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-15
- Rebuild again as fedora-release-5.91.1 is released.

* Mon Jul 17 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-14
- Correct paths to update po files properly and try re-creating po files.
- Rebuild for FC6T2 devel freeze.

* Mon Jul  3 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-13
- Fix for causing SEGV on exit about petri, squiral (total: 22 hacks)
  I hope this will finally fix all hacks' problems.

* Sun Jul  2 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-12
- Fix other (extras, gl-extras) hacks (total: 21 hacks).
- Make sure the subprocess xscreensaver-getimage is properly
  killed by parent hack process.

* Fri Jun 30 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-11
- Fix interaggregate segv.

* Thu Jun 29 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-10
- Fix xscreensaver-extras hacks which cause SEGV or SIGFPE.

* Tue Jun 27 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-9
- Don't make xscreensaver-base require htmlview.
- Update ja.po again.
- Fix noseguy not to eat cpu when geometry is too small.

* Fri Jun 23 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-8
- Spec file script change.
- Add libtool to BuildRequires.

* Thu Jun 15 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-7
- Change timestamps.
- Forcely replace the default text till the release version of fedora-release
  formally changes.

* Sat Jun 10 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-6.1
- Fix the requirement for rebuilding to meet the demand
  from current mock.

* Wed Jun  7 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-6
- Another fixes of config files for ifsmap as reported to jwz 
  livejournal page.
- Update Japanese translation.
- Locale fix for xscreensaver-text.

* Thu Jun  1 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-5
- Disable (not remove) some hacks by default according to 4.24 behavior.
- XML file fix for slidescreen.

* Thu Jun  1 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-4
- Rewrite the patch for decimal separator as discussed with jwz.
- Change defaults not by patch but by function.

* Wed May 31 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-3
- Fix browser option patch.

* Wed May 31 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-2
- Change the default text.
- Rewrite root passwd patch.
- Add browser option to configure.
- Fix requirement about desktop-backgrounds-basic.
- Fix decimal separator problem reported by upstream.

* Fri May 26 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:5.00-1
- Update to 5.00 .
- Switch to extras, don't remove anything.

* Fri Mar 24 2006 Ray Strode <rstrode@redhat.com> - 1:4.24-2
- add patch from jwz to reap zombie processes (bug 185833)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:4.24-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:4.23-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Ray Strode <rstrode@redhat.com> 1:4.23-1
- update to 4.23
- add a BuildRequires on imake (spotted by Mamoru Tasaka)
- add a lot of patches and fixes from Mamoru Tasaka

* Sat Dec 17 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Ray Strode <rstrode@redhat.com> 1:4.22-21
- Update list_files function to fix ownership issues.
  Patch from Mamoru Tasaka (mtasaka@ioa.s.u-tokyo.ac.jp) (bug 161728).

* Tue Nov  1 2005 Ray Strode <rstrode@redhat.com> 1:4.22-20
- Switch requires to modular X

* Thu Oct 13 2005 Tomas Mraz <tmraz@redhat.com> 1:4.22-19
- use include instead of pam_stack in pam config

* Wed Sep 28 2005 Ray Strode <rstrode@redhat.com> 1:4.22-18
- accept zero timeout values for suspend and off.
  Patch from Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
  (bug 157501). 

* Fri Sep 23 2005 Ray Strode <rstrode@redhat.com> 1:4.22-17
- remove explicit dependency on xscreensaver-base for 
  extras and gl-extras packages

* Fri Sep 16 2005 Ray Strode <rstrode@redhat.com> 1:4.22-16
- don't allow root to authenticate lock dialog when selinux
  is enabled (bug 157014).

* Fri Sep  9 2005 Ray Strode <rstrode@redhat.com> 1:4.22-15
- take BSOD out of the default random list (bug 105388).

* Thu Sep 08 2005 Florian La Roche <laroche@redhat.com>
- add version-release to the Provides:

* Wed Sep  7 2005 Ray Strode <rstrode@redhat.com> 1:4.22-13
- Patch from Mamoru Tasaka to improve man page handling
  (bug 167708).

* Tue Sep  6 2005 Ray Strode <rstrode@redhat.com> 1:4.22-12
- remove density option from squiral screensaver,
  Patch from Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
  (bug 167374).

* Wed Aug 31 2005 Ray Strode <rstrode@redhat.com> 1:4.22-11
- ignore unprintable characters in password dialog (bug 135966).

* Thu Aug 25 2005 Ray Strode <rstrode@redhat.com> 1:4.22-10
- Move man pages to section 6 (bug 166441). 

* Wed Aug 24 2005 Ray Strode <rstrode@redhat.com> 1:4.22-9
- The only legitimate way to call realpath is with NULL 
  buffer (bug 165270).

* Fri Aug 19 2005 Ray Strode <rstrode@redhat.com> 1:4.22-8
- Don't try to use an invalid tree iterator (bug 166299)

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 1:4.22-7
- rebuild for new cairo

* Wed Aug 10 2005 Ray Strode <rstrode@redhat.com> 1:4.22-6
- Don't call printf in signal handler (might fix 126428)

* Wed Aug  3 2005 Ray Strode <rstrode@redhat.com> 1:4.22-5
- Update to xscreensaver 4.22.

* Sun Jun 19 2005 Ray Strode <rstrode@redhat.com> 1:4.21-5
- Add build requires for desktop-file-utils (bug 160980). 

* Wed May 11 2005 Ray Strode <rstrode@redhat.com> 1:4.21-4
- Allow configuration gui to support hacks with absolute paths
  (bug 157417). 

* Mon May 09 2005 Ray Strode <rstrode@redhat.com> 1:4.21-3
- Use @libexecdir@/xscreensaver instead of @HACKDIR@ in
  default configuration file so that the path gets expanded
  fully (bug 156906).

* Tue May 03 2005 Ray Strode <rstrode@redhat.com> 1:4.21-2
- Use absolute filenames for screenhacks so we don't pull
  in screenhacks from PATH (bug 151677).
- Don't try to ping in sonar screensaver (bug 139692).

* Sun Mar 20 2005 Ray Strode <rstrode@redhat.com> 1:4.21-1
- Update to xscreensaver-4.21.
- Update spec file to better match new upstream spec file.

* Fri Feb 25 2005 Nalin Dahyabhai <nalin@redhat.com> 1:4.18-19
- We don't patch configure.in, so we don't need to run 'autoconf'.
- Add --without-kerberos to skip built-in Kerberos password verification, so
  that we'll always go through PAM (fixes 149731).

* Mon Feb 21 2005 Ray Strode <rstrode@redhat.com> 1:4.18-18
- Install desktop files to /usr/share/applications instead of
  /usr/share/control-center-2.0 (should fix bug 149229).

* Thu Jan  6 2005 Ray Strode <rstrode@redhat.com> 1:4.18-17
- Change lock dialog instructions to only ask for password
  and not username.

* Tue Jan  4 2005 Ray Strode <rstrode@redhat.com> 1:4.18-16
- Add patch to spec file to change defaults

* Tue Jan  4 2005 Ray Strode <rstrode@redhat.com> 1:4.18-15
- Remove xscreensaver-config-tool after some discussions with
  jwz.
- Take out some additional screensavers

* Wed Dec  1 2004 Ray Strode <rstrode@redhat.com> 1:4.18-14
- Add utility xscreensaver-config-tool to make changing settings
  easier (replaces the short lived xscreensaver-register-hack
  program).  Use xscreensaver-config-tool to set default settings
  instead of using patches. 
- Split up xscreensaver (fixes 121693).
- Make preferences dialog slightly more pretty
- Make lock dialog slightly more pretty

* Fri Nov 26 2004 Than Ngo <than@redhat.com> 1:4.18-13
- add patch to fix vroot bug and make xscreensaver working in KDE again.
- get rid of webcollage, which often download porn images
 
* Wed Nov 10 2004 Ray Strode <rstrode@redhat.com> 1:4.18-11
- Add xscreensaver-register-hack program to make
  installing and uninstalling screensavers easier
  (working toward fixing bug 121693 [split up screensaver])

* Wed Nov 10 2004 Ray Strode <rstrode@redhat.com> 1:4.18-10
- Get rid of unnecessary xloadimage requirement
  (bug 100641)

* Wed Nov 10 2004 Ray Strode <rstrode@redhat.com> 1:4.18-9
- Call pam_acct_mgmt() (might fix bug 137195) 

* Tue Nov 9 2004 Ray Strode <rstrode@redhat.com> 1:4.18-8
- Give vidwhacker screensaver working defaults
  (bug 64518)

* Tue Nov 9 2004 Ray Strode <rstrode@redhat.com> 1:4.18-7
- Get rid of old crufty %%{_datadir}/control-center/ tree
  (bug 114692)

* Wed Nov 3 2004 Ray Strode <rstrode@redhat.com> 1:4.18-6
- rebuild for rawhide

* Wed Nov 3 2004 Ray Strode <rstrode@redhat.com> 1:4.18-5
- Don't allow screensavers access to desktop images by default (bug #126809)
- Lock screen by default (bug #126809)

* Tue Oct 19 2004  <krh@redhat.com> 4.18-4
- Add xscreensaver-4.18-stuff-piecewise-leak.patch to stop piecewise
  from leaking (#135164).

* Wed Sep 1 2004 Ray Strode <rstrode@redhat.com> 4.18-3
- remove superfluous line in the spec file

* Wed Sep 1 2004 Ray Strode <rstrode@redhat.com> 4.18-2
- blank the screen by default

* Tue Aug 24 2004 Ray Strode <rstrode@redhat.com> 4.18-1
- update to 4.18 (fixes bug 87745).

* Sat Aug 14 2004 Ray Strode <rstrode@redhat.com> 4.16-4
- change titles of questionably named bar codes
  (fixes bug 129929).

* Fri Aug 6 2004 Ray Strode <rstrode@redhat.com> 4.16-3
- change titles of questionably named shape formations
  (fixes bug 129335).

* Wed Jun 23 2004 Ray Strode <rstrode@redhat.com> 4.16-2
- use htmlview for browsing help.

* Mon Jun 21 2004 Ray Strode <rstrode@redhat.com> 4.16-1
- update to 4.16.  Use desktop-file-install for desktop file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  5 2004 Bill Nottingham <notting@redhat.com> 4.14-5
- config tweaks

* Wed Mar 31 2004 Karsten Hopp <karsten@redhat.de> 4.14-4 
- fix fortune stand-in (#115369)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Oct 27 2003 Bill Nottingham <notting@redhat,com> 1:4.14-1
- update to 4.14

* Tue Oct  7 2003 Bill Nottingham <notting@redhat.com> 1:4.13-1
- take out flag-with-logo, don't require redhat-logos (#106046)
- update to 4.13

* Wed Aug 27 2003 Bill Nottingham <notting@redhat.com> 1:4.12-1
- update to 4.12 (fixes #101920)
- re-add BSOD to the random list

* Tue Jun 24 2003 Bill Nottingham <notting@redhat.com> 1:4.11-1
- update to 4.11

* Fri Jun 13 2003 Bill Nottingham <notting@redhat.com> 1:4.10-3
- fix some 64-bit arches (#97359)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Bill Nottingham <notting@redhat.com> 1:4.10-1
- update to 4.10

* Thu Mar 20 2003 Bill Nottingham <notting@redhat.com> 1:4.09-1
- update to 4.09, now with bouncing cows

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 1:4.07-2
- oops, xloadimage *is* needed (#83676)

* Thu Feb  6 2003 Bill Nottingham <notting@redhat.com> 1:4.07-1
- update to 4.07, fixes #76276, #75574

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1:4.06-4
- call autoconf instead of autoconf-2.53

* Mon Nov 11 2002 Bill Nottingham <notting@redhat.com> 4.06-3
- put glade tweaks back in
- switch pam package to not specify directories, to work on multilib
  arches

* Fri Nov  8 2002 Nalin Dahyabhai <nalin@redhat.com> 4.06-1
- add a BuildPrereq on bc, which configure requires
- replace use of fortune with an innocuous-and-editable stand-in script in
  %%{stand_in_path}
- define FORTUNE_PROGRAM at compile-time to force apps to use what's specified
  even if it doesn't happen to be installed at compile-time

* Sun Sep  2 2002 Bill Nottingham <notting@redhat.com> 4.05-6
- fix typo (#73246)

* Wed Aug 28 2002 Bill Nottingham <notting@redhat.com> 4.05-5
- revert to non-gtk unlock dialog
- fix translations

* Mon Aug 12 2002 Bill Nottingham <notting@redhat.com> 4.05-4
- twiddle titlebar (#67844)
- fix extraneous text (#70975)
- tweak desktop entry (#69502)

* Fri Aug 9 2002 Yu Shao <yshao@redhat.com> 4.05-3
- use GTK_IM_MODULE=gtk-im-context-simple in lock widget
- to avoid CJK IM weirdness (#70655, #68216)
- xscreensaver-rh-imcjk.patch

* Wed Jul 17 2002 Elliot Lee <sopwith@redhat.com> 4.05-2
- Add fortune-mod to buildprereq to make beehive happy
- Fix find_lang usage - install translations properly by specifying datadir

* Tue Jun 11 2002 Bill Nottingham <notting@redhat.com> 4.05-1
- update to 4.05
- use gtk2 lock widget (<jacob@ximian.com>)
- some Red Hat-ifications
- fix critical (#63916)

* Mon Jun 10 2002 Bill Nottingham <notting@redhat.com> 4.04-2
- remove no longer needed xloadimage dependency

* Mon Jun  3 2002 Bill Nottingham <notting@redhat.com> 4.04-1
- update to 4.04, gtk2 property dialog is now mainline

* Thu May 16 2002 Bill Nottingham <notting@redhat.com> 4.03-1
- update to 4.03
- use gtk2 properties dialog

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 4.01-2
- don't show screensavers that aren't available

* Sun Feb 24 2002 Bill Nottingham <notting@redhat.com>
- update to 4.01

* Mon Feb 11 2002 Bill Nottingham <notting@redhat.com>
- update to 4.00

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Aug 23 2001 Bill Nottingham <notting@redhat.com>
- fix segfault on ia64 (#52336)

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- never mind, back to 3.33 (wheeee)
- hack window-id back in for the time being
- disable memlimit so GL works

* Mon Jul 23 2001 Bill Nottingham <notting@redhat.com>
- oops, back to 3.32 for now
- remove optflags override (oops)
- add pam-devel buildprereq

* Mon Jul 16 2001 Bill Nottingham <notting@redhat.com>
- update to 3.33, fix broken last build
- fix build weirdness on some package sets (#48905)
- don't document non-existent options for forest (#49139)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue May 22 2001 Havoc Pennington <hp@redhat.com>
- putting in tree for David 

* Tue May 22 2001 David Sainty <dsainty@redhat.com>
- added DPMS options to command line help

* Sun Apr 22 2001 Bill Nottingham <notting@redhat.com>
- update to 3.32
- add patch to specify DPMS settings on the command line

* Wed Apr 11 2001 Bill Nottingham <notting@redhat.com>
- update to 3.31

* Wed Apr  4 2001 Bill Nottingham <notting@redhat.com>
- fix extrusion exclusion (#34742)

* Tue Apr  3 2001 Bill Nottingham <notting@redhat.com>
- disable GL screensavers by default (bleah)

* Mon Feb 19 2001 Bill Nottingham <notting@redhat.com>
- update to 3.29 (#27437)

* Tue Jan 23 2001 Bill Nottingham <notting@redhat.com>
- update to 3.27

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Fri Nov 10 2000 Bill Nottingham <notting@redhat.com>
- 3.26

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Wed Jul 26 2000 Bill Nottingham <notting@redhat.com>
- hey, vidmode works again

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- update to 3.25

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- xscreensaver.kss is not a %%config file.

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- tweak kss module (#11872)

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM configuration to use system-auth

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- added Red Hat screensaver (waving flag has logo now).

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- tweaks for ia64

* Mon Apr 10 2000 Bill Nottingham <notting@redhat.com>
- turn off xf86vidmode ext, so that binaries built against XFree86 4.0
  work on 3.x servers

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- turn off gnome support for now

* Mon Apr  3 2000 Bill Nottingham <notting@redhat.com>
- update to 3.24

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig entry gone.

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- update to 3.23

* Fri Jan 14 2000 Bill Nottingham <notting@redhat.com>
- rebuild to fix GL depdencies

* Tue Dec 14 1999 Bill Nottingham <notting@redhat.com>
- everyone in GL
- single package again

* Fri Dec 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.22
- turn off xf86vmode on alpha

* Tue Dec  7 1999 Bill Nottingham <notting@redhat.com>
- mmm... hardware accelerated GL on i386. :) :)

* Mon Nov 22 1999 Bill Nottingham <notting@redhat.com>
- 3.21
- use shm on alpha, let's see what breaks

* Tue Nov 16 1999 Bill Nottingham <notting@redhat.com>
- update to 3.20

* Wed Nov  3 1999 Bill Nottingham <notting@redhat.com>
- update to 3.19

* Thu Oct 14 1999 Bill Nottingham <notting@redhat.com>
- update to 3.18

* Sat Sep 25 1999 Bill Nottingham <notting@redhat.com>
- add a '-oneshot' single time lock option.

* Mon Sep 20 1999 Bill Nottingham <notting@redhat.com>
- take webcollage out of random list (for people who pay for bandwidth)

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- patch webcollage to use xloadimage
- in the random list, run petri with -size 2 to save memory
- extend RPM silliness to man pages, too.

* Mon Jul 19 1999 Bill Nottingham <notting@redhat.com>
- update to 3.17
- add a little RPM silliness to package GL stuff if it's built

* Thu Jun 24 1999 Bill Nottingham <notting@redhat.com>
- update to 3.16

* Mon May 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.12

* Tue May  4 1999 Bill Nottingham <notting@redhat.com>
- remove security problem introduced earlier

* Wed Apr 28 1999 Bill Nottingham <notting@redhat.com>
- update to 3.10

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- kill setuid the Right Way(tm)

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- fix xflame on alpha

* Mon Apr 12 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 3.09, fixes vmware interaction problems.

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- remove setuid bit. Really. I mean it.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Bill Nottingham <notting@redhat.com>
- kill setuid, since pam works OK

* Tue Mar 16 1999 Bill Nottingham <notting@redhat.com>
- update to 3.08

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- wmconfig returns, and no one is safe...

* Tue Feb 23 1999 Bill Nottingham <notting@redhat.com>
- remove bsod from random list because it's confusing people???? *sigh*

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to get it to compile cleanely on the arm

* Tue Jan  5 1999 Bill Nottingham <notting@redhat.com>
- update to 3.07

* Mon Nov 23 1998 Bill Nottingham <notting@redhat.com>
- update to 3.06

* Tue Nov 17 1998 Bill Nottingham <notting@redhat.com>
- update to 3.04

* Thu Nov 12 1998 Bill Nottingham <notting@redhat.com>
- update to 3.02
- PAMify

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- take out Noseguy module b/c of possible TMv
- install modules in /usr/X11R6/lib/xscreensaver
- don't compile support for xshm on the alpha
- properly buildrooted
- updated to version 2.34

* Fri Aug  7 1998 Bill Nottingham <notting@redhat.com>
- update to 2.27

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Mon Jun 08 1998 Erik Troan <ewt@redhat.com>
- added fix for argv0 buffer overflow

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Donnie Barnes <djb@redhat.com>
- updated from 2.10 to 2.16
- added buildroot

* Wed Oct 25 1997 Marc Ewing <marc@redhat.com>
- wmconfig

* Thu Oct 23 1997 Marc Ewing <marc@redhat.com>
- new version, configure

* Fri Aug 22 1997 Erik Troan <ewt@redhat.com>
- built against glibc

