#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# install-ca-cert.sh
#
# Installs the custom CA / self-signed certificate found at
# docker/ssl/server.pem into the container's system trust store so that
# uv, pip, Python's ssl module, curl, and all other tools that rely on
# the system CA bundle will trust it.
#
# Must be invoked before any network activity (package installs, DB
# connections, SMTP connections) — docker-compose-ssl.yml does this by
# prepending this script to every service command.
#
# update-ca-certificates requires a .crt extension; it safely ignores
# any PRIVATE KEY block inside a combined PEM file.

set -eo pipefail

CA_CERT="/app/docker/ssl/server.pem"
CA_DEST="/usr/local/share/ca-certificates/superset-ca.crt"

if [ -f "$CA_CERT" ]; then
    echo "==> Installing custom CA certificate from $CA_CERT"
    cp "$CA_CERT" "$CA_DEST"
    update-ca-certificates --fresh 2>&1 | grep -v "^$" || true
    echo "==> Custom CA certificate installed successfully"
else
    echo "==> Warning: No custom CA cert found at $CA_CERT — skipping CA installation"
    echo "==>          Place your PEM file there if you need custom certificate trust."
fi
