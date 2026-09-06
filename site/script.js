const modeButtons = Array.from(document.querySelectorAll('.mode-btn'));
const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const clearFileButton = document.getElementById('clearFile');
const parseButton = document.getElementById('parseButton');
const statusMessage = document.getElementById('statusMessage');
const fileMeta = document.getElementById('fileMeta');
const previewMode = document.getElementById('previewMode');
const previewModeText = document.getElementById('previewModeText');
const previewIcon = document.getElementById('previewIcon');
const filePreviewName = document.getElementById('filePreviewName');
const filePreviewMeta = document.getElementById('filePreviewMeta');
const previewFormat = document.getElementById('previewFormat');
const previewSize = document.getElementById('previewSize');
const overviewOutput = document.getElementById('overviewOutput');

const MAX_FILE_SIZE = 50 * 1024 * 1024;
const ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'];
const DEFAULT_RESULT = { message: 'Upload a document and click Extract Text.' };

const state = {
  mode: 'offline',
  file: null,
  result: null,
};

function init() {
  modeButtons.forEach((button) => {
    button.addEventListener('click', () => setMode(button.dataset.mode));
  });

  if (fileInput) {
    fileInput.addEventListener('change', onFileSelect);
  }

if (clearFileButton) {
  clearFileButton.addEventListener('click', clearSelectedFile);
}

if (parseButton) {
  parseButton.addEventListener('click', parseResume);
}

if (dropZone) {
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
}

renderResult(DEFAULT_RESULT);
applyRevealAnimation();
updateFilePreview();
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

const label = mode === 'online' ? 'AI + OCR' : 'OCR Only';
previewMode.textContent = label;
previewModeText.textContent = label;
setStatus('neutral', `Mode selected: ${label}.`);
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
    setStatus('err', 'Unsupported file format. Please upload a document image or text file.');
    return;
  }

  if (file.size > MAX_FILE_SIZE) {
    clearSelectedFile();
    setStatus('err', 'File is too large. The limit is 50 MB.');
    return;
  }

  state.file = file;
  fileMeta.textContent = `${file.name} (${formatBytes(file.size)})`;
  updateFilePreview(file);
  setStatus('ok', 'File selected. You can now parse.');
}

function clearSelectedFile() {
  state.file = null;
state.result = null;
if (fileInput) {
  fileInput.value = '';
}
fileMeta.textContent = 'No file selected';
updateFilePreview();
renderResult(DEFAULT_RESULT);
}

