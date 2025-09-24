let shortenButton = document.getElementById("shortenButton")

shortenButton.addEventListener("click", () => {
    let userInput = document.getElementById("userInput")
    if(userInput.value !== ""){
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:8000/api/generate_shortcode");
        xhr.setRequestHeader("Content-type", "application/json")
        console.log(userInput.value)
        const body = JSON.stringify({
            url: userInput.value,
        });
        console.log(body)
        xhr.send(body);
        xhr.onload = () => {
            if(xhr.status === 200 || xhr.status === 201){
                let displayShortUrlElement = document.getElementById("shortUrl");
                const responseJSON = JSON.parse(xhr.response)
                displayShortUrlElement.href = responseJSON.success; 
                displayShortUrlElement.innerHTML = responseJSON.success;
            }       
        };
        xhr.onerror = function() { // only triggers if the request couldn't be made at all
            alert(`Network Error`);
        };
    }
    else{
        alert("No input found.")
    }
})
