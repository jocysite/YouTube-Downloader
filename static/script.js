let currentData = null;
let selectedVideoFormat = null;
let selectedAudioFormat = null;
let playlistData = [];
let skippedIndices = new Set();

// DOM Elements
const urlInput = document.getElementById("urlInput");
const fetchBtn = document.getElementById("fetchBtn");
const infoSection = document.getElementById("infoSection");
const videoInfo = document.getElementById("videoInfo");
const typeSection = document.getElementById("typeSection");
const qualitySection = document.getElementById("qualitySection");
const downloadSection = document.getElementById("downloadSection");
const videoQualityContainer = document.getElementById("videoQualityContainer");
const videoFormats = document.getElementById("videoFormats");
const audioFormats = document.getElementById("audioFormats");
const downloadBtn = document.getElementById("downloadBtn");
const progressSection = document.getElementById("progressSection");
const progressFill = document.getElementById("progressFill");
const progressText = document.getElementById("progressText");
const playlistSection = document.getElementById("playlistSection");
const playlistVideosContainer = document.getElementById("playlistVideos");

// Event Listeners
fetchBtn.addEventListener("click", fetchVideoInfo);
urlInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") fetchVideoInfo();
});

document.querySelectorAll('input[name="downloadType"]').forEach((radio) => {
  radio.addEventListener("change", handleDownloadTypeChange);
});

downloadBtn.addEventListener("click", startDownload);

// Fetch Video Info
async function fetchVideoInfo() {
  const url = urlInput.value.trim();

  if (!url) {
    showError("Please enter a YouTube URL");
    return;
  }

  setLoading(fetchBtn, true);
  hideAllSections();
  skippedIndices.clear();

  try {
    const response = await fetch("/api/fetch-info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to fetch video info");
    }

    currentData = data;
    displayVideoInfo(data);
    displayFormats(data);

    infoSection.classList.remove("hidden");
    typeSection.classList.remove("hidden");
    qualitySection.classList.remove("hidden");
    downloadSection.classList.remove("hidden");

    // Show playlist section if it's a playlist
    if (data.is_playlist && data.videos) {
      playlistData = data.videos;
      displayPlaylistVideos(data.videos);
      playlistSection.classList.remove("hidden");
    }
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(fetchBtn, false);
  }
}

// Display Playlist Videos
function displayPlaylistVideos(videos) {
  playlistVideosContainer.innerHTML = "";

  videos.forEach((video) => {
    const videoItem = document.createElement("div");
    videoItem.className = "playlist-video-item";
    videoItem.dataset.index = video.index;

    const duration = formatDuration(video.duration);

    videoItem.innerHTML = `
            <div class="playlist-video-checkbox">
                <input type="checkbox" id="video-${video.index}" checked>
            </div>
            <div class="playlist-video-info">
                <div class="playlist-video-number">${video.index}</div>
                <div class="playlist-video-details">
                    <div class="playlist-video-title">${video.title}</div>
                    <div class="playlist-video-duration">${duration}</div>
                </div>
            </div>
        `;

    const checkbox = videoItem.querySelector('input[type="checkbox"]');
    checkbox.addEventListener("change", (e) => {
      if (e.target.checked) {
        skippedIndices.delete(video.index);
        videoItem.classList.remove("skipped");
      } else {
        skippedIndices.add(video.index);
        videoItem.classList.add("skipped");
      }
      updateDownloadCount();
    });

    playlistVideosContainer.appendChild(videoItem);
  });

  updateDownloadCount();
}

// Format duration
function formatDuration(seconds) {
  if (!seconds) return "Unknown";
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  }
  return `${minutes}:${String(secs).padStart(2, "0")}`;
}

// Update download count
function updateDownloadCount() {
  if (!currentData || !currentData.videos) return;

  const totalVideos = currentData.videos.length;
  const selectedCount = totalVideos - skippedIndices.size;

  const countElement = document.getElementById("selectedCount");
  if (countElement) {
    countElement.textContent = `${selectedCount} of ${totalVideos} videos selected`;
  }
}

// Select All Videos
function selectAllVideos() {
  skippedIndices.clear();
  document.querySelectorAll(".playlist-video-item").forEach((item) => {
    const checkbox = item.querySelector('input[type="checkbox"]');
    checkbox.checked = true;
    item.classList.remove("skipped");
  });
  updateDownloadCount();
}

// Deselect All Videos
function deselectAllVideos() {
  document.querySelectorAll(".playlist-video-item").forEach((item) => {
    const index = parseInt(item.dataset.index);
    skippedIndices.add(index);
    const checkbox = item.querySelector('input[type="checkbox"]');
    checkbox.checked = false;
    item.classList.add("skipped");
  });
  updateDownloadCount();
}

// Display Video Info
function displayVideoInfo(data) {
  const playlistBadge = data.is_playlist
    ? `<span class="badge">${data.video_count} videos</span>`
    : "";

  videoInfo.innerHTML = `
        <div class="info-item">
            <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="info-label">Title:</span>
            <span class="info-value">${data.title}</span>
        </div>
        <div class="info-item">
            <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
            </svg>
            <span class="info-label">Type:</span>
            <span class="info-value">
                ${data.is_playlist ? "Playlist" : "Single Video"}
                ${playlistBadge}
            </span>
        </div>
    `;
}

