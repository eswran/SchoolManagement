function toggleDetails(element) {

    const card = element.parentElement;

    // Close other opened cards
    document.querySelectorAll('.class-card').forEach(item => {

        if (item !== card) {
            item.classList.remove('active');
        }

    });

    // Open or close clicked card
    card.classList.toggle('active');

}