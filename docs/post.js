const ACCESS_PASSWORD = 'tvcabbage';
const gate = document.querySelector('#password-gate');
const form = document.querySelector('#password-form');
const input = document.querySelector('#site-password');
const error = document.querySelector('#password-error');

function unlock() {
  gate.hidden = true;
  document.body.classList.remove('is-locked');
}

if (sessionStorage.getItem('tvcabbage-access') === 'granted') {
  unlock();
} else {
  document.body.classList.add('is-locked');
  input.focus();
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  if (input.value === ACCESS_PASSWORD) {
    sessionStorage.setItem('tvcabbage-access', 'granted');
    error.hidden = true;
    unlock();
  } else {
    error.hidden = false;
    input.select();
  }
});
