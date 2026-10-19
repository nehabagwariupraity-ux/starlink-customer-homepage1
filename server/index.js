const express = require('express');
const cors = require('cors');
const dbModule = require('./db');

const app = express();
app.use(cors());
app.use(express.json());

const db = dbModule.initialize();

app.get('/api/users/:id/summary', (req, res) => {
  const userId = Number(req.params.id);
  db.get('SELECT u.id,u.name,u.email,s.plan_id,p.name as plan_name,p.data_mb,p.price_cents FROM users u LEFT JOIN subscriptions s ON s.user_id=u.id LEFT JOIN plans p ON p.id=s.plan_id WHERE u.id=?', [userId], (err, row) => {
	if (err) return res.status(500).json({ error: err.message });
	if (!row) return res.status(404).json({ error: 'user not found' });

	db.get('SELECT SUM(amount_due_cents) as outstanding FROM bills WHERE user_id=? AND paid=0', [userId], (err2, billRow) => {
	  if (err2) return res.status(500).json({ error: err2.message });
	  db.get('SELECT * FROM usage WHERE user_id=? ORDER BY period_start DESC LIMIT 1', [userId], (err3, usageRow) => {
		if (err3) return res.status(500).json({ error: err3.message });
		res.json({
		  user: { id: row.id, name: row.name, email: row.email },
		  currentPlan: { id: row.plan_id, name: row.plan_name, data_mb: row.data_mb, price_cents: row.price_cents },
		  lastUsage: usageRow || null,
		  outstandingCents: (billRow && billRow.outstanding) || 0
		});
	  });
	});
  });
});

// Simple rule-based recommender
app.get('/api/users/:id/recommendations', (req, res) => {
  const userId = Number(req.params.id);

  // get current plan
  db.get('SELECT s.plan_id, p.name as plan_name, p.data_mb, p.price_cents FROM subscriptions s JOIN plans p ON p.id=s.plan_id WHERE s.user_id=?', [userId], (err, planRow) => {
	if (err) return res.status(500).json({ error: err.message });
	if (!planRow) return res.status(404).json({ error: 'subscription not found' });

	// compute average data used last 3 records
	db.all('SELECT data_used_mb, minutes_used, sms_used FROM usage WHERE user_id=? ORDER BY period_start DESC LIMIT 3', [userId], (err2, usageRows) => {
	  if (err2) return res.status(500).json({ error: err2.message });

	  let avgData = 0;
	  if (usageRows && usageRows.length > 0) {
		avgData = Math.round(usageRows.reduce((s, r) => s + r.data_used_mb, 0) / usageRows.length);
	  }

	  db.all('SELECT id,name,data_mb,price_cents FROM plans ORDER BY data_mb ASC', [], (err3, plans) => {
		if (err3) return res.status(500).json({ error: err3.message });

		const recs = [];

		// if user is using >90% of data, recommend next larger plan or data add-on
		if (avgData > 0.9 * planRow.data_mb) {
		  const larger = plans.find(p => p.data_mb > planRow.data_mb);
		  if (larger) {
			recs.push({
			  type: 'plan_upgrade',
			  plan: larger,
			  reason: `You use about ${Math.round(avgData/1024*10)/10} GB/month vs your plan ${Math.round(planRow.data_mb/1024*10)/10} GB. Upgrade to ${larger.name} to avoid overages.`,
			  estimatedMonthlyDeltaCents: larger.price_cents - planRow.price_cents
			});
		  } else {
			recs.push({ type: 'addon', addon: 'data_pack_5gb', reason: 'You frequently approach your data cap. Add a 5GB pack to avoid throttling/overages.', estimatedMonthlyDeltaCents: 499 });
		  }
		}

		// if user uses much less than plan, recommend downgrade
		if (avgData < 0.3 * planRow.data_mb) {
		  const cheaper = plans.slice().reverse().find(p => p.data_mb < planRow.data_mb && p.price_cents < planRow.price_cents);
		  if (cheaper) {
			recs.push({ type: 'plan_downgrade', plan: cheaper, reason: `You use only about ${Math.round(avgData/1024*10)/10} GB/month; consider ${cheaper.name} to save money.`, estimatedMonthlyDeltaCents: cheaper.price_cents - planRow.price_cents });
		  }
		}

		// offers
		db.all('SELECT * FROM offers WHERE valid_from <= date("now") AND valid_to >= date("now")', [], (err4, offers) => {
		  if (err4) return res.status(500).json({ error: err4.message });
		  if (offers && offers.length > 0) {
			offers.forEach(o => {
			  recs.push({ type: 'offer', offer: o, reason: o.description });
			});
		  }

		  // Sort by estimated benefit (simple: larger savings first)
		  const sorted = recs.sort((a, b) => (b.estimatedMonthlyDeltaCents || 0) - (a.estimatedMonthlyDeltaCents || 0));
		  res.json({ recommendations: sorted, avgDataMb: avgData, currentPlan: planRow });
		});
	  });
	});
  });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
