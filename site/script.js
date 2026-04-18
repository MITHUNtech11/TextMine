const modeButtons = Array.from(document.querySelectorAll('.mode-btn'));
const apiUrlInput = document.getElementById('apiUrl');
const healthButton = document.getElementById('healthButton');
const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const clearFileButton = document.getElementById('clearFile');
const parseButton = document.getElementById('parseButton');
const statusMessage = document.getElementById('statusMessage');
const fileMeta = document.getElementById('fileMeta');
const summaryGrid = document.getElementById('summaryGrid');
const jsonOutput = document.getElementById('jsonOutput');
const copyJsonButton = document.getElementById('copyJson');
const downloadJsonButton = document.getElementById('downloadJson');

const STORAGE_KEY = 'textmine-api-url';
const MAX_FILE_SIZE = 50 * 1024 * 1024;
const ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'];

const state = {
  mode: 'offline',
  file: null,
  result: null,
};

function init() {
  const savedApiUrl = localStorage.getItem(STORAGE_KEY);
  if (savedApiUrl) {
    apiUrlInput.value = savedApiUrl;
  }

  modeButtons.forEach((button) => {
    button.addEventListener('click', () => setMode(button.dataset.mode));
  });

  apiUrlInput.addEventListener('change', () => {
    const cleaned = normalizeUrl(apiUrlInput.value);
    apiUrlInput.value = cleaned;
    localStorage.setItem(STORAGE_KEY, cleaned);
  });

  healthButton.addEventListener('click', checkApiHealth);
  fileInput.addEventListener('change', onFileSelect);
  clearFileButton.addEventListener('click', clearSelectedFile);
  parseButton.addEventListener('click', parseResume);
  copyJsonButton.addEventListener('click', copyJson);
  downloadJsonButton.addEventListener('click', downloadJson);

  ['dragenter', 'dragover'].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropZone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropZone.classList.remove('dragover');
    });
  });

  dropZone.addEventListener('drop', (event) => {
    const droppedFile = event.dataTransfer?.files?.[0] || null;
    if (!droppedFile) {
      return;
    }
    assignFile(droppedFile);
  });

  applyRevealAnimation();
  renderSummaryCards([{ label: 'Status', value: 'Awaiting parse' }]);
}

function applyRevealAnimation() {
  const revealNodes = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          const delay = Math.min(index * 50, 300);
          setTimeout(() => entry.target.classList.add('visible'), delay);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  revealNodes.forEach((node) => observer.observe(node));
}

function setMode(mode) {
  state.mode = mode;
  modeButtons.forEach((button) => {
    button.classList.toggle('active', button.dataset.mode === mode);
  });
  setStatus('neutral', `Mode selected: ${mode === 'online' ? 'AI Enhanced' : 'Offline'}.`);
}

function normalizeUrl(value) {
  return (value || '').trim().replace(/\/+$/, '');
}

function onFileSelect(event) {
  const selectedFile = event.target.files?.[0] || null;
  if (!selectedFile) {
    return;
  }
  assignFile(selectedFile);
}

function assignFile(file) {
  const extension = (file.name.split('.').pop() || '').toLowerCase();

  if (!ALLOWED_EXTENSIONS.includes(extension)) {
    clearSelectedFile();
    setStatus('err', 'Unsupported file format. Please upload a resume document or image.');
    return;
  }

  if (file.size > MAX_FILE_SIZE) {
    clearSelectedFile();
    setStatus('err', 'File is too large. The limit is 50 MB.');
    return;
  }

  state.file = file;
  fileMeta.textContent = `${file.name} (${formatBytes(file.size)})`;
  setStatus('ok', 'File selected. You can now parse.');
}

function clearSelectedFile() {
  state.file = null;
  fileInput.value = '';
  fileMeta.textContent = 'No file selected';
}

function formatBytes(bytes) {
  if (!Number.isFinite(bytes) || bytes <= 0) {
    return '0 B';
  }
  const units = ['B', 'KB', 'MB', 'GB'];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const amount = bytes / 1024 ** index;
  return `${amount.toFixed(index === 0 ? 0 : 2)} ${units[index]}`;
}

function endpointForMode(mode) {
  return mode === 'online' ? '/parse_resume/online' : '/parse_resume/offline';
}

