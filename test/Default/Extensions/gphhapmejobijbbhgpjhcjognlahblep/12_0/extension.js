// SPDX-License-Identifer: GPL-3.0-or-later

import bus from "./include/bus.js";
import constants from "./include/constants.js";
import Integration from "./include/integration.js";
import Synchronize from "./include/sync.js";
import Toolbar from "./include/toolbar.js";

chrome.runtime.onInstalled.addListener(function (details) {
    var version = chrome.runtime.getManifest().version;

    if (details.reason == chrome.runtime.OnInstalledReason.UPDATE && details.previousVersion != version) {
        chrome.storage.sync.get(constants.DEFAULT_SYNC_OPTIONS, function (options) {
            if (options.showReleaseNotes) {
                chrome.tabs.create({
                    url: `https://gnome.pages.gitlab.gnome.org/gnome-browser-integration/extension-${version}.html`,
                    active: true
                });
            }
        });
    }
});

const IS_FIREFOX = typeof (CSS) !== 'undefined' && CSS.supports("-moz-appearance: none");

if (IS_FIREFOX) {
    chrome.runtime.onMessageExternal = {
        addListener: chrome.runtime.onMessage.addListener
    };
}

chrome.runtime.onMessageExternal.addListener(function (request, sender, sendResponse) {
    if (
        constants.EXTENSIONS_WEBSITES.reduce(
            (accumulator, url) => accumulator + sender.url.startsWith(url),
            0)
    ) {
        if (request && request.execute) {
            if (request.uuid && !Integration.isUUID(request.uuid)) {
                return;
            }

            switch (request.execute) {
                case 'initialize':
                case 'listExtensions':
                    Integration.sendNativeRequest({ execute: request.execute }, sendResponse);
                    return true;

                case 'launchExtensionPrefs':
                    Integration.sendNativeRequest({ execute: request.execute, uuid: request.uuid });
                    break;

                case 'getExtensionErrors':
                case 'getExtensionInfo':
                case 'installExtension':
                case 'uninstallExtension':
                    Integration.sendNativeRequest({ execute: request.execute, uuid: request.uuid }, sendResponse);
                    return true;

                case 'enableExtension':
                    Integration.sendNativeRequest({
                        execute: request.execute,
                        uuid: request.uuid,
                        enable: request.enable
                    },
                        sendResponse
                    );
                    return true;

                case 'setUserExtensionsDisabled':
                case 'setVersionValidationDisabled':
                    Integration.sendNativeRequest({ execute: request.execute, disable: request.disable ? true : false }, sendResponse);
                    return true;
            }
        }
    }
});

chrome.action.onClicked.addListener(function () {
    chrome.tabs.create({
        url: constants.EXTENSIONS_MAIN_WEBSITE,
        active: true
    });
});

var disabledExtensionTimeout = null;
var lastPortMessage = { message: null, date: 0 };
var port = chrome.runtime.connectNative(constants.NATIVE_HOST);
port.onDisconnect.addListener(function () {
    console.log('Disconnected');
    port = null;
});


/*
 * Native host messaging events handler.
 */
port.onMessage.addListener(function (message) {
    if (message && message.signal) {
        if ([constants.SIGNAL_EXTENSION_CHANGED, constants.SIGNAL_SHELL_APPEARED, constants.SIGNAL_SHELL_SETTING_CHANGED].indexOf(message.signal) !== -1) {
            /*
             * Skip duplicate events. This is happens eg when extension is installed.
             */
            if (
                message.signal != constants.SIGNAL_SHELL_SETTING_CHANGED &&
                (new Date().getTime()) - lastPortMessage.date < 1000 && Integration.isSignalsEqual(message, lastPortMessage.message)
            ) {
                lastPortMessage.date = new Date().getTime();
                return;
            }

            // Send events to opened extensions.gnome.org tabs and don't complain in case there is no listener on other side.
            constants.EXTENSIONS_WEBSITES.forEach(url => {
                chrome.tabs.query({
                    url: url + '*'
                },
                    function (tabs) {
                        for (let k in tabs) {
                            chrome.tabs.sendMessage(tabs[k].id, message).catch(() => { });
                        }
                    });
            });

            // Route message to content script and options page and don't complain in case there are no listeners on other sides.
            chrome.runtime.sendMessage(constants.GS_CHROME_ID, message).catch(() => { });
            if (message.signal === constants.SIGNAL_EXTENSION_CHANGED) {
                /*
                 * GNOME Shell sends 2 events when extension is uninstalled:
                 * "disabled" event and then "uninstalled" event.
                 * Let's delay any "disabled" event and drop it if
                 * "uninstalled" event received within 1,5 secs.
                 */
                if (message.parameters[constants.EXTENSION_CHANGED_STATE] === constants.EXTENSION_STATE.DISABLED) {
                    disabledExtensionTimeout = setTimeout(function () {
                        disabledExtensionTimeout = null;
                        Synchronize.onExtensionChanged(message);
                    }, 1500);
                }
                else if (
                    disabledExtensionTimeout &&
                    message.parameters[constants.EXTENSION_CHANGED_STATE] === constants.EXTENSION_STATE.UNINSTALLED &&
                    lastPortMessage.message.signal === constants.SIGNAL_EXTENSION_CHANGED &&
                    lastPortMessage.message.parameters[constants.EXTENSION_CHANGED_UUID] === message.parameters[constants.EXTENSION_CHANGED_UUID] &&
                    lastPortMessage.message.parameters[constants.EXTENSION_CHANGED_STATE] === constants.EXTENSION_STATE.DISABLED
                ) {
                    clearTimeout(disabledExtensionTimeout);
                    disabledExtensionTimeout = null;
                    Synchronize.onExtensionChanged(message);
                }
                else {
                    Synchronize.onExtensionChanged(message);
                }
            }

            lastPortMessage = {
                message: message,
                date: new Date().getTime()
            };
        }
        else if ([constants.SIGNAL_NOTIFICATION_ACTION, constants.SIGNAL_NOTIFICATION_CLICKED].indexOf(message.signal) != -1) {
            bus.postMessage(message);
        }
    }
});
/*
 * Subscribe to GNOME Shell signals
 */
port.postMessage({ execute: 'subscribeSignals' });

bus.addEventListener("message", function (event) {
    // We only accept messages from ourselves
    if (event?.data?.execute) {
        switch (event.data.execute) {
            case 'createNotification':
                port.postMessage(event.data);
                break;
            case 'removeNotification':
                port.postMessage(event.data);
                break;
        }
    }
}
);

chrome.runtime.getPlatformInfo(function (info) {
    if (constants.PLATFORMS_WHITELIST.indexOf(info.os) !== -1) {
        Synchronize.init();
    }
});

Toolbar.init();
