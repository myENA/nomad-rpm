## package settings
%define nomad_home     %{_localstatedir}/lib/nomad
%define nomad_confdir  %{_sysconfdir}/nomad.d
%define debug_package  %{nil}
%define version_suffix %{nil}

Name:           nomad
Version:        0.9.0
Release:        2%{?dist}
Summary:        Flexible, enterprise-grade cluster scheduler.

Group:          System Environment/Daemons
License:        Mozilla Public License, version 2.0
URL:            https://www.nomadproject.io

Source0:        https://releases.hashicorp.com/%{name}/%{version}%{version_suffix}/%{name}_%{version}%{version_suffix}_linux_amd64.zip
Source2:        %{name}.service
Source3:        %{name}.sysconfig

BuildRequires:  systemd-units

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Nomad is a flexible, enterprise-grade cluster scheduler designed to easily integrate into existing workflows.
Nomad can run a diverse workload of micro-service, batch, containerized and non-containerized applications.

%package config
Summary:    Configuration files for %{name}
Group:      System Environment/Daemons
Requires:   nomad

%description config
Example configuration for %{name}.

%prep
%setup -q -c

%build

%install
## directories
%{__install} -d -m 0750 %{buildroot}%{nomad_home}/alloc
%{__install} -d -m 0750 %{buildroot}%{nomad_home}/client
%{__install} -d -m 0750 %{buildroot}%{nomad_home}/server

## sytem files
%{__install} -p -D -m 0640 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

## client configuration
for svc in %{_sourcedir}/nomad-client-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{nomad_confdir}/client/$(echo $(basename $svc)|sed s/nomad-client-//)
done

## server configuration
for svc in %{_sourcedir}/nomad-server-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{nomad_confdir}/server/$(echo $(basename $svc)|sed s/nomad-server-//)
done

## common configuration
for svc in %{_sourcedir}/nomad-common-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{nomad_confdir}/client/$(echo $(basename $svc)|sed s/nomad-common-//)
	%{__install} -p -D -m 0644 $svc %{buildroot}%{nomad_confdir}/server/$(echo $(basename $svc)|sed s/nomad-common-//)
done

## main binary
%{__install} -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%pre

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%dir %{nomad_home}/alloc
%dir %{nomad_home}/client
%dir %{nomad_home}/server

%files config
%defattr(0644,root,root,0755)
%dir %{nomad_confdir}/client
%dir %{nomad_confdir}/server
%config(noreplace) %{nomad_confdir}/client/*
%config(noreplace) %{nomad_confdir}/server/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
