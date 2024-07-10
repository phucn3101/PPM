document.getElementById('generate-data-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let numPatients = document.getElementById('num_patients').value;
    let numRecords = document.getElementById('num_records').value;

    fetch('/generate-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            num_patients: numPatients,
            num_records: numRecords
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message;
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Error: ' + error;
    });
});
