  function toggleDropdown() {
    const dropdown = document.getElementById('dropdown');
    if (dropdown.classList.contains('hidden')) {
      dropdown.classList.remove('hidden');
    } else {
      dropdown.classList.add('hidden');
    }
  }

  document.addEventListener('click', function(e) {
    const dropdown = document.getElementById("dropdown");
    const button = document.querySelector(".drop-button");
    if (!dropdown.contains(e.target) && !button.contains(e.target)) {
      dropdown.classList.add("hidden");
    }
  });
