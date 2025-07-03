let currentPage = 1;
const pageSize = 20;
let currentSearchQuery = '';

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent click from bubbling to document
            mobileMenu.classList.toggle('hidden');
            const icon = mobileMenuButton.querySelector('i');
            if (icon) {
                if (mobileMenu.classList.contains('hidden')) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                } else {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                }
            }
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.classList.contains('hidden') && !mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                mobileMenu.classList.add('hidden');
                const icon = mobileMenuButton.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
    
    fetchItems(currentPage);

    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {
        currentSearchQuery = e.target.value;
        fetchItems(1, currentSearchQuery);
    });

    const addItemForm = document.getElementById('addItemForm');
    const addItemError = document.getElementById('addItemError');

        addItemForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(addItemForm);

        // Close the modal immediately.
        closeModal('addItemModal');

        // Submit the form in the background.
        API.addItem(formData).then(response => {
            if (response.success) {
                // Refresh the list and show a success message.
                fetchItems(currentPage, currentSearchQuery);
                UI.showToast('Item added successfully!', 'success');
                addItemForm.reset();
            } else {
                // Show an error message.
                const message = response.message || 'An unexpected error occurred.';
                UI.showToast(message, 'error');
            }
        });
        
        // Clear any previous error messages in the modal.
        if (addItemError) {
            addItemError.textContent = '';
        }
    });

    document.getElementById('editModalContainer').addEventListener('submit', async (e) => {
        if (e.target.classList.contains('edit-form')) {
            e.preventDefault();
            const itemId = e.target.dataset.itemId;
            const formData = new FormData(e.target);
            const response = await API.updateItem(itemId, formData);
            if (response.success) {
                closeModal(`editModal${itemId}`);
                fetchItems(currentPage, currentSearchQuery);
            } else {
                alert(response.message);
            }
        }
    });
});

async function fetchItems(page, query = '') {
    currentPage = page;
    currentSearchQuery = query;
    const data = query ? await API.searchItems(query, page, pageSize) : await API.getItems(page, pageSize);
    UI.renderItems(data.items);
    UI.renderPagination(Math.ceil(data.total_items / pageSize), page, fetchItems);
}

function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item?')) {
        API.deleteItem(itemId).then(response => {
            if (response.success) {
                fetchItems(currentPage, currentSearchQuery);
            } else {
                alert(response.message);
            }
        });
    }
}

function deleteAllItems() {
    if (confirm('Are you sure you want to delete all items?')) {
        API.deleteAllItems().then(response => {
            if (response.success) {
                fetchItems(1);
            } else {
                alert(response.message);
            }
        });
    }
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('show');
    document.body.classList.add('modal-open');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
    document.body.classList.remove('modal-open');
}

function createEditModal(item) {
    return `
    <div id="editModal${item.id}" class="modal">
        <div class="modal-backdrop" onclick="closeModal('editModal${item.id}')"></div>
        <div class="modal-content bg-white rounded-xl shadow-2xl max-w-4xl w-full mx-4">
            <div class="flex items-center justify-between p-6 border-b border-gray-200">
                <h3 class="text-xl font-semibold text-gray-900 flex items-center">
                    <i class="fas fa-edit mr-2 text-primary"></i>Edit Item #${item.id}
                </h3>
                <button onclick="closeModal('editModal${item.id}')" class="text-gray-400 hover:text-gray-600 transition-colors">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            
            <div class="p-6">
                <form class="edit-form space-y-6" data-item-id="${item.id}">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Name</label>
                            <input type="text" name="name" value="${item.name}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Price</label>
                            <input type="text" name="price" value="${item.price}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                        <textarea name="description" rows="3" 
                                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">${item.description}</textarea>
                    </div>
                    
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Town Hall Level</label>
                            <input type="text" name="town_hall_level" value="${item.town_hall_level}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">King Level</label>
                            <input type="text" name="king_level" value="${item.king_level}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Queen Level</label>
                            <input type="text" name="queen_level" value="${item.queen_level}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Warden Level</label>
                            <input type="text" name="warden_level" value="${item.warden_level}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Champion Level</label>
                            <input type="text" name="champion_level" value="${item.champion_level}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Media URL 1</label>
                            <input type="text" name="media1" value="${item.media.media1 || ''}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Media URL 2 (Optional)</label>
                            <input type="text" name="media2" value="${item.media.media2 || ''}" 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Media URL 3 (Optional)</label>
                        <input type="text" name="media3" value="${item.media.media3 || ''}" 
                               class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200">
                    </div>
                    
                    <div class="flex justify-end space-x-4 pt-4">
                        <button type="button" onclick="closeModal('editModal${item.id}')" 
                                class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                            Cancel
                        </button>
                        <button type="submit" 
                                class="px-6 py-3 bg-primary text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 flex items-center">
                            <i class="fas fa-save mr-2"></i>Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    `;
}
