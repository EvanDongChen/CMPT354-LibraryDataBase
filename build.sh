#!/usr/bin/env bash
# Always run from repo root
cd "$(dirname "$0")"

cd frontend
npm install
npm run build
cd ..
rm -rf backend/build
cp -r frontend/build backend/build
