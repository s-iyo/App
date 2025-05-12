document.addEventListener('DOMContentLoaded', function() {
    const folderToggles = document.querySelectorAll('.folder-toggle');

    folderToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const folderItem = this.parentNode;
            folderItem.classList.toggle('expanded');
        });
    });
});