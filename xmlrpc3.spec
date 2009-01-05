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
%define with()          %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%define without()       %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%define bcond_with()    %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}

%bcond_with             maven

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section free
%define oname xmlrpc

Name:           xmlrpc3
Version:        3.1
Release:        %mkrel 1
Epoch:          0
Summary:        Java XML-RPC implementation
License:        ASL 2.0
Group:          Development/Java
URL:            http://ws.apache.org/xmlrpc/
Source0:        http://www.apache.org/dist/ws/xmlrpc/sources/xmlrpc-3.1-src.tar.gz
Source1:        xmlrpc-settings.xml
Source2:        xmlrpc-jpp-depmap.xml
Source3:        xmlrpc-build.xml
Source4:        xmlrpc-client-build.xml
Source5:        xmlrpc-common-build.xml
Source6:        xmlrpc-server-build.xml
Source7:        xmlrpc-tests-build.xml
Patch0:         xmlrpc-pom_xml.patch
Patch1:         xmlrpc-tests-pom_xml.patch
Patch2:         xmlrpc-site_xml.patch
Patch3:         xmlrpc3-client-addosgimanifest2.patch
Patch4:         xmlrpc3-common-addosgimanifest2.patch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  jakarta-commons-codec
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-logging
BuildRequires:  servletapi5
BuildRequires:  ws-commons-util
BuildRequires:  ws-jaxme
BuildRequires:  xml-commons-jaxp-1.3-apis
%if %with maven
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-eclipse
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-source
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven-release
%endif
Requires:       jakarta-commons-codec
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-logging
Requires:       servletapi5
Requires:       ws-commons-util
Requires:       ws-jaxme
Requires:       xml-commons-jaxp-1.3-apis
Requires(post): jpackage-utils >= 0:1.7.2
Requires(postun): jpackage-utils >= 0:1.7.2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
Buildarch:      noarch
%endif

# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=239123
ExcludeArch: ppc64

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

%package client
Summary:    XML-RPC client implementation
Group:      Development/Java
Requires:   %{name}-common

%description client
%{summary}.

%package server
Summary:    Javadoc for %{name}
Group:      Development/Java
Requires:   %{name}-common

%description server
%{summary}.

%prep
%setup -q -n xmlrpc-%{version}
cp -p %{SOURCE1} settings.xml
cp -p %{SOURCE3} build.xml
cp -p %{SOURCE4} client/build.xml
cp -p %{SOURCE5} common/build.xml
cp -p %{SOURCE6} server/build.xml
cp -p %{SOURCE7} tests/build.xml
%if 0
%patch0 -p0
%patch1 -p0
%patch2 -p0
%endif
pushd client
%patch3 -p1
popd
pushd common
%patch4 -p1
popd

perl -pi -e 's/\r$//g' LICENSE.txt

%build
%if %with maven
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mkdir common/src/site
cp src/site/site.xml common/src/site
mkdir client/src/site
cp src/site/site.xml client/src/site
mkdir server/src/site
cp src/site/site.xml server/src/site
mkdir tests/src/site
cp src/site/site.xml tests/src/site
mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc site:site

%else
pushd common
export CLASSPATH=$(build-classpath ws-commons-java5 ws-commons-util jaxme/jaxmeapi xml-commons-jaxp-1.3-apis)
export OPT_JAR_LIST=:
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd client
export CLASSPATH=$(build-classpath ws-commons-java5 ws-commons-util commons-httpclient xml-commons-jaxp-1.3-apis)
CLASSPATH=$CLASSPATH:../common/target/%{oname}-common-%{version}.jar
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd server
export CLASSPATH=$(build-classpath commons-logging ws-commons-java5 ws-commons-util servletapi5 xml-commons-jaxp-1.3-apis)
CLASSPATH=$CLASSPATH:../common/target/%{oname}-common-%{version}.jar
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd tests
export CLASSPATH=$(build-classpath commons-logging commons-codec commons-httpclient ws-commons-util servletapi5 xml-commons-jaxp-1.3-apis)
CLASSPATH=$CLASSPATH:../common/target/%{oname}-common-%{version}.jar
CLASSPATH=$CLASSPATH:../client/target/%{oname}-client-%{version}.jar
CLASSPATH=$CLASSPATH:../server/target/%{oname}-server-%{version}.jar
CLASSPATH=$CLASSPATH:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

%endif
mkdir -p temp
pushd temp
%{jar} xf ../server/target/%{oname}-server-%{version}.jar
%{jar} xf ../client/target/%{oname}-client-%{version}.jar
%{jar} xf ../common/target/%{oname}-common-%{version}.jar
%{__sed} -i -e "s|-common||g" META-INF/MANIFEST.MF
%{jar} cmf META-INF/MANIFEST.MF ../%{oname}-%{version}.jar *
popd

%install
rm -rf $RPM_BUILD_ROOT

# jars
#install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
#install -m 644 %{oname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
#install -m 644 common/target/%{oname}-common-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/common-%{version}.jar
#install -m 644 client/target/%{oname}-client-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/client-%{version}.jar
#install -m 644 server/target/%{oname}-server-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/server-%{version}.jar
#install -m 644 tests/target/%{oname}-tests-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/tests-%{version}.jar
##############################################################################################
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 %{oname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 client/target/%{oname}-client-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-client-%{version}.jar
install -m 644 server/target/%{oname}-server-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-server-%{version}.jar
install -m 644 common/target/%{oname}-common-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-common-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

%add_to_maven_depmap org.apache.xmlrpc3 xmlrpc %{version} JPP %{name}
%add_to_maven_depmap org.apache.xmlrpc3 xmlrpc-client %{version} JPP/%{name} client
%add_to_maven_depmap org.apache.xmlrpc3 xmlrpc-common %{version} JPP/%{name} common
%add_to_maven_depmap org.apache.xmlrpc3 xmlrpc-server %{version} JPP/%{name} server
%add_to_maven_depmap org.apache.xmlrpc3 xmlrpc-tests %{version} JPP/%{name} tests

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
install -m 644 client/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-client.pom
install -m 644 common/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-common.pom
install -m 644 server/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-server.pom
install -m 644 tests/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-tests.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %with maven
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
for m in common client server tests; do
    install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/$m
    cp -pr $m/target/site/apidocs/* \
                      $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/$m
done
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %with maven
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# FIXME: (dwalluck): breaks -bi --short-circuit
rm -rf target/site/apidocs
cp -pr target/site $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
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
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*
%{_javadir}/%{name}-common.jar
%{_javadir}/%{name}-common-%{version}.jar
%{_javadir}/%{name}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-common*
%endif

%files client
%defattr(-,root,root,-)
%{_javadir}/%{name}-client.jar
%{_javadir}/%{name}-client-%{version}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-client*
%endif

%files server
%defattr(-,root,root,-)
%{_javadir}/%{name}-server.jar
%{_javadir}/%{name}-server-%{version}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-server*
%endif
