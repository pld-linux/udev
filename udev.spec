Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	0.2
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev-0.2.tar.bz2
# Source0-md5:	c63d4482cbaa074f937661486e9f2030
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	hotplug >= 2003_08_05
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u¿ytkownika dla j±der 2.5 i
wy¿szych.

%prep
%setup -q

%build
%{__make} -C libsysfs \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -ansi"

%{__make} \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}"

sed -i -e 's#/udev/#/dev/#g' udev.h
sed -i -e 's#/home/greg/src/udev/#/etc/udev/#g' namedev.h

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_sysconfdir}/{udev,hotplug.d/default}}

install udev $RPM_BUILD_ROOT%{_sbindir}
install namedev.config namedev.permissions $RPM_BUILD_ROOT%{_sysconfdir}/udev

ln -s /sbin/udev $RPM_BUILD_ROOT/etc/hotplug.d/default/udev.hotplug

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog docs/*
%attr(750,root,root) %dir /etc/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
