# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1
%global pypi_name oslo.log
%global pkg_name oslo-log

%global common_desc \
OpenStack logging configuration library provides standardized configuration \
for all openstack projects. It also provides custom formatters, handlers and \
support for context specific logging (like resource id’s etc).

%global common_desc1 \
Tests for the Oslo Log handling library.

Name:           python-oslo-log
Version:        XXX
Release:        XXX
Summary:        OpenStack Oslo Log library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n python%{pyver}-%{pkg_name}
Summary:        OpenStack Oslo Log library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pkg_name} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git
# Required for tests
BuildRequires:  python%{pyver}-dateutil
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-context
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
# Required to compile translation files
BuildRequires:  python%{pyver}-babel
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-inotify
%else
BuildRequires:  python%{pyver}-inotify
%endif

Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-dateutil
Requires:       python%{pyver}-six >= 1.11.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-context >= 2.20.0
Requires:       python%{pyver}-oslo-i18n >= 3.20.0
Requires:       python%{pyver}-oslo-utils >= 3.36.0
Requires:       python%{pyver}-oslo-serialization >= 2.25.0
Requires:       python%{pyver}-debtcollector >= 1.19.0
Requires:       python%{pyver}-monotonic >= 1.4
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-inotify
%else
Requires:       python%{pyver}-inotify
%endif

Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Log handling library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-utils

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Log handling library.
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Tests for the Oslo Log handling library

Requires:       python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-testrepository
Requires:       python%{pyver}-testscenarios

%description -n python%{pyver}-%{pkg_name}-tests
%{common_desc1}

%description
%{common_desc}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo log library

%description -n python-%{pkg_name}-lang
Translation files for Oslo log library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
PYTHONPATH=. sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_log/locale

%install
%{pyver_install}
ln -s ./convert-json %{buildroot}%{_bindir}/convert-json-%{pyver}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_log/locale/*/LC_*/oslo_log*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_log/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_log/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_log --all-name

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{pkg_name}
%doc README.rst ChangeLog AUTHORS
%license LICENSE
%{pyver_sitelib}/oslo_log
%{pyver_sitelib}/*.egg-info
%{_bindir}/convert-json
%{_bindir}/convert-json-%{pyver}
%exclude %{pyver_sitelib}/oslo_log/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_log/tests

%files -n python-%{pkg_name}-lang -f oslo_log.lang
%license LICENSE

%changelog
