const ACCESS_PASSWORD = 'tvcabbage';
const ACCESS_KEY = 'tvcabbage-access';
const gate = document.querySelector('#password-gate');
const passwordForm = document.querySelector('#password-form');
const passwordInput = document.querySelector('#site-password');
const passwordError = document.querySelector('#password-error');

function unlockArchive() {
  gate.hidden = true;
  document.body.classList.remove('is-locked');
}

if (sessionStorage.getItem(ACCESS_KEY) === 'granted') {
  unlockArchive();
} else {
  document.body.classList.add('is-locked');
  passwordInput.focus();
}

passwordForm.addEventListener('submit', (event) => {
  event.preventDefault();
  if (passwordInput.value === ACCESS_PASSWORD) {
    sessionStorage.setItem(ACCESS_KEY, 'granted');
    passwordError.hidden = true;
    unlockArchive();
    return;
  }
  passwordError.hidden = false;
  passwordInput.select();
});

const state = {
  rows: [],
  localPosts: new Map(),
  query: '',
  year: 'all'
};

const list = document.querySelector('#archive-list');
const resultCount = document.querySelector('#result-count');
const captureCount = document.querySelector('#capture-count');
const search = document.querySelector('#search');
const yearFilter = document.querySelector('#year-filter');
const clearFilters = document.querySelector('#clear-filters');

function titleFromUrl(url) {
  const path = new URL(url).pathname;
  const slug = path.split('/').filter(Boolean).pop() || 'TV Cabbage homepage';
  if (slug === 'index.html') return 'TV Cabbage homepage';
  return decodeURIComponent(slug.replace(/\.html$/, '').replace(/[-_]+/g, ' '))
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function archiveUrl(row) {
  if (row[5] === 'source') return row[1];
  return `https://web.archive.org/web/${row[0]}id_/${row[1]}`;
}

function pathKey(url) {
  return new URL(url).pathname.replace(/\/$/, '') || '/';
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[character]));
}

function displayDate(timestamp) {
  const date = new Date(`${timestamp.slice(0, 4)}-${timestamp.slice(4, 6)}-${timestamp.slice(6, 8)}T00:00:00Z`);
  return Number.isNaN(date.getTime()) ? timestamp : new Intl.DateTimeFormat('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric'
  }).format(date);
}

function renderYears() {
  const years = [...new Set(state.rows.map((row) => row[0].slice(0, 4)))].sort().reverse();
  yearFilter.innerHTML = '<option value="all">All years</option>';
  years.forEach((year) => {
    const option = document.createElement('option');
    option.value = year;
    option.textContent = year;
    yearFilter.append(option);
  });
}

function filteredRows() {
  return state.rows.filter((row) => {
    const haystack = `${titleFromUrl(row[1])} ${row[1]}`.toLowerCase();
    const matchesQuery = !state.query || haystack.includes(state.query);
    const matchesYear = state.year === 'all' || row[0].startsWith(state.year);
    return matchesQuery && matchesYear;
  });
}

function render() {
  const rows = filteredRows();
  resultCount.textContent = rows.length.toLocaleString('en-GB');
  list.innerHTML = '';
  if (!rows.length) {
    list.innerHTML = '<p class="empty-state">No source records match that search.</p>';
    return;
  }
  rows.forEach((row, index) => {
    const item = document.createElement('article');
    item.className = 'archive-item';
    item.style.animationDelay = `${Math.min(index, 12) * 24}ms`;
    const originalUrl = row[1];
    const localPost = state.localPosts.get(pathKey(originalUrl));
    const title = localPost ? localPost.title : titleFromUrl(originalUrl);
    const localUrl = localPost ? `posts/${encodeURIComponent(localPost.file.replace(/\.md$/, '.html'))}` : archiveUrl(row);
    item.innerHTML = `
      <time class="archive-date" datetime="${row[0].slice(0, 8)}">${displayDate(row[0])}</time>
      <div>
        <div class="archive-title"><a href="${localUrl}" ${localPost ? '' : 'rel="noreferrer"'}>${escapeHtml(title)}</a></div>
        <div class="archive-path">${escapeHtml(originalUrl)}${localPost ? ' · local copy available' : ''}</div>
      </div>
      <div class="archive-actions">
        ${localPost ? `<a class="archive-link archive-local" href="${localUrl}">Read locally <span aria-hidden="true">→</span></a>` : ''}
        <a class="archive-link" href="${archiveUrl(row)}" rel="noreferrer">${row[5] === 'source' ? 'Open source' : 'Open capture'} <span aria-hidden="true">↗</span></a>
      </div>
    `;
    list.append(item);
  });
}

async function loadArchive() {
  try {
    const [response, localResponse] = await Promise.all([
      fetch('data/wayback-cdx.json'),
      fetch('content/posts/index.json')
    ]);
    if (!response.ok) throw new Error(`Archive index returned ${response.status}`);
    const data = await response.json();
    if (localResponse.ok) {
      const localPosts = await localResponse.json();
      state.localPosts = new Map(localPosts.map((post) => [pathKey(post.original_url), post]));
      const indexedPaths = new Set(data.slice(1).map((row) => pathKey(row[1])));
      localPosts.forEach((post) => {
        const path = pathKey(post.original_url);
        if (!indexedPaths.has(path)) {
          const timestamp = post.published.replace(/\D/g, '').slice(0, 14).padEnd(14, '0');
          data.push([timestamp, post.original_url, '200', 'text/html', '', 'source']);
        }
      });
    }
    state.rows = data.slice(1).sort((a, b) => b[0].localeCompare(a[0]));
    captureCount.textContent = state.rows.length.toLocaleString('en-GB');
    renderYears();
    render();
  } catch (error) {
    captureCount.textContent = '—';
    resultCount.textContent = 'No';
    list.innerHTML = `<p class="empty-state error-state">The source index could not be loaded. ${error.message}</p>`;
  }
}

search.addEventListener('input', (event) => {
  state.query = event.target.value.trim().toLowerCase();
  render();
});
yearFilter.addEventListener('change', (event) => {
  state.year = event.target.value;
  render();
});
clearFilters.addEventListener('click', () => {
  state.query = '';
  state.year = 'all';
  search.value = '';
  yearFilter.value = 'all';
  render();
});

loadArchive();
