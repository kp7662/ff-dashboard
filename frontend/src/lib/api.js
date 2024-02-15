export async function fetchData() {
    const response = await fetch('http://localhost:5000/api/data');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}