let shortenButton = document.getElementById("shortenButton")
let copyButton = document.getElementById("copyButton")

shortenButton.addEventListener("click", () => {
    let userInput = document.getElementById("userInput")
    if(userInput.value !== ""){
        // defining elements we will change
        let displayErrorElement = document.getElementById("errorMessage");
        let errorContainer = document.getElementById("errorContainer")

        let displayShortUrlContainer = document.getElementById("shortUrlContainer");
        let displayShortUrlElement = document.getElementById("shortUrl");

        let displayIncorrectShortcodeElement = document.getElementById("incorrectShortcodeContainer")

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:8000/api/generate_shortcode");
        xhr.setRequestHeader("Content-type", "application/json")
        const body = JSON.stringify({
            url: userInput.value,
        });
        xhr.send(body);
        xhr.onload = () => {
            if(xhr.status === 200 || xhr.status === 201){
                const responseJSON = JSON.parse(xhr.response)
                
                displayShortUrlContainer.style.display = "flex";

                displayShortUrlElement.href = responseJSON.success; 
                displayShortUrlElement.innerHTML = responseJSON.success;

                // Delete any previous errors
                if (displayIncorrectShortcodeElement !== null)displayIncorrectShortcodeElement.style.display = 'none'; // Shortcode might or might not exit!
                errorContainer.style.display = "none";
                if(displayIncorrectShortcodeElement !== null)displayIncorrectShortcodeElement.style.display = 'none';
            }
            else if(xhr.status === 400){
                const responseJSON = JSON.parse(xhr.response)
                displayErrorElement.innerHTML = responseJSON.error;

                errorContainer.style.display = "flex";
                // Delete any previous successes or errors

                if(displayIncorrectShortcodeElement !== null)displayIncorrectShortcodeElement.style.display = 'none';
                displayShortUrlContainer.style.display = "none";
                if (displayIncorrectShortcodeElement !== null)displayIncorrectShortcodeElement.style.display = 'none';
            }       
        };
//         xhr.onerror = function() { // only triggers if the request couldn't be made at all
//             
        // };
    }
})

copyButton.addEventListener("click", () => {
    let shortUrlElement = document.getElementById("shortUrl");
    navigator.clipboard.writeText(shortUrlElement.innerHTML);

    alert("Copied to the clipboard")
})