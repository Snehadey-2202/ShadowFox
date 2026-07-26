// dashboard.js - Guaranteed Chart Box Rendering & Zoom Lightbox Modal

let globalData = {
    leaderboard: [],
    logs: [],
    scouting: {}
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
            document.getElementById(targetId).classList.add("active");

            // If switching to Charts tab, ensure chart images reload cleanly
            if (targetId === "tab-charts") {
                renderCharts();
            }
        });
    });
}

async function fetchDashboardData() {
    try {
        const response = await fetch("/api/data");
        const data = await response.json();

        if (data.error) {
            console.error("API Error:", data.error);
            return;
        }

        globalData = data;
        renderKPIs(data.kpis);
        renderLeaderboard(data.leaderboard);
        renderScoutingProfiles(data.scouting);
        renderCharts();
        renderDeliveryLogs(data.logs);
        populateOverDropdown(data.logs);
    } catch (err) {
        console.error("Failed to load dashboard data:", err);
    }
}

function renderKPIs(kpis) {
    document.getElementById("kpi-top-fielder").innerText = kpis.top_fielder || "N/A";
    document.getElementById("kpi-top-ps").innerText = (kpis.top_ps || 0) + " PS";
    document.getElementById("kpi-runs-saved").innerText = "+" + (kpis.total_runs_saved || 0);
    document.getElementById("kpi-dismissals").innerText = kpis.total_dismissals || 0;
    document.getElementById("kpi-deliveries").innerText = kpis.total_deliveries || 0;
}

function renderLeaderboard(leaderboard) {
    const tbody = document.getElementById("leaderboard-tbody");
    if (!tbody) return;

    tbody.innerHTML = "";
    leaderboard.forEach((player, idx) => {
        const tr = document.createElement("tr");

        let badgeClass = "badge-infield";
        if (player.role.includes("Outfield")) badgeClass = "badge-outfield";
        if (player.role.includes("Wicketkeeper")) badgeClass = "badge-keeper";

        tr.innerHTML = `
            <td><strong>#${idx + 1}</strong></td>
            <td><strong>${player.player_name}</strong></td>
            <td><span class="badge ${badgeClass}">${player.role} (${player.primary_position})</span></td>
            <td>${player.clean_picks}</td>
            <td>${player.good_throws}</td>
            <td>${player.catches}</td>
            <td>${player.stumpings}</td>
            <td>${player.run_outs}</td>
            <td>${player.direct_hits}</td>
            <td>+${player.runs_saved}</td>
            <td><span class="ps-pill">${player.performance_score} PS</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderScoutingProfiles(scouting) {
    const grid = document.getElementById("scouting-grid");
    if (!grid) return;

    grid.innerHTML = "";
    const players = [scouting.Dhoni, scouting.Kohli, scouting.Pandya];

    players.forEach(p => {
        if (!p) return;
        const card = document.createElement("div");
        card.className = "scout-card";

        const strengthsHtml = p.key_strengths.map(s => `<li>${s}</li>`).join("");
        const coachingHtml = p.coaching_points.map(c => `<li>${c}</li>`).join("");

        card.innerHTML = `
            <div class="scout-header">
                <div class="scout-name">
                    <h3>${p.stats.player_name}</h3>
                    <div class="scout-role">${p.role}</div>
                </div>
                <div class="scout-rank">Rank #${p.match_rank} | ${p.stats.performance_score} PS</div>
            </div>
            <div class="scout-highlight">
                ⚡ <strong>Match Highlight:</strong> ${p.match_highlight}
            </div>
            <div class="scout-section-title">Key Tactical Strengths</div>
            <ul class="scout-list">
                ${strengthsHtml}
            </ul>
            <div class="scout-section-title" style="margin-top: 1rem;">Coaching Directives</div>
            <ul class="scout-list">
                ${coachingHtml}
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

    // Add click event for full-screen zoom modal and fallback image handler
    document.querySelectorAll(".zoomable-chart").forEach(img => {
        img.onerror = () => {
            console.warn("Retrying chart load for:", img.src);
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
    if (!tbody) return;

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
            <td>${log.batter} vs ${log.bowler}</td>
            <td><strong>${log.fielder}</strong> (${log.position})</td>
            <td>${log.short_description}</td>
            <td>${keyEventBadge}</td>
            <td>+${log.runs_saved}</td>
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
        opt.value = i;
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
        const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
        const overVal = overFilter ? overFilter.value : "all";
        const posVal = positionFilter ? positionFilter.value : "all";
        const disVal = dismissalFilter ? dismissalFilter.value : "all";

        const filtered = globalData.logs.filter(log => {
            const matchesQuery = (
                log.fielder.toLowerCase().includes(query) ||
                log.position.toLowerCase().includes(query) ||
                log.short_description.toLowerCase().includes(query) ||
                log.over.toString().includes(query)
            );
            const matchesOver = (overVal === "all" || log.over.toString() === overVal);
            
            let matchesPos = true;
            if (posVal === "Wicketkeeper") matchesPos = log.position.includes("Wicketkeeper");
            else if (posVal === "Infield") matchesPos = log.zone === "Infield" || log.position.includes("Infield") || log.position.includes("Cover") || log.position.includes("Point");
            else if (posVal === "Outfield") matchesPos = log.zone === "Outfield" || log.position.includes("Deep") || log.position.includes("Long") || log.position.includes("Fine Leg");

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
