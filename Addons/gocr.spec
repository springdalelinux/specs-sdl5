Name:           gocr
Version:        0.44
Release:        2%{?dist}
Summary:        GNU Optical Character Recognition program

Group:          Applications/Multimedia
License:        GPL
URL:            http://jocr.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/jocr/gocr-%{version}.tar.gz
Patch0:         gocr-0.44-man.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  netpbm-devel
# Needed for conversion programs
Requires:       gzip, bzip2, libjpeg, netpbm-progs, transfig

%description
GOCR is an OCR (Optical Character Recognition) program, developed under the
GNU Public License. It converts scanned images of text back to text files.
Joerg Schulenburg started the program, and now leads a team of developers.

GOCR can be used with different front-ends, which makes it very easy to port
to different OSes and architectures. It can open many different image
formats, and its quality have been improving in a daily basis.


%prep
%setup -q
%patch -p1 -b .man


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# Don't ship static library
rm -rf $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}
# Don't ship buggy Tcl/Tk frontend
rm $RPM_BUILD_ROOT/%{_bindir}/gocr.tcl


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS CREDITS doc/gocr.html gpl.html HISTORY README
%doc REMARK.txt REVIEW TODO
%lang(de) %doc READMEde.txt
%{_bindir}/gocr
%{_mandir}/man1/gocr.1*


%changelog
* Wed Mar 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.44-2
- Bump release to fix import tag issue

* Fri Mar 02 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.44-1
- Update to 0.44

* Mon Dec 18 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.43-1
- Update to 0.43
- Don't ship frontends

* Wed Nov 22 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.41-3
- Add more requires

* Tue Nov 21 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.41-2
- Split TCL/Tk GUI into -tk sub-package
- Ship GTK+ GUI

* Mon Nov 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.41-1
- Initial Fedora Extras Version
