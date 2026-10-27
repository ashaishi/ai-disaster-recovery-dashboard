
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
main { max-width: 1100px; margin: auto; padding: 25px 5%; }
.banner {
  padding: 12px 15px; border: 1px solid #665c32;
  border-radius: 9px; color: #facc15;
  background: #292617; margin-bottom: 20px; font-size: 13px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
  gap: 16px;
}
.card {
  background: #131f33; border: 1px solid #293951;
  border-radius: 12px; padding: 20px;
}
.label { color: #9fb0c8; font-size: 13px; }
.status { font-size: 21px; font-weight: bold; margin: 12px 0; }
.green { color: #6ee7b7; }
.blue { color: #93c5fd; }
.yellow { color: #facc15; }
h2 { font-size: 18px; margin-top: 28px; }
button {
  border: 0; border-radius: 8px; padding: 12px 18px;
  margin: 8px 8px 8px 0; cursor: pointer; font-weight: bold;
}
button:disabled { opacity: .4; cursor: not-allowed; }
.primary { background: #3b82f6; color: white; }
.secondary { background: #253650; color: white; }
.checks {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(230px,1fr));
  gap: 10px; margin-top: 16px;
}
.check {
  padding: 13px; border-radius: 8px;
  background: #0e192b; border: 1px solid #293951;
}
.check strong { display: block; margin-bottom: 6px; }
.check small { color: #9fb0c8; line-height: 1.5; }
#result { margin-top: 16px; line-height: 1.7; white-space: pre-wrap; }
#events { white-space: pre-wrap; line-height: 1.7; color: #cbd5e1; }
footer { color: #8798b1; font-size: 12px; margin-top: 28px; line-height: 1.6; }
</style>
</head>
<body>
<header>
  <h1>AI Disaster Recovery Control Center</h1>
  <p>DC ↔ DR | Readiness Gate | Controlled DR Demonstration</p>
</header>

<main>
  <div class="banner">
    DEMO MODE — readiness results and DR state transitions are simulated.
    No live infrastructure is connected.
  </div>

  <div class="grid">
    <div class="card">
      <div class="label">DATA CENTER (DC)</div>
      <div class="status green" id="dcStatus">PRIMARY / ACTIVE</div>
      <div id="dcDescription">Initial demonstration state</div>
    </div>
    <div class="card">
      <div class="label">DISASTER RECOVERY (DR)</div>
      <div class="status blue" id="drStatus">STANDBY</div>
      <div id="drDescription">Waiting for demo execution</div>
    </div>
    <div class="card">
      <div class="label">READINESS GATE</div>
      <div class="status yellow" id="readiness">NOT RUN</div>
      <div id="readinessDescription">Run the readiness demo to begin</div>
    </div>
    <div class="card">
      <div class="label">WORKFLOW STATUS</div>
      <div class="status blue" id="workflow">NOT STARTED</div>
      <div id="workflowDescription">Waiting for readiness assessment</div>
    </div>
  </div>

  <h2>1. Pre-DR readiness assessment</h2>
  <div class="card">
    <p>Run the successful demonstration scenario. Each PASS below is sample data, not a live system check.</p>
    <button class="primary" id="readinessButton" onclick="runReadiness()">
      Run AI Readiness Demo
    </button>

    <div class="checks" id="checks">
      <div class="check"><strong>Database synchronization</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>Backup and restore verification</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>DC/DR connectivity</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>Kubernetes nodes and pods</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>GitHub code and version</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>Jenkins pipeline readiness</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>Application and database health</strong><small>Awaiting demo assessment</small></div>
      <div class="check"><strong>Transaction validation</strong><small>Awaiting demo assessment</small></div>
    </div>

    <div id="result" role="status">Readiness assessment has not run.</div>
  </div>

  <h2>2. Human approval and DR execution</h2>
  <div class="card">
    <p id="approvalText">Complete the readiness assessment before proceeding.</p>
    <button class="primary" id="drButton" onclick="executeDR()" disabled>
      Execute DR Demo
    </button>
    <button class="secondary" onclick="resetDemo()">Reset Demo</button>
    <div id="completion" role="status"></div>
  </div>

  <h2>Event log</h2>
  <div class="card" id="events">Dashboard initialized. Demo mode is active.</div>

  <footer>
    Educational demonstration only. PASS results are predefined sample results.
    No real AI model is called, and no real database, backup, Kubernetes,
    GitHub, Jenkins, application, or network check is executed.
    No real database promotion, failover, or traffic switching occurs.
    <br><span id="updated"></span>
  </footer>
</main>

<script>
const $ = id => document.getElementById(id);

let readinessPassed = false;
let completed = false;
let history = ["Dashboard initialized — demo mode."];

const demoChecks = [
  ["Database synchronization", "Demo replication status: synchronized"],
  ["Backup and restore verification", "Demo backup and restore checks passed"],
  ["DC/DR connectivity", "Demo dependency connectivity passed"],
  ["Kubernetes nodes and pods", "Demo nodes and application pods ready"],
  ["GitHub code and version", "Demo source version consistency passed"],
  ["Jenkins pipeline readiness", "Demo pipeline validation passed"],
  ["Application and database health", "Demo health checks passed"],
  ["Transaction validation", "Demo transaction validation passed"]
];

function log(message) {
  history.unshift(new Date().toLocaleTimeString() + " — " + message);
  $("events").textContent = history.slice(0, 10).join("\\n");
}

function renderChecks() {
  $("checks").innerHTML = demoChecks.map(item =>
    '<div class="check">' +
    '<strong><span class="green">✓ PASS</span> — ' + item[0] + '</strong>' +
    '<small>' + item[1] + '</small>' +
    '</div>'
  ).join("");
}

function runReadiness() {
  if (completed) return;

  renderChecks();
  readinessPassed = true;

  $("readiness").textContent = "ALL CHECKS PASSED";
  $("readiness").className = "status green";
  $("readinessDescription").textContent = "Demo readiness gate passed";

  $("workflow").textContent = "READY FOR DR";
  $("workflow").className = "status green";
  $("workflowDescription").textContent = "Awaiting your approval";

  $("result").textContent =
    "DEMO READINESS REPORT\\n\\n" +
    "✓ All 8 demonstration checks passed\\n" +
    "✓ No simulated blocker detected\\n" +
    "✓ Human approval is required before proceeding\\n\\n" +
    "Recommendation: READY FOR PLANNED DR DEMO";

  $("approvalText").textContent =
    "Readiness passed in demo mode. Click Execute DR Demo to show the DC-to-DR state transition.";

  $("drButton").disabled = false;
  $("readinessButton").textContent = "Readiness Demo Passed";
  $("readinessButton").disabled = true;

  log("Demo readiness completed — all 8 sample checks passed.");
  log("DR demo is awaiting the user's explicit approval.");
}

function executeDR() {
  if (!readinessPassed || completed) return;

  const approved = confirm(
    "Approve the simulated DC-to-DR transition? " +
    "This changes only the demo webpage. No real infrastructure will change."
  );

  if (!approved) {
    log("User declined DR demo execution. State unchanged.");
    return;
  }

  $("dcStatus").textContent = "STANDBY";
  $("dcStatus").className = "status blue";
  $("dcDescription").textContent = "Standby — simulated final state";

  $("drStatus").textContent = "ACTIVE";
  $("drStatus").className = "status green";
  $("drDescription").textContent = "Primary role — simulated final state";

  $("workflow").textContent = "DR DEMO COMPLETED";
  $("workflow").className = "status green";
  $("workflowDescription").textContent = "Workflow stopped at successful completion";

  $("readiness").textContent = "PASSED";
  $("readiness").className = "status green";

  $("approvalText").textContent = "Approval received for the simulated workflow.";
  $("drButton").disabled = true;
  $("completion").textContent =
    "✓ Simulated DR activation completed\\n" +
    "✓ Simulated post-switch health validation passed\\n" +
    "✓ Simulated transaction validation passed\\n" +
    "✓ Final state: DR ACTIVE — DC STANDBY\\n\\n" +
    "DR DEMO COMPLETED. No further action will run.";

  completed = true;
  log("User approved the demo-only DR transition.");
  log("Demo state changed: DC ACTIVE → DC STANDBY; DR STANDBY → DR ACTIVE.");
  log("Simulated post-switch validation passed.");
  log("DR DEMO COMPLETED — workflow stopped.");
}

function resetDemo() {
  readinessPassed = false;
  completed = false;

  $("dcStatus").textContent = "PRIMARY / ACTIVE";
  $("dcStatus").className = "status green";
  $("dcDescription").textContent = "Initial demonstration state";

  $("drStatus").textContent = "STANDBY";
  $("drStatus").className = "status blue";
  $("drDescription").textContent = "Waiting for demo execution";

  $("readiness").textContent = "NOT RUN";
  $("readiness").className = "status yellow";
  $("readinessDescription").textContent = "Run the readiness demo to begin";

  $("workflow").textContent = "NOT STARTED";
  $("workflow").className = "status blue";
  $("workflowDescription").textContent = "Waiting for readiness assessment";

  $("checks").innerHTML = demoChecks.map(item =>
    '<div class="check"><strong>' + item[0] +
    '</strong><small>Awaiting demo assessment</small></div>'
  ).join("");

  $("result").textContent = "Readiness assessment has not run.";
  $("approvalText").textContent = "Complete the readiness assessment before proceeding.";
  $("completion").textContent = "";
  $("drButton").disabled = true;
  $("readinessButton").disabled = false;
  $("readinessButton").textContent = "Run AI Readiness Demo";

  history = ["Demo reset — demo mode."];
  $("events").textContent = history[0];
  log("Dashboard reset to initial DC-active state.");
}

$("updated").textContent =
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
