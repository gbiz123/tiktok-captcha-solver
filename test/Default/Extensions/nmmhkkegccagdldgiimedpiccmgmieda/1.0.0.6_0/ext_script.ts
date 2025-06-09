const sendApiKey = document.getElementById("sendApiKey")!

interface Response {
	message: string,
	success: number
}

async function sendApiKeyToContentScript() {
	console.log("ummm")
	const apiKeyInput = <HTMLInputElement>document.getElementById("apiKeyInput")!
	const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
	if (apiKeyInput !== null) {
		const apiKey: string = apiKeyInput.value
		let tabId = tab.id
		// if (!tab.url?.includes("tiktok")) {
		// 	alert("Please go to the TikTok website before entering your key.")
		// }
		if (tabId !== undefined) {
			console.log("Sending api key: " + apiKey)
			const response: Response = await chrome.tabs.sendMessage(tabId, { apiKey: apiKey });
			if (response.success === 1) {
				alert("API key set successfully. Now, captchas will be solved automatically.")
			} else {
				alert("Something went wrong: " + response.message)
			}
		} else {
			console.log("tabId was undefined")
		}
	} else {
		console.log("apiKeyInput was null")
	}
}

sendApiKey.addEventListener("click", sendApiKeyToContentScript)
