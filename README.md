# Telecom Recommendation Demo

This repository contains a minimal prototype: a Node/Express backend with a SQLite database and a small React (Vite) frontend. It demonstrates an on-homepage recommendation widget that suggests plan upgrades/downgrades or offers based on recent usage.

Quick start

1. Server

   - Open a terminal and run:
	 cd server
	 npm install
	 npm start

   The server runs on http://localhost:4000 and creates a demo SQLite database at server/data.db.

2. Client

   - In another terminal:
	 cd client
	 npm install
	 npm run dev

   - Open the Vite dev URL (usually http://localhost:5173). The client proxies /api to the server.

Notes
- This is a minimal demo. The apply/apply-flow is not implemented. The recommender is rule-based and intended as a starting point.
- Feel free to ask for enhancements: authentication scaffolding, persisted user accounts, upgrade endpoints, or a real CI/CD setup.
