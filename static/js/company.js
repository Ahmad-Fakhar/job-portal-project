// ==================== static/js/company.js ====================

// Company Dashboard Specific Functions

// Delete Job Confirmation
function deleteJob(jobId) {
    if (confirmDelete('Are you sure you want to delete this job posting?')) {
        showLoading();
        $.ajax({
            url: `/company/jobs/${jobId}/delete/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function() {
                showToast('Job deleted successfully', 'success');
                setTimeout(() => {
                    window.location.href = '/company/jobs/';
                }, 1000);
            },
            error: function() {
                hideLoading();
                showToast('Error deleting job', 'danger');
            }
        });
    }
}

// Update Application Status
function updateApplicationStatus(applicationId, status) {
    $.ajax({
        url: `/company/applications/${applicationId}/update-status/`,
        type: 'POST',
        data: {
            'status': status,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function() {
            showToast('Application status updated', 'success');
            location.reload();
        },
        error: function() {
            showToast('Error updating status', 'danger');
        }
    });
}

// Status change dropdown
$(document).on('change', '.status-select', function() {
    const applicationId = $(this).data('application-id');
    const newStatus = $(this).val();
    
    if (confirm('Are you sure you want to change the status?')) {
        updateApplicationStatus(applicationId, newStatus);
    } else {
        $(this).val($(this).data('original-status'));
    }
});

// Preview company logo before upload
$('#companyLogo').on('change', function() {
    previewImage(this, 'logoPreview');
});

// Job form validation
function validateJobForm() {
    const salaryMin = parseFloat($('#id_salary_min').val());
    const salaryMax = parseFloat($('#id_salary_max').val());
    
    if (salaryMax < salaryMin) {
        showToast('Maximum salary must be greater than minimum salary', 'danger');
        return false;
    }
    
    const deadline = new Date($('#id_deadline').val());
    const today = new Date();
    
    if (deadline < today) {
        showToast('Deadline must be in the future', 'danger');
        return false;
    }
    
    return true;
}

// Add notes to application
function addApplicationNote(applicationId) {
    const note = prompt('Add a note for this application:');
    if (note) {
        $.ajax({
            url: `/company/applications/${applicationId}/add-note/`,
            type: 'POST',
            data: {
                'note': note,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function() {
                showToast('Note added successfully', 'success');
                location.reload();
            },
            error: function() {
                showToast('Error adding note', 'danger');
            }
        });
    }
}
