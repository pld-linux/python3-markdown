%define 	module	Markdown
Summary:	Python implementation of Markdown.
Name:		python-%{module}
Version:	2.0.3
Release:	2
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/M/Markdown/%{module}-%{version}.tar.gz
# Source0-md5:	751e8055be2433dfd1a82e0fb1b12f13
URL:		http://www.freewisdom.org/projects/python-markdown
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python implementation of John Gruber's Markdown. It is almost
completely compliant with the reference implementation.

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
%attr(755,root,root) %{_bindir}/markdown
%{py_sitescriptdir}/markdown
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/*.egg-info
%endif
