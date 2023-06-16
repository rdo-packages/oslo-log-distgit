%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

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

License:        Apache-2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
%if "%{version}" == "4.6.1"
# TODO(jcapitao): patch to be removed once https://review.opendev.org/c/openstack/oslo.log/+/828017
# is available in uc tag.
Patch0001:      0001-Use-project-when-logging-the-user-identity.patch
%endif
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo Log library
Obsoletes: python2-%{pkg_name} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:  git-core
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Log handling library

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Log handling library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo Log handling library

Requires:       python3-%{pkg_name} = %{version}-%{release}
%description -n python3-%{pkg_name}-tests
%{common_desc1}

%description
%{common_desc}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo log library

%description -n python-%{pkg_name}-lang
Translation files for Oslo log library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-knwon BRs
for pkg in %{excluded_brs};do
sed -i /^${pkg}.*/d doc/requirements.txt
sed -i /^${pkg}.*/d test-requirements.txt
done
# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_log/locale --domain oslo_log

ln -s ./convert-json %{buildroot}%{_bindir}/convert-json-3

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_log/locale/*/LC_*/oslo_log*po
rm -f %{buildroot}%{python3_sitelib}/oslo_log/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_log/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_log --all-name

%check
python3 setup.py test

%files -n python3-%{pkg_name}
%doc README.rst ChangeLog AUTHORS
%license LICENSE
%{python3_sitelib}/oslo_log
%{python3_sitelib}/*.dist-info
%{_bindir}/convert-json
%{_bindir}/convert-json-3
%exclude %{python3_sitelib}/oslo_log/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_log/tests

%files -n python-%{pkg_name}-lang -f oslo_log.lang
%license LICENSE

%changelog
