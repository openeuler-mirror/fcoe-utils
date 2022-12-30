Name:               fcoe-utils
Version:            1.0.33
Release:            5
Summary:            Fibre Channel over Ethernet utilities
License:            GPLv2
URL:                https://github.com/morbidrsa/fcoe-utils
Source0:            https://github.com/morbidrsa/fcoe-utils/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:            quickstart.txt
Patch0:             backport-00-Revert_Make_gcc_compiler_happy_about_ifname_string.patch 
Patch1:             backport-01-fix_VLAN_device_name_overflow_check.patch 
Patch2:             backport-02-string_op_truncation_format_trauncation.patch     
Patch3:             backport-03-use-of-uninitialized-values-detected-during-LTO.patch
#This patch refer to ubuntu's version
Patch4:             backport-Fix-build-error-to-change-char-type.patch
Patch5:             backport-handle-NIC-names-longer-than-7-characters.patch           
Patch6:             bachport-Fix-GCC-12-warning.patch

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
install -d %{buildroot}%{_libexecdir}/fcoe
for file in contrib/*.sh debug/*sh
    do install -m 755 ${file} %{buildroot}%{_libexecdir}/fcoe/
done

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
%config(noreplace) %{_sysconfdir}/fcoe/config
%{_unitdir}/fcoe.service
%{_unitdir}/fcoemon.socket
%{_sbindir}/*
%{_datadir}/bash-completion/completions/*
%{_libexecdir}/fcoe/

%files help
%defattr(-,root,root)
%doc README quickstart.txt QUICKSTART
%{_mandir}/man8/*

%changelog
* Fri Dec 30 2022 xulei <xulei@xfusion.com> - 1.0.33-5
- Backport upstream patch to fix GCC 12 warning.

* Thu Dec 29 2022 xulei <xulei@xfusion.com> - 1.0.33-4
- Backport upstream patch to handle NIC names lognger than 7 characters

* Wed Mar 03 2022 xu_ping <xuping33@huawei.com> - 1.0.33-3
- Backport upstream patch to avoid non-X86 build break.

* Wed Aug 25 2021 sunguoshuai <sunguoshuai@huawei.com> - 1.0.33-2
- Fix fcoe.service start error

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

