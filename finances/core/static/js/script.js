// Logout button action
document.addEventListener('DOMContentLoaded', function() {
	const logoutBtn = document.querySelector('.logout-btn');
	if (logoutBtn) {
		logoutBtn.addEventListener('click', function() {
			window.location.href = '/accounts/logout/';
		});
	}
});
