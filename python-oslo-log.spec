%{!?_licensedir:%global license %%doc}
%global pypi_name oslo.log

Name:           python-oslo-log
Version:        1.11.0
Release:        2%{?dist}
Summary:        OpenStack Oslo Log library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       python-babel
Requires:       python-six >= 1.9.0
Requires:       python-iso8601
Requires:       python-oslo-config
Requires:       python-oslo-context
Requires:       python-oslo-i18n
Requires:       python-oslo-utils
Requires:       python-oslo-serialization
Requires:       python-debtcollector

%description
OpenStack logging configuration library provides standardized configuration
for all openstack projects. It also provides custom formatters, handlers and
support for context specific logging (like resource id’s etc).

%package doc
Summary:    Documentation for the Oslo Log handling library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-context

%description doc
Documentation for the Oslo Log handling library.


%prep
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -f requirements.txt


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc README.rst ChangeLog AUTHORS
%license LICENSE
%{python2_sitelib}/oslo_log
%{python2_sitelib}/*.egg-info

%files doc
%doc html
%license LICENSE

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 18 2015 Alan Pevec <alan.pevec@redhat.com> 1.11.0-1
- Update to upstream 1.11.0

* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 1.10.0-1
- Update to upstream 1.10.0

* Wed Aug 05 2015 Alan Pevec <alan.pevec@redhat.com> 1.8.0-1
- Update to upstream 1.8.0

* Mon Jun 29 2015 Alan Pevec <alan.pevec@redhat.com> 1.5.0-1
- Update to upstream 1.5.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-1
- Upstream 1.0.0
- Based on Derek Higgins spec from Delorean