// Display Formats
function displayFormats(data) {
  // Video Formats
  videoFormats.innerHTML = "";
  data.video_formats.forEach((format, index) => {
    const formatItem = createFormatItem(format, "video", index);
    videoFormats.appendChild(formatItem);
  });

  // Audio Formats
  audioFormats.innerHTML = "";
  data.audio_formats.forEach((format, index) => {
    const formatItem = createFormatItem(format, "audio", index);
    audioFormats.appendChild(formatItem);
  });

  // Select first formats by default
  if (data.video_formats.length > 0) {
    selectFormat(videoFormats.children[0], data.video_formats[0], "video");
  }
  if (data.audio_formats.length > 0) {
    selectFormat(audioFormats.children[0], data.audio_formats[0], "audio");
  }
}

// Create Format Item
function createFormatItem(format, type, index) {
  const div = document.createElement("div");
  div.className = "format-item";

  const detail =
    type === "video" ? format.res : `${Math.round(format.abr)}kbps`;

  div.innerHTML = `
        <div class="format-main">
            <span class="format-ext">${format.ext}</span>
            <span class="format-detail">${detail}</span>
        </div>
        ${format.note ? `<span class="format-note">${format.note}</span>` : ""}
    `;

  div.addEventListener("click", () => {
    selectFormat(div, format, type);
  });

  return div;
}

// Select Format
function selectFormat(element, format, type) {
  const container = type === "video" ? videoFormats : audioFormats;

  // Remove previous selection
  container.querySelectorAll(".format-item").forEach((item) => {
    item.classList.remove("selected");
  });

  // Add selection
  element.classList.add("selected");

  if (type === "video") {
    selectedVideoFormat = format.id;
  } else {
    selectedAudioFormat = format.id;
  }
}

// Handle Download Type Change
function handleDownloadTypeChange(e) {
  const downloadType = e.target.value;

  if (downloadType === "audio") {
    videoQualityContainer.style.display = "none";
  } else {
    videoQualityContainer.style.display = "block";
  }
}

// Start Download
async function startDownload() {
  const downloadType = document.querySelector(
    'input[name="downloadType"]:checked',
  ).value;

  if (!selectedAudioFormat) {
    showError("Please select an audio quality");
    return;
  }

  if (downloadType === "video" && !selectedVideoFormat) {
    showError("Please select a video quality");
    return;
  }

  setLoading(downloadBtn, true);
  progressSection.classList.remove("hidden");

  try {
    const response = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: urlInput.value.trim(),
        download_type: downloadType,
        video_format_id: selectedVideoFormat,
        audio_format_id: selectedAudioFormat,
        is_playlist: currentData.is_playlist,
        skip_indices: Array.from(skippedIndices), // NEW: Send skip indices
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to start download");
    }

    // Poll for progress
    pollDownloadStatus(data.session_id);
  } catch (error) {
    showError(error.message);
    setLoading(downloadBtn, false);
    progressSection.classList.add("hidden");
  }
}

// Poll Download Status
async function pollDownloadStatus(sessionId) {
  const interval = setInterval(async () => {
    try {
      const response = await fetch(`/api/download-status/${sessionId}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error("Failed to get download status");
      }

      // Update progress
      progressFill.style.width = `${data.progress}%`;
      progressText.textContent = data.message;

      if (data.status === "completed") {
        clearInterval(interval);
        setLoading(downloadBtn, false);
        showSuccess(
          "Download completed successfully! Check your downloads folder.",
        );

        setTimeout(() => {
          progressSection.classList.add("hidden");
          progressFill.style.width = "0%";
        }, 3000);
      } else if (data.status === "error") {
        clearInterval(interval);
        setLoading(downloadBtn, false);
        showError(data.message);
      }
    } catch (error) {
      clearInterval(interval);
      setLoading(downloadBtn, false);
      showError(error.message);
    }
  }, 1000);
}

// Utility Functions
function setLoading(button, isLoading) {
  const btnText = button.querySelector(".btn-text");
  const spinner = button.querySelector(".spinner");

  if (isLoading) {
    btnText.classList.add("hidden");
    spinner.classList.remove("hidden");
    button.disabled = true;
  } else {
    btnText.classList.remove("hidden");
    spinner.classList.add("hidden");
    button.disabled = false;
  }
}

function hideAllSections() {
  infoSection.classList.add("hidden");
  typeSection.classList.add("hidden");
  qualitySection.classList.add("hidden");
  downloadSection.classList.add("hidden");
  progressSection.classList.add("hidden");
  playlistSection.classList.add("hidden");
}

function showError(message) {
  alert("❌ Error: " + message);
}

function showSuccess(message) {
  alert("✅ " + message);
}

// Buy Me a Coffee popup — shown every time the app opens
function showCoffeeModal() {
  const modal = document.getElementById("coffeeModal");
  if (modal) modal.classList.remove("hidden");
}

function closeCoffeeModal() {
  const modal = document.getElementById("coffeeModal");
  if (modal) modal.classList.add("hidden");
}

// Close the desktop window (via pywebview) or browser tab as a fallback
function closeApp() {
  if (window.pywebview && window.pywebview.api && window.pywebview.api.close_app) {
    window.pywebview.api.close_app();
  } else {
    window.close();
  }
}

showCoffeeModal();
