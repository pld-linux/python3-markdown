#
# Conditional build:
%bcond_with	doc	# documentation
%bcond_without	tests	# unit tests
%bcond_without	python2	# python2 package
%bcond_without	python3	# python3 package

%define 	module	markdown
Summary:	Markdown implementation in Python 2
Summary(pl.UTF-8):	Implementacja formatu Markdown w Pythonie 2
Name:		python-%{module}
Version:	3.1.1
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/markdown/
Source0:	https://files.pythonhosted.org/packages/source/M/Markdown/Markdown-%{version}.tar.gz
# Source0-md5:	d84732ecc65b3a1bff693d9d4c24277f
URL:		https://pypi.org/project/markdown/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-elementtree
BuildRequires:	python-setuptools >= 36
%if %{with tests}
BuildRequires:	python-PyYAML
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 36
%if %{with tests}
BuildRequires:	python3-PyYAML
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-elementtree
Provides:	python-Markdown = %{version}-%{release}
Obsoletes:	python-Markdown < 2.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python 2 implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%description -l pl.UTF-8
Ten pakiet zawiera implementację formatu Markdown Johna Grubera w
Pythonie 2. Jest prawie całkowicie zgodna z implementacją wzorcową,
choć jest kilka znanych problemów.

%package -n python3-markdown
Summary:	Markdown implementation in Python 3
Summary(pl.UTF-8):	Implementacja formatu Markdown w Pythonie 3
Group:		Development/Languages/Python

%description -n python3-markdown
This is a Python 3 implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%description -n python3-markdown -l pl.UTF-8
Ten pakiet zawiera implementację formatu Markdown Johna Grubera w
Pythonie 3. Jest prawie całkowicie zgodna z implementacją wzorcową,
choć jest kilka znanych problemów.

%prep
%setup -q -n Markdown-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover tests
%endif
%endif

%if %{with doc}
mkdocs
mkdocs_nature
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
# rename binary
%{__mv} $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py_ver}}
%endif

%if %{with python3}
%py3_install
# rename binary
%{__mv} $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py3_ver}}
# default binary
ln -s markdown_py-%{py3_ver} $RPM_BUILD_ROOT%{_bindir}/markdown_py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md docs/{change_log,extensions,authors.md,cli.md,favicon.ico,index.md,py.png,reference.md}
%attr(755,root,root) %{_bindir}/markdown_py-%{py_ver}
%{py_sitescriptdir}/markdown
%{py_sitescriptdir}/Markdown-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-markdown
%defattr(644,root,root,755)
%doc LICENSE.md README.md docs/{change_log,extensions,authors.md,cli.md,favicon.ico,index.md,py.png,reference.md}
%attr(755,root,root) %{_bindir}/markdown_py
%attr(755,root,root) %{_bindir}/markdown_py-%{py3_ver}
%{py3_sitescriptdir}/markdown
%{py3_sitescriptdir}/Markdown-%{version}-py*.egg-info
%endif
