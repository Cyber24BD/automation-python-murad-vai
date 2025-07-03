// Common fetch helper to include credentials and default headers
const apiFetch = (url, options = {}) => {
    const defaultHeaders = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
    };
    return fetch(url, {
        credentials: 'same-origin',
        ...options,
        headers: {
            ...defaultHeaders,
            ...(options.headers || {}),
        },
    }).then(res => res.json());
};

const API = {
    getItems: async (page = 1, pageSize = 20) => {
        return apiFetch(`/api/items?page=${page}&page_size=${pageSize}`);
    },
    searchItems: async (query, page = 1, pageSize = 20) => {
        return apiFetch(`/api/search?query=${query}&page=${page}&page_size=${pageSize}`);
    },
    addItem: async (itemData) => {
        return apiFetch('/add', {
            method: 'POST',
            body: itemData,
        });
    },
    updateItem: async (itemId, itemData) => {
        return apiFetch(`/update/${itemId}`, {
            method: 'POST',
            body: itemData,
        });
    },
    deleteItem: async (itemId) => {
        return apiFetch(`/delete/${itemId}`, {
            method: 'POST',
        });
    },
    deleteAllItems: async () => {
        return apiFetch('/delete-all', { method: 'POST' });
    }
};