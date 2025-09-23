let shortenButton = document.getElementById("shortenButton")

shortenButton.addEventListener("click", () => {
    let userInput = document.getElementById("userInput")
    if(userInput.value === ""){
        alert("Can not shorten an empty input!")
    }
    else{
        alert(`Sent over the input: ${userInput.value}`)
    }
})
