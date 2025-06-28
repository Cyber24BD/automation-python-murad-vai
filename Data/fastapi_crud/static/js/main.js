document.addEventListener('DOMContentLoaded', () => {
    // --- MODAL HANDLING ---
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
            document.body.classList.add('modal-open');
        }
    }

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            document.body.classList.remove('modal-open');
        }
    }

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                closeModal(openModal.id);
            }
        }
    });
    
    // Close modal on backdrop click
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-backdrop')) {
            const modal = e.target.closest('.modal');
            if (modal) {
                closeModal(modal.id);
            }
        }
    });

    // --- NOTIFICATIONS ---
    window.showNotification = function(message, type = 'info') {
        const notification = document.createElement('div');
        const typeClasses = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500'
        };
        const typeIcon = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            info: 'fa-info-circle'
        }
        
        notification.className = `fixed top-20 right-4 z-[1050] p-4 rounded-lg shadow-lg text-white ${typeClasses[type]} transition-all duration-300 transform translate-x-full`;
        notification.innerHTML = `<i class="fas ${typeIcon[type]} mr-2"></i>${message}`;
        document.body.appendChild(notification);

        setTimeout(() => notification.classList.remove('translate-x-full'), 100);
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // --- API & FORM HANDLING ---

    // EDIT ITEM
    document.querySelectorAll('.edit-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const itemId = form.dataset.itemId;
            const formData = new FormData(form);
            
            try {
                const response = await fetch(`/update/${itemId}`, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' },
                    body: formData
                });
                const result = await response.json();

                if (result.success) {
                    const row = document.querySelector(`#row-${itemId}`);
                    if (row) {
                        row.querySelector('.item-name').textContent = result.name;
                        row.querySelector('.item-description').textContent = result.description;
                        row.querySelector('.item-price').textContent = '$' + result.price;
                        row.querySelector('.item-th-level').textContent = 'Level ' + result.town_hall_level;
                    }
                    closeModal(`editModal${itemId}`);
                    // No success message as requested, just close the modal.
                } else {
                    showNotification(result.message || 'Error updating item.', 'error');
                }
            } catch (error) {
                showNotification('An error occurred while updating.', 'error');
            }
        });
    });

    // ADD ITEM
    const addItemForm = document.getElementById('addItemForm');
    if(addItemForm) {
        addItemForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addItemForm);
            try {
                const response = await fetch('/add', {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' },
                    body: formData
                });
                const result = await response.json();
                if (result.success) {
                    closeModal('addItemModal');
                    showNotification('Item added successfully!', 'success');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(result.message || 'Error adding item.', 'error');
                }
            } catch (error) {
                showNotification('An error occurred while adding the item.', 'error');
            }
        });
    }

    // DELETE ITEM (single)
    window.deleteItem = async function(itemId) {
        if (!confirm('Are you sure you want to delete this item?')) return;
        
        try {
            const response = await fetch(`/delete/${itemId}`, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' }
            });
            const result = await response.json();
            if (result.success) {
                document.querySelector(`#row-${itemId}`).remove();
                showNotification('Item deleted!', 'success');
            } else {
                showNotification(result.message || 'Error deleting item.', 'error');
            }
        } catch (error) {
            showNotification('An error occurred while deleting.', 'error');
        }
    }

    // DELETE ALL ITEMS
    window.deleteAllItems = async function() {
        try {
            const response = await fetch('/delete-all', {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' }
            });
            const result = await response.json();
            if (result.success) {
                closeModal('deleteAllModal');
                showNotification('All items have been deleted.', 'success');
                setTimeout(() => window.location.reload(), 1000);
            } else {
                showNotification(result.message || 'Error deleting all items.', 'error');
            }
        } catch (error) {
            showNotification('An error occurred while deleting all items.', 'error');
        }
    }
    
    // --- MOBILE MENU ---
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if(menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // --- SEARCH ---
    const searchInput = document.getElementById('searchInput');
    if(searchInput) {
        const tableBody = document.getElementById('itemsTableBody');
        const rows = Array.from(tableBody.querySelectorAll('tr'));

        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase().trim();
            rows.forEach(row => {
                const textContent = row.textContent.toLowerCase();
                row.style.display = textContent.includes(searchTerm) ? '' : 'none';
            });
        });
    }
});