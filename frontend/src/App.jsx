import { useCallback, useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8001/api";

function App() {
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedFinding, setSelectedFinding] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

 
  
  const fetchFindings = useCallback(async () => {
    const response = await fetch(`${API_URL}/findings`);

    if (!response.ok) {
      throw new Error("Unable to load security findings.");
    }

    return response.json();
  }, []);

  const loadFindings = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const data = await fetchFindings();
      setFindings(data.findings ?? []);
      setLastUpdated(new Date());
    } catch {
      setError(
        "Could not connect to the CloudGuard API. Check that it is running on port 8001."
      );
    } finally {
      setLoading(false);
    }
  }, [fetchFindings]);

  useEffect(() => {
    let cancelled = false;

    fetchFindings()
      .then((data) => {
        if (cancelled) return;

        setFindings(data.findings ?? []);
        setLastUpdated(new Date());
      })
      .catch(() => {
        if (!cancelled) {
          setError(
            "Could not connect to the CloudGuard API. Check that it is running on port 8001."
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [fetchFindings]);
 

  const counts = {
    HIGH: findings.filter((item) => item.severity === "HIGH").length,
    MEDIUM: findings.filter((item) => item.severity === "MEDIUM").length,
    LOW: findings.filter((item) => item.severity === "LOW").length,
  };

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">C</div>
          <div>
            <strong>CloudGuard</strong>
            <span>AI SECURITY CENTER</span>
          </div>
        </div>

        <p className="nav-label">WORKSPACE</p>
        <div className="nav-item active">▦ <span>Overview</span></div>
        <div className="nav-item">⌘ <span>Security findings</span></div>
        <div className="nav-item">◇ <span>Cloud resources</span></div>

        <div className="sidebar-bottom">
          <div className="status-dot" />
          <div>
            <strong>Demo environment</strong>
            <span>Connected to local API</span>
          </div>
        </div>
      </aside>

      <section className="main-content">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> Overview</div>
          <div className="demo-pill"><span /> SIMULATED DATA</div>
        </header>

        <div className="page-heading">
          <div>
            <p className="eyebrow">CLOUD SECURITY OVERVIEW</p>
            <h1>Your cloud, in focus.</h1>
            <p className="subtitle">
              Understand security risks and get practical remediation guidance.
            </p>
          </div>
          <button className="refresh-button" onClick={loadFindings} disabled={loading}>
            {loading ? "Refreshing..." : "↻  Refresh findings"}
          </button>
        </div>

        <div className="notice">
          <span className="notice-icon">i</span>
          <div>
            <strong>Demo mode is active</strong>
            <p>These findings are simulated examples, not results from a live AWS security scan.</p>
          </div>
        </div>

        <div className="section-heading">
          <div>
            <h2>Security posture</h2>
            <p>A quick breakdown of detected demo findings.</p>
          </div>
          <span className="updated">
            {lastUpdated ? `Updated ${lastUpdated.toLocaleTimeString()}` : "Waiting for data"}
          </span>
        </div>

        <div className="summary-grid">
          <article className="summary-card total-card">
            <div className="card-top"><span>Total findings</span><span className="metric-icon">▤</span></div>
            <strong className="metric">{findings.length}</strong>
            <span className="metric-caption">Across demo resources</span>
          </article>
          <article className="summary-card">
            <div className="card-top"><span>High severity</span><span className="severity-icon high">!</span></div>
            <strong className="metric">{counts.HIGH}</strong>
            <span className="metric-caption">Prioritize immediately</span>
          </article>
          <article className="summary-card">
            <div className="card-top"><span>Medium severity</span><span className="severity-icon medium">!</span></div>
            <strong className="metric">{counts.MEDIUM}</strong>
            <span className="metric-caption">Review recommended</span>
          </article>
          <article className="summary-card">
            <div className="card-top"><span>Low severity</span><span className="severity-icon low">i</span></div>
            <strong className="metric">{counts.LOW}</strong>
            <span className="metric-caption">Improve when possible</span>
          </article>
        </div>

        <section className="findings-panel">
          <div className="panel-heading">
            <div>
              <h2>Security findings</h2>
              <p>Review risks and recommended next steps.</p>
            </div>
            <span className="result-count">{findings.length} findings</span>
          </div>

          {error && <div className="error-message">{error}</div>}
          {loading && <p className="empty-state">Loading security findings…</p>}
          {!loading && !error && findings.length === 0 && (
            <p className="empty-state">No findings returned by the API.</p>
          )}

          {!loading && findings.length > 0 && (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>FINDING</th>
                    <th>RESOURCE</th>
                    <th>SEVERITY</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {findings.map((finding) => (
                    <tr key={finding.id}>
                      <td>
                        <strong>{finding.issue}</strong>
                        <span className="finding-id">{finding.id}</span>
                      </td>
                      <td><span className="resource-name">{finding.resource}</span></td>
                      <td><span className={`severity-badge ${finding.severity.toLowerCase()}`}>{finding.severity}</span></td>
                      <td>
                        <button className="text-button" onClick={() => setSelectedFinding(finding)}>
                          View remediation →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer>
          <span>CloudGuard AI <span className="footer-separator">•</span> Hackathon prototype</span>
          <span>Security insights made actionable.</span>
        </footer>
      </section>

      {selectedFinding && (
        <div className="modal-backdrop" onClick={() => setSelectedFinding(null)}>
          <section
            className="remediation-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <button className="modal-close" onClick={() => setSelectedFinding(null)} aria-label="Close dialog">×</button>
            <p className="eyebrow">REMEDIATION GUIDANCE · {selectedFinding.id}</p>
            <h2 id="modal-title">{selectedFinding.issue}</h2>
            <p className="modal-resource">Resource: {selectedFinding.resource}</p>
            <span className={`severity-badge ${selectedFinding.severity.toLowerCase()}`}>
              {selectedFinding.severity} severity
            </span>
            <div className="recommendation-box">
              <strong>Recommended next step</strong>
              <p>{selectedFinding.recommendation}</p>
            </div>
            <p className="demo-footnote">This is general guidance for a simulated finding. Verify your environment before making changes.</p>
            <button className="refresh-button modal-done" onClick={() => setSelectedFinding(null)}>Done</button>
          </section>
        </div>
      )}
    </main>
  );
}

export default App;
