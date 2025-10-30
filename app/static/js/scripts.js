/********* Add modal *********/
const addIcon = document.getElementById('addIcon');
const addModal = document.getElementById('addModal');
const backgroundModal = document.getElementById('backgroundModal');

if(addIcon) {
    addIcon.addEventListener('click', async function (event) {
        backgroundModal.style.display = 'block';
    });
}

if(backgroundModal) {
    backgroundModal.addEventListener('click', async function (event) {
        if (!addModal.contains(event.target)) {
            backgroundModal.style.display = 'none';
            return;
        }
    });
}

/********** Login *************/
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        const payload = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            payload.append(key, value);
        }

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (response.ok) {
                // Handle success (e.g., redirect to dashboard)
                const data = await response.json();
                // Delete any cookies available
                logout();
                // Save token to cookie
                document.cookie = `access_token=${data.access_token}; path=/`;
                window.location.href = '/home'; // Change this to your desired redirect page
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}