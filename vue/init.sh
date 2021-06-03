#!/bin/bash
set -e
npm remove webpack-dev-server
npm install webpack-dev-server@2.9.1
npm run dev
