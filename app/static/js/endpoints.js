// Login JS
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
                window.location.href = '/'; // Change this to your desired redirect page
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

// Register
const registerForm = document.getElementById('registerForm');
if (registerForm) {

    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.password !== data.password2) {
            alert("Passwords do not match");
            return;
        }

        const payload = {
            email: data.email,
            username: data.username,
            first_name: data.firstname,
            last_name: data.lastname,
            role: 'admin',
            password: data.password,
            phone_number: '+52 (123)456-7890'
        };

        try {
            const response = await fetch('/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/auth/login';
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// Helper function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function logout() {
    // Get all cookies
    const cookies = document.cookie.split(";");

    // Iterate through all cookies and delete each one
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        // Set the cookie's expiry date to a past date to delete it
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }

    // Redirect to the login page
    window.location.href = '/auth/login';
};

/********** Add product ************/
const stockForm = document.getElementById('stockForm');
if (stockForm) {
    stockForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            name: data.name,
            unit: data.unit,
            quantity: data.quantity,
        };

        try {
            const response = await fetch('/stock', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                form.reset(); // Clear the form
                window.location.href = '/stock/stock'; // Redirect to the stock page
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

/********** Delete product ************/
const stockTable = document.getElementById('stockTable');

if (stockTable) {
    stockTable.addEventListener('click', async function (event) {

        if (event.target.className.includes('delete')) {
            const id = event.target.closest('tr').firstElementChild.textContent;

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                const response = await fetch(`/stock/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    // Handle success
                    window.location.href = '/stock/stock';
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        }
    });
}

/********** Add customer ************/
const customerForm = document.getElementById('customersForm');
if (customerForm) {
    customerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            first_name: data.firstname,
            last_name: data.lastname,
            birthday: data.birthday,
            phone_number: data.phone,
            address: data.address
        };

        try {
            const response = await fetch('/customers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                form.reset(); // Clear the form
                window.location.href = '/customers/customers'; // Redirect to the stock page
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

/********** Delete customer ************/
const customersTable = document.getElementById('customersTable');

if (customersTable) {
    customersTable.addEventListener('click', async function (event) {

        if (event.target.className.includes('delete')) {
            const id = event.target.closest('tr').firstElementChild.textContent;

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                const response = await fetch(`/customers/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    // Handle success
                    window.location.href = '/customers/customers';
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        }
    });
}

/********** Add barbers ************/
const barbersForm = document.getElementById('barbersForm');
if (barbersForm) {
    barbersForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            first_name: data.firstname,
            last_name: data.lastname,
            birthday: data.birthday
        };

        try {
            const response = await fetch('/barbers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                form.reset(); // Clear the form
                window.location.href = '/barbers/barbers'; // Redirect to the stock page
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

/********** Delete barber ************/
const barbersTable = document.getElementById('barbersTable');

if (barbersTable) {
    barbersTable.addEventListener('click', async function (event) {

        if (event.target.className.includes('delete')) {
            const id = event.target.closest('tr').firstElementChild.textContent;

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                const response = await fetch(`/barbers/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    // Handle success
                    window.location.href = '/barbers/barbers';
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        }
    });
}

/********** Add services ************/
const servicesForm = document.getElementById('servicesForm');
if (servicesForm) {
    servicesForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            name: data.name,
            price: data.price
        };

        try {
            const response = await fetch('/services', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('access_token')}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                form.reset(); // Clear the form
                window.location.href = '/services/services'; // Redirect to the stock page
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