#!/usr/bin/env bash
# This is a dummy change to force git to track permissions

cd frontend
npm install
npm run build
cd ..
rm -rf backend/build
cp -r frontend/build backend/build