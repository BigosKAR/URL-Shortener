let shortenButton = document.getElementById("shortenButton")

shortenButton.addEventListener("click", () => {
    let userInput = document.getElementById("userInput")
    if(userInput.value !== ""){
        // defining elements we will change
        let displayErrorElement = document.getElementById("errorMessage");
        let displayShortUrlElement = document.getElementById("shortUrl");
        let displayIncorrectShortcodeElement = document.getElementById("incorrectShortcodeMsg")
        
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
                const responseJSON = JSON.parse(xhr.response)
                displayShortUrlElement.href = responseJSON.success; 
                displayShortUrlElement.innerHTML = responseJSON.success;

                // Delete any previous errors
                displayErrorElement.innerHTML = "";

                displayIncorrectShortcodeElement.hidden = true
            }
            else if(xhr.status === 400){
                const responseJSON = JSON.parse(xhr.response)
                displayErrorElement.innerHTML = responseJSON.error;

                // Delete any previous successes
                displayShortUrlElement.href = "";
                displayShortUrlElement.innerHTML = "";

                displayIncorrectShortcodeElement.hidden = true

            }       
        };
//         xhr.onerror = function() { // only triggers if the request couldn't be made at all
//             
        // };
    }
    else{
        alert("No input found.")
    }
})
