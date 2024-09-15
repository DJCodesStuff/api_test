document.getElementById('submitForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        id_number: document.getElementById('id_number').value,
        email: document.getElementById('email').value
    };

    fetch('/api/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerHTML = `Response: ${JSON.stringify(data)}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
