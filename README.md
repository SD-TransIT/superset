<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Superset

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation](https://img.shields.io/badge/docs-apache.org-blue.svg)](https://superset.apache.org)

This is a fork of [Apache Superset](https://github.com/apache/superset) adjusted for purpose of generating responsive 
dashboards embedded directly in core TransIT application.

### Changes
docker-compose.yml change to production instance. Used Superset image is pointing to `transit/superset`:latest 
instead of `apache/superset`.

Dashboards stored in `transit_dashboards` are automatically deployed during setup. 
Database connection used by these dashboards is adjusted through `.env-non-dev`

`docker-compose.yml` is using with transit-network to reach data (necessary when transit backend also relies on db service.)

`SUPERSET_FEATURE_EMBEDDED_SUPERSET` is enabled by default.

Content of `.github` folder removed. 



