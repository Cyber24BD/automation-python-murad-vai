const UI = {
    renderItems: (items) => {
        const itemsTableBody = document.getElementById('itemsTableBody');
        itemsTableBody.innerHTML = '';
        items.forEach(item => {
            const row = `
                <tr id="row-${item.id}" class="hover:bg-gray-50 transition-colors duration-200">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="truncate-custom item-name text-sm text-gray-900 font-medium" title="${item.name}">${item.name}</div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="truncate-custom item-description text-sm text-gray-600" title="${item.description}">${item.description}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="item-price text-sm font-semibold text-green-600">$${item.price}</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="item-th-level inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            Level ${item.town_hall_level}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button onclick="openModal('editModal${item.id}')" 
                                class="bg-secondary hover:bg-gray-600 text-white px-3 py-1.5 rounded-lg transition-colors duration-200 text-xs">
                            <i class="fas fa-edit mr-1"></i>Edit
                        </button>
                        <button onclick="deleteItem(${item.id})" 
                                class="bg-danger hover:bg-red-600 text-white px-3 py-1.5 rounded-lg transition-colors duration-200 text-xs">
                            <i class="fas fa-trash mr-1"></i>Delete
                        </button>
                    </td>
                </tr>
            `;
            itemsTableBody.innerHTML += row;
            document.getElementById('editModalContainer').innerHTML += createEditModal(item);
        });
    },
    renderPagination: (totalPages, currentPage, onPageClick) => {
        const paginationContainer = document.getElementById('pagination-container');
        paginationContainer.innerHTML = '';

        const prevButton = document.createElement('button');
        prevButton.className = `px-4 py-2 mx-1 rounded-md ${
            currentPage === 1 
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed' 
                : 'bg-blue-500 text-white hover:bg-blue-600'
        } transition-colors duration-200`;
        prevButton.innerText = 'Previous';
        prevButton.disabled = currentPage === 1;
        prevButton.addEventListener('click', () => onPageClick(currentPage - 1));
        paginationContainer.appendChild(prevButton);

        const pageInfo = document.createElement('span');
        pageInfo.className = 'mx-4 text-gray-700 font-medium';
        pageInfo.innerText = `Page ${currentPage} of ${totalPages}`;
        paginationContainer.appendChild(pageInfo);

        const nextButton = document.createElement('button');
        nextButton.className = `px-4 py-2 mx-1 rounded-md ${
            currentPage === totalPages 
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed' 
                : 'bg-blue-500 text-white hover:bg-blue-600'
        } transition-colors duration-200`;
        nextButton.innerText = 'Next';
        nextButton.disabled = currentPage === totalPages;
        nextButton.addEventListener('click', () => onPageClick(currentPage + 1));
        paginationContainer.appendChild(nextButton);
    }
};