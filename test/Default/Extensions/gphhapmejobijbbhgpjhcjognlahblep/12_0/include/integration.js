// SPDX-License-Identifer: GPL-3.0-or-later

import constants from "./constants.js";
import { m } from "./i18n.js";

const Integration = (function () {
    var ready = new Promise(function (resolve, reject) {
        chrome.runtime.getPlatformInfo(function (info) {
            if (constants.PLATFORMS_WHITELIST.indexOf(info.os) === -1) {
                reject();
            }
            else {
                resolve();
            }
        });
    }).catch(() => { });

    var onInitialize = new Promise((resolve, reject) => {
        sendNativeRequest({ execute: "initialize" }, (response) => {
            if (response && response.success) {
                resolve(response);
            }
            else {
                reject(response);
            }
        });
    });

    function sendNativeRequest(request, sendResponse) {
        ready.then(function () {
            if (sendResponse) {
                chrome.runtime.sendNativeMessage(
                    constants.NATIVE_HOST,
                    request,
                    function (response) {
                        if (response) {
                            sendResponse(response);
                        }
                        else {
                            var message = m('no_host_connector');
                            if (
                                chrome.runtime.lastError &&
                                chrome.runtime.lastError.message &&
                                chrome.runtime.lastError.message.indexOf("host not found") === -1 && // Chrome
                                chrome.runtime.lastError.message.indexOf("disconnected port") === -1 // Firefox
                            ) {
                                // Some error occured. Show to user
                                message = chrome.runtime.lastError.message;
                            }

                            sendResponse({
                                success: false,
                                message: message
                            });
                        }
                    }
                );
            }
            else {
                chrome.runtime.sendNativeMessage(constants.NATIVE_HOST, request);
            }
        }, function () {
            if (sendResponse) {
                sendResponse({
                    success: false,
                    message: m('platform_not_supported')
                });
            }
        });
    }

    function isSupported(feature, response) {
        return response.properties &&
            response.properties.supports && response.properties.supports.indexOf(feature) !== -1;
    }

    return {
        // https://wiki.gnome.org/Projects/GnomeShell/Extensions/UUIDGuidelines
        isUUID: function (uuid) {
            return uuid && uuid.match('^[-a-zA-Z0-9@._]+$');
        },

        sendNativeRequest: sendNativeRequest,

        isSignalsEqual: function (newSignal, oldSignal) {
            if (!oldSignal || !newSignal)
                return false;

            if (!newSignal.signal || !oldSignal.signal || newSignal.signal !== oldSignal.signal)
                return false;

            if (newSignal.parameters) {
                if (!oldSignal.parameters)
                    return false;

                if (newSignal.parameters.length !== oldSignal.parameters.length)
                    return false;

                for (var i = 0; i < newSignal.parameters.length; i++) {
                    if (newSignal.parameters[i] !== oldSignal.parameters[i]) {
                        return false;
                    }
                }
            }
            else if (oldSignal.parameters) {
                return false;
            }

            return true;
        },

        onInitialize: function () {
            return onInitialize;
        },

        nativeNotificationsSupported: function (response) {
            return isSupported('notifications', response);
        },
    };
})();

export default Integration;
