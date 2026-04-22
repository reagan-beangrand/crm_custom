/**
        * Page Switching Logic
        * @param {string} pageId - The ID of the view to show
        * @param {HTMLElement} element - The clicked element to set active state
*/
function showPage(pageId, element) {
    // 1. Switch visibility of page sections
    document.querySelectorAll('.page-view').forEach(view => {
        view.classList.remove('active');
    });
    const selectedView = document.getElementById(pageId + '-view');
    if (selectedView) {
        selectedView.classList.add('active');
    }

    // 2. Clear all active styles from navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // 3. Set the clicked element as active if it's a nav-link
    if (element && element.classList.contains('nav-link')) {
        element.classList.add('active');
    }
    // Fallback: If clicked on Logo or Home link specifically
    else if (pageId === 'home') {
        const homeLink = document.querySelector('.nav-link[onclick*="home"]');
        if (homeLink) homeLink.classList.add('active');
    }

    // 4. Smooth scroll to top if we switched views
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Close mobile menu if open
    const navbarCollapse = document.getElementById('navbarNav');
    if (navbarCollapse.classList.contains('show')) {
        new bootstrap.Collapse(navbarCollapse).hide();
    }
}

// Contact Form Handling
function handleContact(event) {
    event.preventDefault();
    const firstname = document.getElementById('firstName').value;
    const lastname = document.getElementById('lastName').value;
    const mobileNo = document.getElementById('mobileNo').value;
    const gender = document.getElementById('gender').value;
    const container = document.getElementById('contact-form-container');

    const errorMessage = `
            <div class="text-center h-100 d-flex flex-column justify-content-center align-items-center p-4 bg-light rounded-4">
                <i class="fas fa-times-circle text-danger mb-3" style="font-size: 4rem;"></i>
                <h3 class="h4 mb-3">Submission Failed</h3>
                <p class="text-muted mb-4">Sorry, there was an issue sending your message. Please try again later.</p>
                <button onclick="location.reload()" class="btn btn-outline-secondary rounded-pill px-4">Try Again</button>
            </div>
        `;
    frappe.call({
        method: "crm_custom.custom.custom_api.create_lead_api", //dotted path to server method
        args: {
            firstname: firstname,
            lastname: lastname,
            mobileNo: mobileNo,
            gender: gender,
        },
        callback: function (r) {
            if (!r.exc) {
                if (r.message) {
                    // Show success message inline
                    container.innerHTML = `
                    <div class="text-center h-100 d-flex flex-column justify-content-center align-items-center p-4 bg-light rounded-4">
                        <i class="fas fa-check-circle text-success mb-3" style="font-size: 4rem;"></i>
                        <h3 class="h4 mb-3">Message Sent!</h3>
                        <p class="text-muted mb-4">Thank you, <strong>${firstname} ${lastname}</strong>. Your inquiry has been successfully received. Our team will get back to you shortly.</p>
                        <button onclick="location.reload()" class="btn btn-outline-secondary rounded-pill px-4">Send Another Message</button>
                    </div>
                `;;
                }
            }
        },
        error: function () {
            // Show error message inline
            container.innerHTML = errorMessage;
        }
    });
}