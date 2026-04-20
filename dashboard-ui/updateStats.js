/* UPDATE THESE VALUES TO MATCH YOUR SETUP */

const PROCESSING_STATS_API_URL = "/processing/stats";
const ANALYZER_API_URL = {
    stats: "/analyzer/stats",
    matchSummaryBase: "/analyzer/match-summaries",
    bettingOddsBase: "/analyzer/betting-odds"
};
const HEALTH_API_URL = "/health/health-status";

// This function fetches and updates the general statistics => GET request helper
const makeReq = (url, cb) => {
    fetch(url)
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP ${res.status} from ${url}`);
            }
            return res.json();
        })
        .then((result) => {
            console.log("Received data from", url, result);
            cb(result);
        })
        .catch((error) => {
            console.error("Request failed:", error);
            updateErrorMessages(error.message);
        });
};

// Writes JSON nicely into a <code> block
const updateCodeDiv = (result, elemId) => {
    document.getElementById(elemId).innerText = JSON.stringify(result, null, 2);
};

// Human-readable browser time
const getLocaleDateStr = () => {
    return new Date().toLocaleString();
};

// Show temporary error messages on screen
const updateErrorMessages = (message) => {
    const id = Date.now();

    const msg = document.createElement("div");
    msg.id = `error-${id}`;
    msg.innerHTML = `<p>Something happened at ${getLocaleDateStr()}!</p><code>${message}</code>`;

    document.getElementById("messages").style.display = "block";
    document.getElementById("messages").prepend(msg);

    setTimeout(() => {
        const elem = document.getElementById(`error-${id}`);
        if (elem) {
            elem.remove();
        }
    }, 7000);
};

// Time difference function
const getSecondsAgo = (isoTimestamp) => {
    if (!isoTimestamp) return "Not available";

    const now = new Date();
    const past = new Date(isoTimestamp + "Z");

    const diffMs = now - past;
    const diffSeconds = Math.floor(diffMs / 1000);

    if (diffSeconds < 60) return `${diffSeconds} seconds ago`;

    const diffMinutes = Math.floor(diffSeconds / 60);
    return `${diffMinutes} minute(s) ago`;
};

const setStatusBadge = (elemId, status) => {
    const elem = document.getElementById(elemId);
    elem.innerText = status;

    elem.classList.remove("status-up", "status-down", "status-unknown");

    if (status === "Up") {
        elem.classList.add("status-up");
    } else if (status === "Down") {
        elem.classList.add("status-down");
    } else {
        elem.classList.add("status-unknown");
    }
};

const updateHealthPanel = (result) => {
    setStatusBadge("receiver-status", result.receiver || "Unknown");
    setStatusBadge("storage-status", result.storage || "Unknown");
    setStatusBadge("processing-status", result.processing || "Unknown");
    setStatusBadge("analyzer-status", result.analyzer || "Unknown");

    document.getElementById("health-last-update").innerText =
        "Updated " + getSecondsAgo(result.last_update);
};

// Fetch the latest analyzer events based on current counts
const updateLatestAnalyzerEvents = (stats) => {
    const matchCount = stats.num_match_summaries || 0;
    const bettingCount = stats.num_betting_odds || 0;

    if (matchCount > 0) {
        const lastMatchIndex = matchCount - 1;
        makeReq(
            `${ANALYZER_API_URL.matchSummaryBase}?index=${lastMatchIndex}`,
            (result) => updateCodeDiv(result, "event-match-summary")
        );
    } else {
        document.getElementById("event-match-summary").innerText =
            "Waiting for match summary event...";
    }

    if (bettingCount > 0) {
        const lastBettingIndex = bettingCount - 1;
        makeReq(
            `${ANALYZER_API_URL.bettingOddsBase}?index=${lastBettingIndex}`,
            (result) => updateCodeDiv(result, "event-betting-odds")
        );
    } else {
        document.getElementById("event-betting-odds").innerText =
            "Waiting for betting odds event...";
    }
};

// Pull fresh data from all endpoints
const getStats = () => {
    document.getElementById("last-updated-value").innerText = getLocaleDateStr();

    makeReq(PROCESSING_STATS_API_URL, (result) => updateCodeDiv(result, "processing-stats"));

    makeReq(ANALYZER_API_URL.stats, (result) => {
        updateCodeDiv(result, "analyzer-stats");
        updateLatestAnalyzerEvents(result);
    });

    makeReq(HEALTH_API_URL, (result) => updateHealthPanel(result));
};

// Initial load + auto-refresh every 4 seconds
const setup = () => {
    getStats();
    setInterval(() => getStats(), 4000);
};

document.addEventListener("DOMContentLoaded", setup);