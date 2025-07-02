const API = {
    getItems: async (page = 1, pageSize = 20) => {
        const response = await fetch(`/api/items?page=${page}&page_size=${pageSize}`);
        return response.json();
    },
    searchItems: async (query, page = 1, pageSize = 20) => {
        const response = await fetch(`/api/search?query=${query}&page=${page}&page_size=${pageSize}`);
        return response.json();
    },
    addItem: async (itemData) => {
        const response = await fetch('/add', {
            method: 'POST',
            body: itemData,
        });
        return response.json();
    },
    updateItem: async (itemId, itemData) => {
        const response = await fetch(`/update/${itemId}`, {
            method: 'POST',
            body: itemData,
        });
        return response.json();
    },
    deleteItem: async (itemId) => {
        const response = await fetch(`/delete/${itemId}`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        return response.json();
    },
    deleteAllItems: async () => {
        const response = await fetch('/delete-all', {
            method: 'POST',
        });
        return response.json();
    }
};