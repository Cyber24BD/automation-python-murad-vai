document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners to all edit forms
    document.querySelectorAll('.edit-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const itemId = form.dataset.itemId;
            const formData = new FormData(form);
            
            try {
                const response = await fetch(`/update/${itemId}`, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const updatedItem = await response.json();
                    const successAlert = form.querySelector('.alert-success');
                    successAlert.classList.remove('d-none');

                    // Update the table row with the new data
                    const row = document.querySelector(`#row-${itemId}`);
                    if (row) {
                        row.querySelector('.item-name').textContent = updatedItem.name;
                        row.querySelector('.item-description').textContent = updatedItem.description;
                        row.querySelector('.item-price').textContent = updatedItem.price;
                        row.querySelector('.item-th-level').textContent = updatedItem.town_hall_level;
                    }

                    // Hide the modal and the alert after a short delay
                    setTimeout(() => {
                        const modalElement = form.closest('.modal');
                        const modal = bootstrap.Modal.getInstance(modalElement);
                        modal.hide();
                        successAlert.classList.add('d-none');
                    }, 1500);

                } else {
                    alert('Failed to save changes. Please try again.');
                }
            } catch (error) {
                console.error('An error occurred:', error);
                alert('An error occurred while saving changes.');
            }
        });
    });
});
