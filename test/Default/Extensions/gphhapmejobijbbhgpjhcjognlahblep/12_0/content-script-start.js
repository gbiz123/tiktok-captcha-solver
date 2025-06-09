// SPDX-License-Identifer: GPL-3.0-or-later

const data = document.createElement('gnome-browser-integration');
data.dataset['extensionId'] = constants.GS_CHROME_ID;
if (constants.EXTERNAL_MESSAGES) {
    for (let key of constants.EXTERNAL_MESSAGES) {
        data.dataset[key] = chrome.i18n.getMessage(key);
    }
}
document.documentElement.appendChild(data);

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (
            sender.id && sender.id === constants.GS_CHROME_ID &&
            request && request.signal &&
            [constants.SIGNAL_EXTENSION_CHANGED, constants.SIGNAL_SHELL_APPEARED, constants.SIGNAL_SHELL_SETTING_CHANGED].indexOf(request.signal) !== -1) {
            window.postMessage(
                {
                    type: "gs-chrome",
                    request: request
                }, "*"
            );
        }
    }
);

const s = document.createElement('script');

s.src = chrome.runtime.getURL('include/sweettooth-api.js');
s.onload = function () {
    this.parentNode.removeChild(this);
};
(document.head || document.documentElement).appendChild(s);
