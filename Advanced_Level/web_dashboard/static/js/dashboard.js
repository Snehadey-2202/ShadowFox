// dashboard.js - Resilient Data Loader with Defensive Fallbacks & Full Section Rendering

let globalData = {
    leaderboard: [],
    logs: [],
    scouting: {},
    kpis: {}
};

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    fetchDashboardData();
    initFilters();
    initModal();
});

function initTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabViews = document.querySelectorAll(".tab-view");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            tabViews.forEach(v => v.classList.remove("active"));

            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            const targetView = document.getElementById(targetId);
            if (targetView) targetView.classList.add("active");

            // Re-render charts when switching to charts tab to avoid image rendering delay
            if (targetId === "tab-charts") {
                renderCharts();
            }
        });
    });
}

async function fetchDashboardData() {
    try {
        console.log("[+] Fetching dashboard data from /api/data...");
        const response = await fetch("/api/data");
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.error) {
            console.error("API Returned Error:", data.error);
            return;
        }

        globalData = data;
        
        // Execute each section renderer independently with defensive error boundaries
        safeExecute(() => renderKPIs(data.kpis), "renderKPIs");
        safeExecute(() => renderLeaderboard(data.leaderboard), "renderLeaderboard");
        safeExecute(() => renderScoutingProfiles(data.scouting), "renderScoutingProfiles");
        safeExecute(() => renderCharts(), "renderCharts");
        safeExecute(() => renderDeliveryLogs(data.logs), "renderDeliveryLogs");
        safeExecute(() => populateOverDropdown(data.logs), "populateOverDropdown");

        console.log("[SUCCESS] All dashboard data successfully loaded and rendered!");
    } catch (err) {
        console.error("Critical error loading dashboard data:", err);
    }
}

function safeExecute(fn, name) {
    try {
        fn();
    } catch (e) {
        console.error(`Error in ${name}:`, e);
    }
}

function renderKPIs(kpis) {
    if (!kpis) return;
    const topFielderEl = document.getElementById("kpi-top-fielder");
    const topPsEl = document.getElementById("kpi-top-ps");
    const runsSavedEl = document.getElementById("kpi-runs-saved");
    const dismissalsEl = document.getElementById("kpi-dismissals");
    const deliveriesEl = document.getElementById("kpi-deliveries");

    if (topFielderEl) topFielderEl.innerText = kpis.top_fielder || "N/A";
    if (topPsEl) topPsEl.innerText = (kpis.top_ps !== undefined ? kpis.top_ps : 0) + " PS";
    if (runsSavedEl) runsSavedEl.innerText = "+" + (kpis.total_runs_saved !== undefined ? kpis.total_runs_saved : 0);
    if (dismissalsEl) dismissalsEl.innerText = kpis.total_dismissals !== undefined ? kpis.total_dismissals : 0;
    if (deliveriesEl) deliveriesEl.innerText = kpis.total_deliveries !== undefined ? kpis.total_deliveries : 0;
}

