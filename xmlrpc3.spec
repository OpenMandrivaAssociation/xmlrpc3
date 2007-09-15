# Copyright (c) 2000-2005, JPackage roject
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define mainname xmlrpc
%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Name:       xmlrpc3
Version:    3.0
Release:    %mkrel 1.4.3
Summary:    Java XML-RPC implementation
License:    Apache Software License
Group:      Development/Java
Url:        http://xml.apache.org/%{name}/
Source0:    http://www.apache.org/dist/ws/xmlrpc/sources/xmlrpc-%{version}-src.tar.gz
Source1:    %{name}-jpp-depmap.xml
# FIXME:  file this upstream
# The tests pom.xml doesn't include necessary dependencies on junit and
# servletapi
Patch0:     %{name}-addjunitandservletapitotestpom.patch
# Add OSGi MANIFEST information
Patch1:     %{name}-client-addosgimanifest.patch
Patch2:     %{name}-common-addosgimanifest.patch

# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=239123
ExcludeArch: ppc64

BuildRequires:  maven2 >= 0:2.0.4
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-eclipse
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-source
BuildRequires:  ws-jaxme
BuildRequires:  ws-commons-util
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  servletapi5
BuildRequires:  junit
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-codec >= 0:1.3
BuildRequires:  jsse
Requires:       jpackage-utils >= 0:1.6
Requires:       servletapi5
Requires:       junit
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-codec >= 1.3
Requires:       jsse
Requires:       ws-jaxme
Requires:       ws-commons-util

%if ! %{gcj_support}
Buildarch:    noarch
%endif
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
Apache XML-RPC is a Java implementation of XML-RPC, a popular protocol
that uses XML over HTTP to implement remote procedure calls.
Apache XML-RPC was previously known as Helma XML-RPC. If you have code
using the Helma library, all you should have to do is change the import
statements in your code from helma.xmlrpc.* to org.apache.xmlrpc.*.

%package javadoc
Summary:    Javadoc for %{name}
Group:      Development/Java

%description javadoc
Javadoc for %{name}.

%package common
Summary:    Common classes for XML-RPC client and server implementations
Group:      Development/Java

%description common
%{summary}.

%package common-devel
Summary:    Source for common classes of XML-RPC
Group:      Development/Java
Requires:   %{name}-common

%description common-devel
%{summary} client and server implementations.

%package client
Summary:    XML-RPC client implementation
Group:      Development/Java
Requires:   %{name}-common

%description client
%{summary}.

%package client-devel
Summary:    Source for XML-RPC client implementation
Group:      Development/Java
Requires:   %{name}-client

%description client-devel
%{summary}.

%package server
Summary:    Javadoc for %{name}
Group:      Development/Java
Requires:   %{name}-common

%description server
%{summary}.

%package server-devel
Summary:    Source for XML-RPC server implementation
Group:      Development/Java
Requires:   %{name}-server

%description server-devel
%{summary}.

%prep
%setup -q -n %{mainname}-%{version}
%patch0
cp %{SOURCE1} .
pushd client
%patch1
popd
pushd common
%patch2
popd

%build
%{__perl} -pi -e 's/\r$//g' LICENSE.txt
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
# The java.home is due to java-gcj and libgcj weirdness on 64-bit
# systems
mvn-jpp \
  -e \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  -Djava.home=%{_jvmdir}/java/jre \
  -Dmaven2.jpp.depmap.file=%{SOURCE1} \
  -Dmaven.test.failure.ignore=true \
  install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 client/target/%{mainname}-client-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-client-%{version}.jar
install -m 644 server/target/%{mainname}-server-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-server-%{version}.jar
install -m 644 common/target/%{mainname}-common-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-common-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# sources jars
install -m 644 client/target/%{mainname}-client-%{version}-sources.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-client-%{version}-sources.jar
install -m 644 server/target/%{mainname}-server-%{version}-sources.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-server-%{version}-sources.jar
install -m 644 common/target/%{mainname}-common-%{version}-sources.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-common-%{version}-sources.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}

%files common
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/%{name}-common.jar
%{_javadir}/%{name}-common-%{version}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-common*
%endif

%files common-devel
%defattr(-,root,root,-)
%{_javadir}/%{name}-common-%{version}-sources.jar

%files client
%defattr(-,root,root,-)
%{_javadir}/%{name}-client.jar
%{_javadir}/%{name}-client-%{version}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-client*
%endif

%files client-devel
%defattr(-,root,root,-)
%{_javadir}/%{name}-client-%{version}-sources.jar

%files server
%defattr(-,root,root,-)
%{_javadir}/%{name}-server.jar
%{_javadir}/%{name}-server-%{version}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-server*
%endif

%files server-devel
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-server-%{version}-sources.jar
