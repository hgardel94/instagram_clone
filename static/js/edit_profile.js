document.addEventListener('DOMContentLoaded', function () {
    
    const forms = document.querySelectorAll('form.profile-update-form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const input = form.querySelector('input');
            const fieldName = input.name; 
            const formData = new FormData(form);

            fetch('/accounts/update_profile/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    
                    if (data[fieldName] !== undefined) {
                        input.value = data[fieldName];
                        
                    }
                    
                } if (data.error) {
                    alert('Error to update field: ' + JSON.stringify(data.error));
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});