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
# install-playwright.sh
#
# Installs Playwright and Chromium browser for taking screenshots in
# alert reports. This is needed because the base image doesn't include
# a headless browser.
#
# Must be invoked before the worker starts processing alerts.
# docker-compose-ssl.yml prepends this script to the worker command.

set -eo pipefail

echo "==> Installing Playwright for alert/report screenshots"

# Check if already installed
if python -c "import playwright" 2>/dev/null; then
    echo "==> Playwright already installed, checking for browsers..."
    if playwright install --dry-run chromium 2>/dev/null | grep -q "chromium"; then
        echo "==> Chromium already installed, skipping"
        exit 0
    fi
fi

# Install Playwright package
echo "==> Installing playwright Python package..."
pip install playwright --quiet

# Install Chromium browser
echo "==> Installing Chromium browser for Playwright..."
playwright install chromium --with-deps

echo "==> Playwright and Chromium installed successfully"