async function checkApiHealth() {
  const baseUrl = normalizeUrl(apiUrlInput.value);
  if (!baseUrl) {
    setStatus('warn', 'Enter your backend API URL first.');
    return;
  }

  setStatus('neutral', 'Checking API health...');

  try {
    const response = await fetch(`${baseUrl}/health`, { method: 'GET' });
    if (!response.ok) {
      throw new Error(`Health check failed (${response.status}).`);
    }
    const healthPayload = await response.json();
    setStatus('ok', `API is reachable. Status: ${healthPayload.status || 'healthy'}.`);
  } catch (error) {
    setStatus('err', error.message || 'Unable to reach API endpoint.');
  }
}

async function parseResume() {
  const baseUrl = normalizeUrl(apiUrlInput.value);
  if (!baseUrl) {
    setStatus('warn', 'Please provide your backend API URL.');
    return;
  }

  if (!state.file) {
    setStatus('warn', 'Please select a file before parsing.');
    return;
  }

  const endpoint = endpointForMode(state.mode);
  const formData = new FormData();
  formData.append('file', state.file);

  parseButton.disabled = true;
  parseButton.textContent = 'Parsing...';
  setStatus('neutral', 'Parsing in progress. This may take a few moments.');

  try {
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'POST',
      body: formData,
      headers: {
        Accept: 'application/json',
      },
    });

    const responseText = await response.text();
    let payload;

    try {
      payload = JSON.parse(responseText);
    } catch {
      payload = { message: responseText || 'No JSON payload returned by API.' };
    }

    if (!response.ok) {
      const detail = payload.detail || payload.message || `Request failed (${response.status}).`;
      throw new Error(detail);
    }

    state.result = payload;
    jsonOutput.textContent = JSON.stringify(payload, null, 2);
    renderSummaryCards(buildSummary(payload));
    copyJsonButton.disabled = false;
    downloadJsonButton.disabled = false;

    setStatus('ok', 'Parse completed successfully.');
  } catch (error) {
    setStatus('err', error.message || 'Parsing failed.');
  } finally {
    parseButton.disabled = false;
    parseButton.textContent = 'Parse Resume';
  }
}

function buildSummary(payload) {
  const topLevelKeys = Object.keys(payload || {});

  const skills = payload.skills || payload?.parsed_data?.skills || [];
  const experience = payload.experience || payload?.parsed_data?.experience || [];
  const education = payload.education || payload?.parsed_data?.education || [];

  return [
    { label: 'Mode', value: state.mode === 'online' ? 'AI Enhanced' : 'Offline' },
    { label: 'Top-level fields', value: String(topLevelKeys.length) },
    { label: 'Skills', value: String(Array.isArray(skills) ? skills.length : 0) },
    { label: 'Experience entries', value: String(Array.isArray(experience) ? experience.length : 0) },
    { label: 'Education entries', value: String(Array.isArray(education) ? education.length : 0) },
  ];
}

function renderSummaryCards(items) {
  summaryGrid.innerHTML = '';
  items.forEach((item) => {
    const card = document.createElement('div');
    card.className = 'summary-card';

    const label = document.createElement('p');
    label.className = 'summary-label';
    label.textContent = item.label;

    const value = document.createElement('p');
    value.className = 'summary-value';
    value.textContent = item.value;

    card.appendChild(label);
    card.appendChild(value);
    summaryGrid.appendChild(card);
  });
}

async function copyJson() {
  if (!state.result) {
    return;
  }

  try {
    await navigator.clipboard.writeText(JSON.stringify(state.result, null, 2));
    setStatus('ok', 'JSON copied to clipboard.');
  } catch {
    setStatus('warn', 'Clipboard copy is not available in this browser context.');
  }
}

function downloadJson() {
  if (!state.result) {
    return;
  }

  const blob = new Blob([JSON.stringify(state.result, null, 2)], { type: 'application/json' });
  const href = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const baseName = state.file ? state.file.name.replace(/\.[^/.]+$/, '') : 'resume';

  link.href = href;
  link.download = `${baseName}_parsed.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(href);

  setStatus('ok', 'JSON file downloaded.');
}

function setStatus(type, message) {
  statusMessage.className = `status-message ${type}`;
  statusMessage.textContent = message;
}

init();
