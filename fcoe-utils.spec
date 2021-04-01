Name:               fcoe-utils
Version:            1.0.33
Release:            1
Summary:            Fibre Channel over Ethernet utilities
License:            GPLv2
URL:                https://github.com/morbidrsa/fcoe-utils
Source0:            https://github.com/morbidrsa/fcoe-utils/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:            quickstart.txt
Source2:            fcoe.service
Source3:            fcoe.config
Patch0:             backport-00-Revert_Make_gcc_compiler_happy_about_ifname_string.patch 
Patch1:             backport-01-fix_VLAN_device_name_overflow_check.patch 
Patch2:             backport-02-string_op_truncation_format_trauncation.patch     
Patch3:             backport-03-use-of-uninitialized-values-detected-during-LTO.patch
#This patch refer to ubuntu's version


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
%{_datadir}/bash-completion/completions/*
%{_libexecdir}/fcoe/

%files help
%defattr(-,root,root)
%doc README quickstart.txt QUICKSTART
%{_mandir}/man8/*

%changelog
* Tue Mar 30 2021 lijingyuan <lijingyuan@huawei.com> - 1.0.33-1
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update fcoe-utils-1.0.32 to fcoe-utils-1.0.33

* Tue Dec 15 2020 xihaochen <xihaochen@huawei.com> - 1.0.32-9
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update url

* Tue Jun 23 2020 gaihuiying <gaihuiying1@huawei.com> - 1.0.32-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix build error with gcc9 about strncpy

* Fri Oct 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.32-7
- Package init