function updateFilePreview(file = state.file) {
const label = state.mode === 'online' ? 'AI + OCR' : 'OCR Only';
previewMode.textContent = label;
previewModeText.textContent = label;

if (!file) {
  previewIcon.textContent = 'FILE';
  filePreviewName.textContent = 'No file selected';
  filePreviewMeta.textContent = 'Upload a document to begin.';
  previewFormat.textContent = '—';
  previewSize.textContent = '—';
  return;
}

const extension = (file.name.split('.').pop() || '').toUpperCase();
previewIcon.textContent = extension || 'FILE';
filePreviewName.textContent = file.name;
filePreviewMeta.textContent = 'Ready to extract';
previewFormat.textContent = extension || 'Unknown';
previewSize.textContent = formatBytes(file.size);
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

function escapeHtml(value) {
return String(value ?? '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/\"/g, '&quot;')
  .replace(/'/g, '&#039;');
}

function buildSectionTitle(title) {
return `<div class="result-section-title">${escapeHtml(title)}</div>`;
}

function renderResult(result) {
  if (!overviewOutput) {
    return;
  }

  const payload = result && Object.keys(result).length ? result : DEFAULT_RESULT;
  const parsed = payload.parsed_json || payload;
  const extractedText = payload.extracted_text || parsed.extracted_text || '';
  const readableText = payload.readable_text || parsed.readable_text || '';
  const pageCount = payload.page_count || parsed.page_count || 1;
  const confidence = payload.confidence_score || parsed.confidence_score || payload.accuracy || parsed.accuracy || 0;
  const modeLabel = payload.processing_mode === 'online' || state.mode === 'online' ? 'AI + OCR' : 'OCR Only';
  const fileName = state.file?.name || 'Document';
  const charCount = (readableText || extractedText).length;

  const rawTextMarkup = extractedText
    ? `<div class="raw-text">${escapeHtml(extractedText)}</div>`
    : '<span class="empty-state">No OCR text available.</span>';

  const restoredTextMarkup = readableText
    ? `<div class="raw-text" style="background: rgba(42, 157, 255, 0.05); border: 1px solid rgba(42, 157, 255, 0.2); font-size: 0.9rem; line-height: 1.7;">${escapeHtml(readableText)}</div>`
    : rawTextMarkup;

  const docSummary = parsed.summary
    ? `<div class="summary-box" style="margin-bottom: 0.8rem; padding: 0.75rem; border-radius: 8px; background: rgba(255, 122, 0, 0.08); border-left: 3px solid var(--brand);">
        <strong style="font-size: 0.8rem; text-transform: uppercase; color: var(--brand-strong); display: block; margin-bottom: 0.25rem;">Document Summary</strong>
        <p class="summary-text" style="font-size: 0.88rem;">${escapeHtml(parsed.summary)}</p>
      </div>`
    : '';

  const docTitle = parsed.document_title
    ? `<span class="chip" style="margin-left: 0.5rem; font-size: 0.75rem;">${escapeHtml(parsed.document_title)}</span>`
    : '';

  let sectionsMarkup = '';
  if (Array.isArray(parsed.sections) && parsed.sections.length > 0) {
    sectionsMarkup = `
      <div class="result-card" style="margin-top: 1rem;">
        ${buildSectionTitle('Recovered Document Sections')}
        <div style="display: grid; gap: 0.75rem;">
          ${parsed.sections.map((sec) => `
            <div style="padding: 0.6rem; border-radius: 8px; background: rgba(255, 255, 255, 0.6); border: 1px solid rgba(42, 157, 255, 0.1);">
              ${sec.heading ? `<strong style="font-size: 0.85rem; color: var(--brand-strong); display: block; margin-bottom: 0.2rem;">${escapeHtml(sec.heading)}</strong>` : ''}
              <div style="font-size: 0.82rem; color: var(--text); white-space: pre-wrap;">${escapeHtml(sec.content)}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  const isOnlineResult = Boolean(payload.processing_mode === 'online' || (state.mode === 'online' && readableText));

  overviewOutput.innerHTML = `
    <div class="result-card hero-card">
      <div>
        <div class="result-eyebrow">Extraction overview</div>
        <h4>${escapeHtml(fileName)}${docTitle}</h4>
      </div>
      <div class="stats-grid">
        <div class="mini-stat">
          <span>Pages</span>
          <strong>${escapeHtml(pageCount)}</strong>
        </div>
        <div class="mini-stat">
          <span>${isOnlineResult ? 'Chars Recovered' : 'Chars'}</span>
          <strong>${escapeHtml(charCount)}</strong>
        </div>
        <div class="mini-stat">
          <span>Confidence</span>
          <strong>${Number(confidence).toFixed(1)}%</strong>
        </div>
        <div class="mini-stat">
          <span>Mode</span>
          <strong>${escapeHtml(modeLabel)}</strong>
        </div>
      </div>
    </div>

    ${isOnlineResult ? `
      <div class="result-card">
        ${buildSectionTitle('AI Restored Readable Text (Maximum Retrieval)')}
        ${docSummary}
        ${restoredTextMarkup}
        
        <details style="margin-top: 1.2rem; padding: 0.6rem 0.8rem; border-radius: 8px; background: rgba(0, 0, 0, 0.03); border: 1px solid rgba(0,0,0,0.06);">
          <summary style="cursor: pointer; font-size: 0.82rem; font-weight: 600; color: var(--muted); outline: none;">
            🔍 View Raw OCR Extracted Text (${extractedText.length} characters)
          </summary>
          <div style="margin-top: 0.75rem;">
            ${rawTextMarkup}
          </div>
        </details>
      </div>
      ${sectionsMarkup}
    ` : `
      <div class="result-card">
        ${buildSectionTitle('OCR Extracted Text')}
        ${rawTextMarkup}
      </div>
    `}
  `;
}

async function parseResume() {
const baseUrl = 'http://127.0.0.1:8000';

if (!state.file) {
  setStatus('warn', 'Please select a file before parsing.');
  return;
}

const endpoint = endpointForMode(state.mode);
const formData = new FormData();
formData.append('file', state.file);

if (parseButton) {
  parseButton.disabled = true;
  parseButton.textContent = 'Extracting...';
}

setStatus('neutral', 'Extracting text in progress. This may take a few moments.');

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
  renderResult(payload);
  updateFilePreview(state.file);
  setStatus('ok', 'Text extraction completed successfully.');
} catch (error) {
  const message = error && error.message ? error.message : 'Parsing failed.';
  setStatus('err', message);
  renderResult({ message, error: message });
} finally {
  if (parseButton) {
    parseButton.disabled = false;
    parseButton.textContent = 'Extract Text';
  }
}
}

function setStatus(type, message) {
if (!statusMessage) {
  return;
}

statusMessage.className = `status-message ${type}`;
statusMessage.textContent = message;
}

init();
