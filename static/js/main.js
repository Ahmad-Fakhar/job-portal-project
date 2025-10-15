// ==================== static/js/main.js ====================

// Global CSRF Token Setup for AJAX
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
}

const csrftoken = getCookie('csrftoken');

// Setup AJAX with CSRF token
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Toast Notifications
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const div = document.createElement('div');
    div.innerHTML = toastHtml;
    document.getElementById('toastContainer').appendChild(div);
    
    const toast = new bootstrap.Toast(div.querySelector('.toast'));
    toast.show();
    
    setTimeout(() => {
        div.remove();
    }, 5000);
}

// Save/Unsave Job (AJAX)
function saveJob(jobId) {
    $.ajax({
        url: `/save-job/${jobId}/`,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            const btn = $(`.save-job[data-job-id="${jobId}"]`);
            if (response.saved) {
                btn.html('<i class="fas fa-heart"></i> Saved');
                btn.removeClass('btn-outline-danger').addClass('btn-danger');
                showToast('Job saved successfully!', 'success');
            } else {
                btn.html('<i class="far fa-heart"></i> Save');
                btn.removeClass('btn-danger').addClass('btn-outline-danger');
                showToast('Job removed from saved list', 'info');
            }
        },
        error: function() {
            showToast('Error saving job. Please try again.', 'danger');
        }
    });
}

// Attach save job event to buttons
$(document).on('click', '.save-job', function() {
    const jobId = $(this).data('job-id');
    saveJob(jobId);
});

// Confirm Dialog for Delete Actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this? This action cannot be undone.');
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Auto-dismiss alerts
$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show scroll to top button
$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('#scrollToTop').fadeIn();
    } else {
        $('#scrollToTop').fadeOut();
    }
});

// Initialize tooltips
$(document).ready(function() {
    $('[data-bs-toggle="tooltip"]').tooltip();
});

// Character counter for textareas
function setupCharCounter(textareaId, counterId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    
    if (textarea && counter) {
        textarea.addEventListener('input', function() {
            const length = this.value.length;
            counter.textContent = `${length}/${maxLength}`;
            
            if (length > maxLength) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    }
}

// File upload preview
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(previewId).src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.innerHTML = `
        <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    overlay.style.zIndex = '9999';
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}