function renderLeaderboard(leaderboard) {
    const tbody = document.getElementById("leaderboard-tbody");
    if (!tbody || !Array.isArray(leaderboard)) return;

    tbody.innerHTML = "";
    leaderboard.forEach((player, idx) => {
        const tr = document.createElement("tr");

        const role = player.role || "Fielder";
        const position = player.primary_position || "Field";

        let badgeClass = "badge-infield";
        if (role.includes("Outfield")) badgeClass = "badge-outfield";
        if (role.includes("Wicketkeeper")) badgeClass = "badge-keeper";

        tr.innerHTML = `
            <td><strong>#${idx + 1}</strong></td>
            <td><strong>${player.player_name || 'Player'}</strong></td>
            <td><span class="badge ${badgeClass}">${role} (${position})</span></td>
            <td>${player.clean_picks || 0}</td>
            <td>${player.good_throws || 0}</td>
            <td>${player.catches || 0}</td>
            <td>${player.stumpings || 0}</td>
            <td>${player.run_outs || 0}</td>
            <td>${player.direct_hits || 0}</td>
            <td>+${player.runs_saved || 0}</td>
            <td><span class="ps-pill">${player.performance_score || 0} PS</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderScoutingProfiles(scouting) {
    const grid = document.getElementById("scouting-grid");
    if (!grid || !scouting) return;

    grid.innerHTML = "";
    const players = [scouting.Dhoni, scouting.Kohli, scouting.Pandya].filter(Boolean);

    players.forEach(p => {
        const card = document.createElement("div");
        card.className = "scout-card";

        const stats = p.stats || {};
        const strengths = Array.isArray(p.key_strengths) ? p.key_strengths : [];
        const coaching = Array.isArray(p.coaching_points) ? p.coaching_points : [];

        const strengthsHtml = strengths.map(s => `<li>${s}</li>`).join("");
        const coachingHtml = coaching.map(c => `<li>${c}</li>`).join("");

        card.innerHTML = `
            <div class="scout-header">
                <div class="scout-name">
                    <h3>${stats.player_name || p.player_name || 'Target Player'}</h3>
                    <div class="scout-role">${p.role || 'Fielder'}</div>
                </div>
                <div class="scout-rank">Rank #${p.match_rank || 1} | ${stats.performance_score || 0} PS</div>
            </div>
            <div class="scout-highlight">
                ⚡ <strong>Match Highlight:</strong> ${p.match_highlight || 'Solid defensive contribution.'}
            </div>
            <div class="scout-section-title">Key Tactical Strengths</div>
            <ul class="scout-list">
                ${strengthsHtml || '<li>Consistent fielding positioning</li>'}
            </ul>
            <div class="scout-section-title" style="margin-top: 1rem;">Coaching Directives</div>
            <ul class="scout-list">
                ${coachingHtml || '<li>Maintain defensive alertness</li>'}
            </ul>
        `;
        grid.appendChild(card);
    });
}

function renderCharts() {
    const container = document.getElementById("charts-grid");
    if (!container) return;

    const chartFiles = [
        { name: "team_performance_scores.png", title: "Team Performance Ranking (PS)" },
        { name: "target_player_comparison.png", title: "Target Player Metric Comparison" },
        { name: "fielding_zone_analysis.png", title: "Fielding Zone Territorial Analysis" },
        { name: "runs_saved_analysis.png", title: "Net Runs Saved per Player" },
        { name: "dismissal_breakdown.png", title: "Fielding Dismissals Breakdown" }
    ];

    container.innerHTML = "";
    chartFiles.forEach(c => {
        const div = document.createElement("div");
        div.className = "chart-card";
        
        const timestamp = new Date().getTime();
        const imgSrc = `/charts/${c.name}?t=${timestamp}`;

        div.innerHTML = `
            <div class="chart-card-title">${c.title}</div>
            <div class="chart-img-wrapper">
                <img class="zoomable-chart" src="${imgSrc}" alt="${c.title}" title="Click to view full-screen zoom">
            </div>
        `;
        container.appendChild(div);
    });

    document.querySelectorAll(".zoomable-chart").forEach(img => {
        img.onerror = () => {
            console.warn("Retrying chart image load:", img.src);
            setTimeout(() => {
                img.src = img.src.split('?')[0] + '?t=' + new Date().getTime();
            }, 1000);
        };

        img.addEventListener("click", () => {
            const modal = document.getElementById("chart-modal");
            const modalImg = document.getElementById("modal-img");
            if (modal && modalImg) {
                modalImg.src = img.src;
                modal.classList.add("active");
            }
        });
    });
}

function initModal() {
    const modal = document.getElementById("chart-modal");
    const closeBtn = document.getElementById("modal-close");

    if (closeBtn && modal) {
        closeBtn.addEventListener("click", () => modal.classList.remove("active"));
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.classList.remove("active");
        });
    }
}

function renderDeliveryLogs(logs) {
    const tbody = document.getElementById("logs-tbody");
    if (!tbody || !Array.isArray(logs)) return;

    tbody.innerHTML = "";
    logs.forEach(log => {
        const tr = document.createElement("tr");

        let keyEventBadge = "";
        if (log.catches > 0) keyEventBadge += '<span class="badge badge-outfield">Catch</span> ';
        if (log.direct_hits > 0) keyEventBadge += '<span class="badge badge-infield">Direct Hit</span> ';
        if (log.run_outs > 0) keyEventBadge += '<span class="badge badge-infield">Run Out</span> ';
        if (log.stumpings > 0) keyEventBadge += '<span class="badge badge-keeper">Stumping</span> ';
        if (!keyEventBadge) keyEventBadge = '<span style="color: var(--text-muted);">Routine</span>';

        tr.innerHTML = `
            <td><strong>${log.over}.${log.ball}</strong></td>
            <td>${log.batter || 'Batter'} vs ${log.bowler || 'Bowler'}</td>
            <td><strong>${log.fielder || 'Fielder'}</strong> (${log.position || 'Position'})</td>
            <td>${log.short_description || 'Routine action'}</td>
            <td>${keyEventBadge}</td>
            <td>+${log.runs_saved || 0}</td>
        `;
        tbody.appendChild(tr);
    });
}

function populateOverDropdown(logs) {
    const dropdown = document.getElementById("over-filter");
    if (!dropdown) return;

    dropdown.innerHTML = '<option value="all">All Overs (1 - 20)</option>';
    for (let i = 1; i <= 20; i++) {
        const opt = document.createElement("option");
        opt.value = i.toString();
        opt.innerText = `Over ${i}`;
        dropdown.appendChild(opt);
    }
}

function initFilters() {
    const searchInput = document.getElementById("search-input");
    const overFilter = document.getElementById("over-filter");
    const positionFilter = document.getElementById("position-filter");
    const dismissalFilter = document.getElementById("dismissal-filter");

    const applyFilters = () => {
        if (!globalData || !Array.isArray(globalData.logs)) return;

        const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
        const overVal = overFilter ? overFilter.value : "all";
        const posVal = positionFilter ? positionFilter.value : "all";
        const disVal = dismissalFilter ? dismissalFilter.value : "all";

        const filtered = globalData.logs.filter(log => {
            const fielderName = (log.fielder || "").toLowerCase();
            const posName = (log.position || "").toLowerCase();
            const desc = (log.short_description || "").toLowerCase();
            const overStr = (log.over !== undefined ? log.over.toString() : "");

            const matchesQuery = (
                fielderName.includes(query) ||
                posName.includes(query) ||
                desc.includes(query) ||
                overStr.includes(query)
            );
            const matchesOver = (overVal === "all" || overStr === overVal);
            
            let matchesPos = true;
            if (posVal === "Wicketkeeper") matchesPos = posName.includes("keeper") || posName.includes("wicket");
            else if (posVal === "Infield") matchesPos = log.zone === "Infield" || posName.includes("infield") || posName.includes("cover") || posName.includes("point");
            else if (posVal === "Outfield") matchesPos = log.zone === "Outfield" || posName.includes("deep") || posName.includes("long") || posName.includes("fine leg");

            let matchesDis = true;
            if (disVal === "catch") matchesDis = log.catches > 0;
            else if (disVal === "stumping") matchesDis = log.stumpings > 0;
            else if (disVal === "runout") matchesDis = log.run_outs > 0 || log.direct_hits > 0;

            return matchesQuery && matchesOver && matchesPos && matchesDis;
        });

        renderDeliveryLogs(filtered);
    };

    if (searchInput) searchInput.addEventListener("input", applyFilters);
    if (overFilter) overFilter.addEventListener("change", applyFilters);
    if (positionFilter) positionFilter.addEventListener("change", applyFilters);
    if (dismissalFilter) dismissalFilter.addEventListener("change", applyFilters);
}
