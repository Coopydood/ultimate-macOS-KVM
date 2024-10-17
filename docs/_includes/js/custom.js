onload = function() {
  // JavaScript to toggle between light and dark mode
  const toggleButton = document.getElementById('theme-toggle');
  const bodyElement = document.body;

  // Check for saved mode preference in localStorage
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme === 'light') {
    bodyElement.classList.toggle('light-mode');
  }

  // Toggle mode and save preference
  toggleButton.addEventListener('click', () => {
    bodyElement.classList.toggle('light-mode');
    
    const theme = bodyElement.classList.contains('light-mode') ? 'light' : 'dark';
    localStorage.setItem('theme', theme); // Save the preference
  });
}