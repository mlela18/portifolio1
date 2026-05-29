// Dynamically set API base URL based on environment
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  window.API_BASE = 'http://localhost:5000/api';
} else {
  // Production: replace with your Render backend URL
  window.API_BASE = 'https://your-backend-name.onrender.com/api';
}
