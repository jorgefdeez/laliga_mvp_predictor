const predictionsContainer = document.querySelector("#predictions");
const errorMessage = document.querySelector("#error-message");
const statusText = document.querySelector("#status-text");

const escapeHtml = (value) => String(value)
	.replaceAll("&", "&amp;")
	.replaceAll("<", "&lt;")
	.replaceAll(">", "&gt;")
	.replaceAll('"', "&quot;")
	.replaceAll("'", "&#039;");

const renderPredictions = (predictions) => {
	predictionsContainer.innerHTML = predictions.map((prediction, index) => `
		<article class="player-card" style="--delay: ${index * 55}ms">
			<div class="rank">${String(index + 1).padStart(2, "0")}</div>
			<div class="player-copy">
				<h3>${escapeHtml(prediction.player_name)}</h3>
				<p>${escapeHtml(prediction.team)}</p>
			</div>
			<div class="probability">
				<strong>${Number(prediction.probability).toFixed(2)}%</strong>
				<span>chance</span>
			</div>
		</article>
	`).join("");
};

const loadPredictions = async () => {
	try {
		const response = await fetch("/api/top10");
		if (!response.ok) {
			throw new Error("Prediction request failed");
		}
		const predictions = await response.json();
		renderPredictions(predictions);
		statusText.textContent = "Live model";
	} catch (error) {
		statusText.textContent = "Unavailable";
		errorMessage.classList.remove("is-hidden");
	}
};

loadPredictions();
