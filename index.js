const fetchData = async () => {
    const options = {
        headers: {
            'Authorization': 'Client-ID tKq2uU7VT5a5p6aYX0FPn-uTMjglwoOmV2TsKtYlAus'
        }, method: 'GET'
    }

    const response = await fetch('https://api.unsplash.com/photos', options);

    const data = await response.json();

    data.forEach(element => {
        console.log(element);
    });
}

console.log(fetchData());