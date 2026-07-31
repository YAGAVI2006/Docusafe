const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    
    // Login Handling
    const loginForm = document.getElementById('loginForm');
    if(loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const alertBox = document.getElementById('loginAlert');
            
            try {
                const res = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await res.json();
                if(res.ok) {
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    if(data.user.role === 'admin') {
                        window.location.href = 'admin.html';
                    } else {
                        window.location.href = 'dashboard.html';
                    }
                } else {
                    alertBox.textContent = data.message || 'Login failed';
                    alertBox.classList.remove('d-none');
                }
            } catch(err) {
                console.error(err);
                alertBox.textContent = 'Server error';
                alertBox.classList.remove('d-none');
            }
        });
    }

    // Register Handling
    const regForm = document.getElementById('regForm');
    if(regForm) {
        regForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const full_name = document.getElementById('fullName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            const alertBox = document.getElementById('regAlert');
            
            try {
                const res = await fetch(`${API_URL}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, full_name })
                });
                
                const data = await res.json();
                if(res.ok) {
                    window.location.href = 'index.html';
                } else {
                    alertBox.textContent = data.message || 'Registration failed';
                    alertBox.classList.remove('d-none');
                }
            } catch(err) {
                console.error(err);
                alertBox.textContent = 'Server error';
                alertBox.classList.remove('d-none');
            }
        });
    }
});
