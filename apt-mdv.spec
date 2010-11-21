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
BuildRequires:	libtool,docbook-style-xsl = %{DBVer}
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
mkdir -p  $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/usr/lib64 $RPM_BUILD_ROOT/usr/share/man/man8 $RPM_BUILD_ROOT/usr/share/man/man1 $RPM_BUILD_ROOT/usr/share/man/man5
cp -a bin/apt-* $RPM_BUILD_ROOT/usr/bin
%ifarch x86_64
cp -a bin/lib* $RPM_BUILD_ROOT/usr/lib64
%else
cp -a bin/lib* $RPM_BUILD_ROOT/usr/lib
%endif
cp -a doc/*.8 $RPM_BUILD_ROOT/usr/share/man/man8
cp -a doc/*.1 $RPM_BUILD_ROOT/usr/share/man/man1
cp -a doc/*.5 $RPM_BUILD_ROOT/usr/share/man/man5

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
