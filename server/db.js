const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, 'data.db');

function open() {
  return new sqlite3.Database(DB_PATH);
}

function initialize() {
  const db = open();
  db.serialize(() => {
	db.run(`CREATE TABLE IF NOT EXISTS users (
	  id INTEGER PRIMARY KEY,
	  name TEXT,
	  email TEXT
	)`);

	db.run(`CREATE TABLE IF NOT EXISTS plans (
	  id INTEGER PRIMARY KEY,
	  name TEXT,
	  data_mb INTEGER,
	  minutes INTEGER,
	  sms INTEGER,
	  price_cents INTEGER
	)`);

	db.run(`CREATE TABLE IF NOT EXISTS subscriptions (
	  id INTEGER PRIMARY KEY,
	  user_id INTEGER,
	  plan_id INTEGER,
	  start_date TEXT,
	  end_date TEXT,
	  auto_renew INTEGER
	)`);

	db.run(`CREATE TABLE IF NOT EXISTS usage (
	  id INTEGER PRIMARY KEY,
	  user_id INTEGER,
	  period_start TEXT,
	  period_end TEXT,
	  data_used_mb INTEGER,
	  minutes_used INTEGER,
	  sms_used INTEGER
	)`);

	db.run(`CREATE TABLE IF NOT EXISTS bills (
	  id INTEGER PRIMARY KEY,
	  user_id INTEGER,
	  period_start TEXT,
	  period_end TEXT,
	  amount_due_cents INTEGER,
	  paid INTEGER,
	  due_date TEXT
	)`);

	db.run(`CREATE TABLE IF NOT EXISTS offers (
	  id INTEGER PRIMARY KEY,
	  title TEXT,
	  description TEXT,
	  benefit_type TEXT,
	  benefit_value INTEGER,
	  valid_from TEXT,
	  valid_to TEXT
	)`);

	// Seed minimal data if empty
	db.get('SELECT COUNT(*) as c FROM users', (err, row) => {
	  if (err) return console.error(err);
	  if (row.c === 0) {
		seed(db);
	  }
	});
  });
  return db;
}

function seed(db) {
  const now = new Date().toISOString();

  db.run(`INSERT INTO users (name, email) VALUES (?,?)`, ['Demo User', 'demo@example.com']);

  const plans = [
	['Basic 5GB', 5 * 1024, 500, 100, 2999],
	['Standard 10GB', 10 * 1024, 1000, 200, 3999],
	['Unlimited 50GB', 50 * 1024, 5000, 500, 5999]
  ];
  const stmt = db.prepare('INSERT INTO plans (name,data_mb,minutes,sms,price_cents) VALUES (?,?,?,?,?)');
  plans.forEach(p => stmt.run(p));
  stmt.finalize();

  db.run(`INSERT INTO subscriptions (user_id, plan_id, start_date, end_date, auto_renew) VALUES (?,?,?,?,?)`, [1, 2, now, null, 1]);

  // usage for last 3 months
  const usages = [
	[1, '2023-12-01', '2023-12-31', 9 * 1024, 800, 100],
	[1, '2024-01-01', '2024-01-31', 11 * 1024, 900, 120],
	[1, '2024-02-01', '2024-02-28', 12 * 1024, 700, 80]
  ];
  const ustmt = db.prepare('INSERT INTO usage (user_id, period_start, period_end, data_used_mb, minutes_used, sms_used) VALUES (?,?,?,?,?,?)');
  usages.forEach(u => ustmt.run(u));
  ustmt.finalize();

  db.run(`INSERT INTO bills (user_id, period_start, period_end, amount_due_cents, paid, due_date) VALUES (?,?,?,?,?)`, [1, '2024-02-01', '2024-02-28', 3999, 0, '2024-03-10']);

  db.run(`INSERT INTO offers (title, description, benefit_type, benefit_value, valid_from, valid_to) VALUES (?,?,?,?,?,?)`,
	['10% off for auto-pay', 'Get 10% off monthly bill when you enable auto-pay', 'discount_percent', 10, '2024-01-01', '2024-12-31']);
}

module.exports = { open, initialize };
