document.addEventListener('DOMContentLoaded', () => {
    const passwordForm = document.getElementById('passwordForm');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('errorMessage');

    // Check if already authenticated
    const authTimestamp = localStorage.getItem('authTimestamp');
    if (authTimestamp) {
        const oneDay = 24 * 60 * 60 * 1000;
        if (Date.now() - parseInt(authTimestamp, 10) < oneDay) {
            window.location.href = '/';
        }
    }

    passwordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const password = passwordInput.value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password }),
            });

            if (response.ok) {
                localStorage.setItem('authTimestamp', Date.now().toString());
                window.location.href = '/';
            } else {
                const data = await response.json();
                errorMessage.textContent = data.detail || 'Incorrect password. Please try again.';
                errorMessage.classList.remove('hidden');
            }
        } catch (error) {
            errorMessage.textContent = 'An error occurred. Please try again later.';
            errorMessage.classList.remove('hidden');
        }
    });
});