Name:               fcoe-utils
Version:            1.0.34
Release:            1
Summary:            Fibre Channel over Ethernet utilities
License:            GPLv2
URL:                https://github.com/morbidrsa/fcoe-utils
Source0:            https://github.com/openSUSE/fcoe-utils/archive/v{version}/%{name}-%{version}.tar.gz
Source1:            quickstart.txt
#This patch refer to ubuntu's version
Patch1:             0001-Fix-GCC-12-warning.patch
Patch2:             0001-fcoemon-add-snprintf-string-precision-modifiers-in-f.patch

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
%if "%toolchain" == "clang"
    CFLAGS="$CFLAGS -Wno-error=format-nonliteral -Wno-error=strncat-size -Wno-error=strict-prototypes"
%endif

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
* Sat Oct 07 2023 xu_ping <707078654@qq.com> - 1.0.34-1
- Upgrade version to 1.0.34

* Thu Aug 24 2023 Xiaoya Huang <huangxiaoya@iscas.ac.cn> - 1.0.33-5
- Fix clang build error

* Fri Jul 14 2023 chenchen <chen_aka_jan@163.com> - 1.0.33-4
- fix build error caused by upgrading gcc to 12.3.0 

* Thu Mar 03 2022 xu_ping <xuping33@huawei.com> - 1.0.33-3
- Backport upstream patch to avoid non-X86 build break.

* Wed Aug 2021 sunguoshuai <sunguoshuai@huawei.com> - 1.0.33-2
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

