cd frontend
npm install
npm run build
cd ..
rm -rf backend/build
cp -r frontend/build backend/build