// ==================== static/js/job-search.js ====================

// Job Search and Filter Functions

// Advanced search toggle
$('#advancedSearchToggle').on('click', function() {
    $('#advancedSearchPanel').slideToggle();
});

// Filter jobs by checkbox
$('.job-type-filter').on('change', function() {
    filterJobs();
});

function filterJobs() {
    const selectedTypes = [];
    $('.job-type-filter:checked').each(function() {
        selectedTypes.push($(this).val());
    });
    
    const experience = $('#experienceFilter').val();
    const location = $('#locationFilter').val();
    
    let url = '/jobs/?';
    if (selectedTypes.length > 0) {
        url += `job_type=${selectedTypes.join(',')}&`;
    }
    if (experience) {
        url += `experience=${experience}&`;
    }
    if (location) {
        url += `location=${location}&`;
    }
    
    window.location.href = url;
}

// Real-time job search
let searchTimeout;
$('#jobSearchInput').on('keyup', function() {
    clearTimeout(searchTimeout);
    const query = $(this).val();
    
    searchTimeout = setTimeout(function() {
        if (query.length >= 3) {
            searchJobs(query);
        }
    }, 500);
});

function searchJobs(query) {
    $.ajax({
        url: '/jobs/',
        type: 'GET',
        data: {
            'keyword': query
        },
        success: function(response) {
            // Update job listings
            $('#jobListings').html(response);
        }
    });
}

// Sort jobs
$('#sortSelect').on('change', function() {
    const sortBy = $(this).val();
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('sort', sortBy);
    window.location.href = currentUrl.toString();
});

// Salary range slider (if using range input)
$('#salaryRange').on('input', function() {
    const value = $(this).val();
    $('#salaryValue').text(`$${value}`);
});

// Resume upload validation
$('#resumeUpload').on('change', function() {
    const file = this.files[0];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (file) {
        // Check file size
        if (file.size > maxSize) {
            showToast('File size must be less than 5MB', 'danger');
            this.value = '';
            return;
        }
        
        // Check file type
        if (file.type !== 'application/pdf') {
            showToast('Only PDF files are allowed', 'danger');
            this.value = '';
            return;
        }
        
        showToast('Resume selected successfully', 'success');
    }
});

// Cover letter character counter
$('#coverLetter').on('input', function() {
    const length = $(this).val().length;
    const minLength = 100;
    
    $('#charCount').text(`${length} characters`);
    
    if (length < minLength) {
        $('#charCount').addClass('text-danger').removeClass('text-success');
    } else {
        $('#charCount').addClass('text-success').removeClass('text-danger');
    }
});

// Application form validation
$('#applicationForm').on('submit', function(e) {
    const coverLetter = $('#coverLetter').val();
    const resume = $('#resumeUpload').val();
    
    if (coverLetter.length < 100) {
        e.preventDefault();
        showToast('Cover letter must be at least 100 characters', 'danger');
        return false;
    }
    
    if (!resume) {
        e.preventDefault();
        showToast('Please upload your resume', 'danger');
        return false;
    }
    
    showLoading();
});

// Initialize on page load
$(document).ready(function() {
    // Initialize character counters
    setupCharCounter('coverLetter', 'charCount', 1000);
    
    // Initialize admin charts if on admin page
    if ($('#applicationsChart').length > 0) {
        initAdminCharts();
    }
});

// Scroll to top button
$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('#scrollToTop').fadeIn();
    } else {
        $('#scrollToTop').fadeOut();
    }
});

$('#scrollToTop').click(function() {
    scrollToTop();
});

// Add scroll to top button HTML if not exists
$(document).ready(function() {
    if ($('#scrollToTop').length === 0) {
        $('body').append(`
            <button id="scrollToTop" class="btn btn-primary position-fixed bottom-0 end-0 m-4" style="display: none; z-index: 1000;">
                <i class="fas fa-arrow-up"></i>
            </button>
        `);
    }
});
