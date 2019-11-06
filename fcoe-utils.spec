Name:               fcoe-utils
Version:            1.0.32
Release:            7
Summary:            Fibre Channel over Ethernet utilities
License:            GPLv2
URL:                https://www.open-fcoe.org
Source0:            https://github.com/morbidrsa/fcoe-utils/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:            quickstart.txt
Source2:            fcoe.service
Source3:            fcoe.config
Patch0:             fcoe-utils-gcc7-fmt-truc-err.patch
Patch1:             fcoe-utils-gcc8-fmt-truc-err.patch

BuildRequires:      autoconf automake libpciaccess-devel libtool lldpad-devel systemd
Requires:           lldpad iproute device-mapper-multipath
%{?systemd_requires}

%description
Fibre Channel over Ethernet utilities
fcoeadm - command line tool for configuring FCoE interfaces
fcoemon - service to configure DCB Ethernet QOS filters, works with lldpad

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
cp -v %{SOURCE1} quickstart.txt

%build
./bootstrap.sh
%configure
%make_build

%install
%make_install
rm -rf %{buildroot}/etc/init.d
install -d %{buildroot}%{_sysconfdir}/sysconfig %{buildroot}%{_unitdir}
rm -f %{buildroot}%{_unitdir}/*
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/fcoe
install -d %{buildroot}%{_libexecdir}/fcoe
for file in contrib/*.sh debug/*sh
    do install -m 755 ${file} %{buildroot}%{_libexecdir}/fcoe/
done
rm -f %{buildroot}/%{_sysconfdir}/fcoe/config

%post
%systemd_post fcoe.service

%preun
%systemd_preun fcoe.service

%postun
%systemd_postun_with_restart fcoe.service

%files
%defattr(-,root,root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/fcoe/cfg-ethx
%config(noreplace) %{_sysconfdir}/sysconfig/fcoe
%{_unitdir}/fcoe.service
%{_sbindir}/*
%{_sysconfdir}/bash_completion.d/*
%{_libexecdir}/fcoe/

%files help
%defattr(-,root,root)
%doc README quickstart.txt QUICKSTART
%{_mandir}/man8/*

%changelog
* Fri Oct 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.32-7
- Package init

