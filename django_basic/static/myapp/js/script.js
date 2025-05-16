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
        const spotCards = document.querySelectorAll('.spot-link');

        spotCards.forEach(card => {
            let spotTags = card.dataset.spotTags ? card.dataset.spotTags.split(',') : [];
            let spotMonths = card.dataset.spotMonths ? card.dataset.spotMonths.split(',') : [];

            const tagMatch = selectedTags.length === 0 || selectedTags.every(tagId => spotTags.includes(tagId));
            const monthMatch = selectedMonths.length === 0 || selectedMonths.every(monthId => spotMonths.includes(monthId));

            if (tagMatch && monthMatch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }


    