// ==================== static/js/admin.js ====================

// Admin Dashboard Specific Functions

// Approve Company
function approveCompany(companyId) {
    if (confirm('Are you sure you want to approve this company?')) {
        showLoading();
        window.location.href = `/admin-panel/companies/${companyId}/approve/`;
    }
}

// Reject Company
function rejectCompany(companyId) {
    const reason = prompt('Please enter the reason for rejection:');
    if (reason) {
        showLoading();
        $.ajax({
            url: `/admin-panel/companies/${companyId}/reject/`,
            type: 'POST',
            data: {
                'reason': reason,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function() {
                showToast('Company rejected successfully', 'success');
                location.reload();
            },
            error: function() {
                hideLoading();
                showToast('Error rejecting company', 'danger');
            }
        });
    }
}

// Deactivate Job
function deactivateJob(jobId) {
    if (confirm('Are you sure you want to deactivate this job?')) {
        $.ajax({
            url: `/admin-panel/jobs/${jobId}/deactivate/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function() {
                showToast('Job deactivated successfully', 'success');
                location.reload();
            },
            error: function() {
                showToast('Error deactivating job', 'danger');
            }
        });
    }
}

// Filter Companies
function filterCompanies() {
    const status = document.getElementById('statusFilter').value;
    const search = document.getElementById('searchInput').value;
    
    let url = '/admin-panel/companies/?';
    if (status) url += `status=${status}&`;
    if (search) url += `search=${search}&`;
    
    window.location.href = url;
}

// Chart.js Dashboard Charts (if Chart.js is included)
function initAdminCharts() {
    // Applications Over Time Chart
    const ctx1 = document.getElementById('applicationsChart');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Applications',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: 'rgb(37, 99, 235)',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    }
    
    // Jobs by Category Chart
    const ctx2 = document.getElementById('jobsCategoryChart');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Security Guard', 'Security Manager', 'Security Officer', 'Others'],
                datasets: [{
                    data: [30, 20, 25, 15],
                    backgroundColor: [
                        'rgb(37, 99, 235)',
                        'rgb(16, 185, 129)',
                        'rgb(245, 158, 11)',
                        'rgb(239, 68, 68)'
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });
    }
}

