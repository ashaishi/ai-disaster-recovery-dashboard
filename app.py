
from flask import Flask, jsonify, render_template_string
from datetime import datetime, timezone

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Disaster Recovery Control Center</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0; font-family: Arial, sans-serif;
  background: #0b1220; color: #e5edf8;
}
header {
  padding: 26px 5%; background: #111c30;
  border-bottom: 1px solid #293951;
}
header h1 { margin: 0 0 8px; font-size: 26px; }
header p { margin: 0; color: #9fb0c8; }
main { max-width: 1050px; margin: auto; padding: 25px 5%; }
.grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 16px; }
.card {
  background: #131f33; border: 1px solid #293951;
  border-radius: 12px; padding: 20px;
}
.label { color: #9fb0c8; font-size: 13px; }
.status { font-size: 22px; font-weight: bold; margin: 12px 0; }
.green { color: #6ee7b7; }
.blue { color: #93c5fd; }
h2 { font-size: 18px; margin-top: 28px; }
button {
  border: 0; border-radius: 8px; padding: 12px 18px;
  margin: 8px 8px 8px 0; cursor: pointer; font-weight: bold;
}
.primary { background: #3b82f6; color: white; }
.secondary { background: #253650; color: white; }
#result { margin-top: 16px; white-space: pre-wrap; line-height: 1.7; }
footer { color: #8798b1; font-size: 12px; margin-top: 28px; }
</style>
</head>
<body>
<header>
  <h1>AI Disaster Recovery Control Center</h1>
  <p>DC ↔ DR | Readiness Monitoring | Controlled Simulation</p>
</header>
<main>
  <div class="grid">
    <div class="card">
      <div class="label">DATA CENTER</div>
      <div class="status green">PRIMARY</div>
      <div>Role: Active (simulated)</div>
    </div>
    <div class="card">
      <div class="label">DISASTER RECOVERY</div>
      <div class="status blue" id="drStatus">STANDBY</div>
      <div id="drDescription">Role: Standby (simulated)</div>
    </div>
    <div class="card">
      <div class="label">READINESS ASSESSMENT</div>
      <div class="status green" id="readiness">READY FOR REVIEW</div>
      <div>Demo environment — no real database connection</div>
    </div>
  </div>

  <h2>Recovery operations</h2>
  <div class="card">
    <p>Run a demo readiness assessment or simulate a recovery workflow.</p>
    <button class="primary" onclick="runCheck()">Run readiness check</button>
    <button class="secondary" onclick="simulate()">Simulate failover</button>
    <button class="secondary" onclick="resetDemo()">Reset demo</button>
    <div id="result" role="status">Waiting for your action.</div>
  </div>

  <h2>Event log</h2>
  <div class="card" id="events">Dashboard initialized.</div>
  <footer>
    Educational simulation only. No live database is promoted, no real
    payment is processed, and no production traffic is changed.
    <br><span id="updated"></span>
  </footer>
</main>
<script>
const result = document.getElementById("result");
const events = document.getElementById("events");
let history = ["Dashboard initialized."];

function log(message) {
  history.unshift(new Date().toLocaleTimeString() + " — " + message);
  events.textContent = history.slice(0, 8).join("\\n");
}
function runCheck() {
  document.getElementById("readiness").textContent = "CHECK PASSED";
  result.textContent =
    "DEMO READINESS REPORT\\n" +
    "✓ Simulated DC role configured\\n" +
    "✓ Simulated DR role configured\\n" +
    "✓ Demo validation checks passed\\n" +
    "⚠ Live replication and backups not verified\\n" +
    "Decision: READY FOR MANUAL REVIEW";
  log("Demo readiness assessment completed.");
}
function simulate() {
  if (!confirm("Run a simulated failover? No real database or traffic will change.")) return;
  document.getElementById("drStatus").textContent = "SIMULATED ACTIVE";
  document.getElementById("drDescription").textContent = "Demo role only";
  document.getElementById("readiness").textContent = "SIMULATION COMPLETE";
  result.textContent =
    "SIMULATION COMPLETE\\n" +
    "1. Readiness assessment displayed\\n" +
    "2. Demo DR role changed in this page\\n" +
    "3. Demo validation completed\\n\\n" +
    "No real database promotion or traffic switching occurred.";
  log("Simulated failover completed — no infrastructure changed.");
}
function resetDemo() {
  document.getElementById("drStatus").textContent = "STANDBY";
  document.getElementById("drDescription").textContent = "Role: Standby (simulated)";
  document.getElementById("readiness").textContent = "READY FOR REVIEW";
  result.textContent = "Demo reset. Waiting for your action.";
  history = ["Demo reset."];
  events.textContent = history[0];
  log("Dashboard reset.");
}
document.getElementById("updated").textContent =
  "Dashboard loaded: " + new Date().toLocaleString();
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "mode": "simulation_only",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
