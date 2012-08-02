%define 	module	Markdown
Summary:	Python implementation of Markdown
Name:		python-%{module}
Version:	2.2.0
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/M/Markdown/%{module}-%{version}.tar.gz
# Source0-md5:	28dd4f54894b3af2615b08f50d2ce4bf
URL:		http://packages.python.org/Markdown/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules >= 2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs
%attr(755,root,root) %{_bindir}/markdown_py
%{py_sitescriptdir}/markdown
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/*.egg-info
%endif
