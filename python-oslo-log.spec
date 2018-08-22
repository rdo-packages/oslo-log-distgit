%if 0%{?fedora} >= 24
%global with_python3 1
%endif

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

%package -n python2-%{pkg_name}
Summary:        OpenStack Oslo Log library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  git
# Required for tests
BuildRequires:  python2-dateutil
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-context
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-subunit
BuildRequires:  python2-testtools
# Required to compile translation files
BuildRequires:  python2-babel
%if 0%{?fedora} > 0
BuildRequires:  python2-inotify
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
%else
BuildRequires:  python-inotify
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
%endif

Requires:       python2-pbr
Requires:       python2-dateutil
Requires:       python2-six >= 1.10.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-context >= 2.19.2
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-debtcollector >= 1.2.0
%if 0%{?fedora} > 0
Requires:       python2-inotify
Requires:       python2-monotonic
%else
Requires:       python-inotify
Requires:       python-monotonic
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Log handling library

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-utils

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Log handling library.
%endif

%package -n python2-%{pkg_name}-tests
Summary:    Tests for the Oslo Log handling library

Requires:       python2-%{pkg_name} = %{version}-%{release}
Requires:       python2-mock
Requires:       python2-oslotest
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-subunit
Requires:       python2-testtools
%if 0%{?fedora} > 0
Requires:       python2-testrepository
Requires:       python2-testscenarios
%else
Requires:       python-testrepository
Requires:       python-testscenarios
%endif

%description -n python2-%{pkg_name}-tests
%{common_desc1}

%if 0%{?with_python3}
%package -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo Log handling library

Requires:       python3-%{pkg_name} = %{version}-%{release}
Requires:       python3-mock
Requires:       python3-oslotest
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-subunit
Requires:       python3-testrepository
Requires:       python3-testscenarios
Requires:       python3-testtools

%description -n python3-%{pkg_name}-tests
%{common_desc1}
%endif

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo Log library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Required for tests
BuildRequires:  python3-dateutil
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-inotify

Requires:       python3-pbr
Requires:       python3-dateutil
Requires:       python3-monotonic
Requires:       python3-six >= 1.10.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-context >= 2.19.2
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-debtcollector
Requires:       python3-inotify
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
Oslo concurrency library has utilities for safely running multi-thread,
multi-process applications using locking mechanisms and for running
external processes.
%endif

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_log/locale

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/convert-json %{buildroot}%{_bindir}/convert-json-%{python3_version}
ln -s ./convert-json-%{python3_version} %{buildroot}%{_bindir}/convert-json-3
%endif
%py2_install
ln -s ./convert-json %{buildroot}%{_bindir}/convert-json-2
ln -s ./convert-json %{buildroot}%{_bindir}/convert-json-%{python2_version}


# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_log/locale/*/LC_*/oslo_log*po
rm -f %{buildroot}%{python2_sitelib}/oslo_log/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_log/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_log/locale
%endif

# Find language files
%find_lang oslo_log --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%doc README.rst ChangeLog AUTHORS
%license LICENSE
%{python2_sitelib}/oslo_log
%{python2_sitelib}/*.egg-info
%{_bindir}/convert-json
%{_bindir}/convert-json-2
%{_bindir}/convert-json-%{python2_version}
%exclude %{python2_sitelib}/oslo_log/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_log/tests

%files -n python-%{pkg_name}-lang -f oslo_log.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst ChangeLog AUTHORS
%license LICENSE
%{python3_sitelib}/oslo_log
%{python3_sitelib}/*.egg-info
%{_bindir}/convert-json-3
%{_bindir}/convert-json-%{python3_version}
%exclude %{python3_sitelib}/oslo_log/tests
%endif

%if 0%{?with_python3}
%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_log/tests
%endif


%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/oslo.log/commit/?id=e7747eff1f5b5c04bfcc82e6c3325a6ca001cdd5
