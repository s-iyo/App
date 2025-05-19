let selectedTags = [];
let selectedMonths = [];

function toggleTag(button) {
    const tagId = button.dataset.tagId;
    const index = selectedTags.indexOf(tagId);

    if (index === -1) {
        selectedTags.push(tagId);
        button.classList.add('selected');
    } else {
        selectedTags.splice(index, 1);
        button.classList.remove('selected');
    }

    filterSpots();
}

function toggleMonth(button) {
    const monthId = button.dataset.monthId;
    const index = selectedMonths.indexOf(monthId);

    if (index === -1) {
        selectedMonths.push(monthId);
        button.classList.add('selected');
    } else {
        selectedMonths.splice(index, 1);
        button.classList.remove('selected');
    }

    filterSpots();
}

function filterSpots() {
    const spotCards = document.querySelectorAll('.card'); // セレクタを修正
    spotCards.forEach(card => {
        let spotTags = card.dataset.spotTags ? card.dataset.spotTags.split(',') : [];
        let spotMonths = card.dataset.spotMonths ? card.dataset.spotMonths.split(',') : [];
        const tagMatch = selectedTags.length === 0 || selectedTags.every(tagId => spotTags.includes(String(tagId))); // タグのIDを文字列として比較
        const monthMatch = selectedMonths.length === 0 || selectedMonths.every(monthId => spotMonths.includes(String(monthId))); // 月のIDを文字列として比較
        if (tagMatch && monthMatch) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-button');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const spotId = this.dataset.spotId;
            const icon = this.querySelector('i');
            fetch(`/myapp/spot/${spotId}/toggle_favorite/`)
                .then(response => response.json())
                .then(data => {
                    if (data.is_favorite) {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        icon.style.color = 'gold';
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        icon.style.color = 'gray';
                    }
                });
        });
    });
});
