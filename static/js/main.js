document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input[type="password"]').forEach(input => {
    // Wrap the input
    const wrapper = document.createElement('div');
    wrapper.className = 'password-wrapper';
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    // Insert the toggle button
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'toggle-password';
    btn.textContent = '👁️';
    wrapper.appendChild(btn);

    // Hook up the click
    btn.addEventListener('click', () => {
      if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = '🙈';
      } else {
        input.type = 'password';
        btn.textContent = '👁️';
      }
    });
  });
});
