#
# $Id$
#
%define DBVer		1.75.2
Summary:	Debian apt tools for Mandriva
Name:		apt-mdv
Version:	0.8.9
Release:	%mkrel 1
License:	GPL
Group:		System/Configuration/Packaging
Url:		http://ftp.de.debian.org/debian/pool/main/a/apt/
Source:		http://ftp.de.debian.org/debian/pool/main/a/apt/apt_%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
Requires:	bzip2, gnupg
BuildRequires:	libtool-base,docbook-style-xsl = %{DBVer},libcurl-devel,dpkg
Conflicts:	apt 

%description
Provides tools useful to manage a Debian repository on a Mandriva distribution (apt-ftparchive e.g.)

%prep
%setup -q -n apt-%{version}

%build
# Wrong links upstream
ln -sf /usr/share/libtool/config/config.guess buildlib/
ln -sf /usr/share/libtool/config/config.sub buildlib
# As no DebianDoc is available yet, remove xml doc build
perl -pi -e 's/^\[type: docbook\]/#[type: docbook]/' doc/po4a.conf
perl -pi -e 's/^\[type: sgml\]/#[type: sgml]/' doc/po4a.conf
perl -pi -e 's|/usr/share/xml/docbook/stylesheet/nwalsh/manpages/docbook.xsl|/usr/share/sgml/docbook/xsl-stylesheets-%{DBVer}/manpages/docbook.xsl|' doc/manpage-style.xsl
./configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p  $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_mandir}/man8 $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_mandir}/man5
cp -a bin/apt-* $RPM_BUILD_ROOT%{_bindir}
cp -a bin/lib* $RPM_BUILD_ROOT%{_libdir}
cp -a doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -a doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/lib*
%{_bindir}/*

%changelog
