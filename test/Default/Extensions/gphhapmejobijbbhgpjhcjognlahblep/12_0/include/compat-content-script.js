// SPDX-License-Identifer: GPL-3.0-or-later

if (!window.chrome) {
    (function () {
        // Define the API subset provided to the webpage
        var externalMessaging = {
            runtime: {
                sendMessage: function (extensionId, message, options, responseCallback) {
                    if (extensionId !== chrome.runtime.id) {
                        console.error('Wrong extension id provided.')
                        return;
                    }

                    if (typeof (options) === 'function') {
                        responseCallback = options;
                        options = undefined;
                    }

                    chrome.runtime.sendMessage(extensionId, message, options)
                        .then(result => {
                            if (typeof (responseCallback) == 'function') {
                                responseCallback(cloneInto(result, window));
                            }
                        })
                        .catch(err => {
                            console.error("firefox-external-messaging: runtime.sendMessage error", err);
                        });
                }
            }
        };

        // Inject the API in the webpage wrapped by this content script
        // (exposed as `chrome.runtime.sendMessage({anyProp: "anyValue"}).then(reply => ..., err => ...)`)
        window.wrappedJSObject.chrome = cloneInto(externalMessaging, window, {
            cloneFunctions: true,
        });
    })();
}
