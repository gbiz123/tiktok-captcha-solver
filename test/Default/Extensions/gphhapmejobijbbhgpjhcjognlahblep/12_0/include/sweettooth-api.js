// SPDX-License-Identifer: GPL-3.0-or-later

"use strict";

var GSC = (function () {
    const dataset = document.getElementsByTagName("gnome-browser-integration")[0].dataset;

    function getData(key) {
        return dataset[key];
    }

    return {
        GS_CHROME_ID: getData('extensionId'),
        getMessage: function (key) {
            let message = getData(key);
            if (message) {
                for (let i = 1; i < arguments.length; i++) {
                    message = message.replace('$' + i, arguments[i]);
                }

                return message;
            }

            return key;
        },
    }
}());

window.SweetTooth = function () {
    var apiObject = {
        apiVersion: 5,
        shellVersion: '-1',
        versionValidationEnabled: true,
        userExtensionsDisabled: false,

        getChromeExtensionId: function () {
            return GSC.GS_CHROME_ID;
        },

        getExtensionErrors: function (uuid) {
            return sendResolveExtensionMessage("getExtensionErrors", "extensionErrors", { uuid: uuid });
        },

        getExtensionInfo: function (uuid) {
            return sendResolveExtensionMessage("getExtensionInfo", "extensionInfo", { uuid: uuid });
        },

        installExtension: function (uuid) {
            return sendResolveExtensionMessage("installExtension", "status", { uuid: uuid });
        },

        launchExtensionPrefs: function (uuid) {
            sendExtensionMessage("launchExtensionPrefs", null, { uuid: uuid });
        },

        listExtensions: function () {
            return sendResolveExtensionMessage("listExtensions", "extensions");
        },

        setExtensionEnabled: function (uuid, enable) {
            return sendResolveExtensionMessage("enableExtension", "success", { uuid: uuid, enable: enable });
        },

        uninstallExtension: function (uuid) {
            return sendResolveExtensionMessage("uninstallExtension", "status", { uuid: uuid });
        },

        setUserExtensionsDisabled: function (disable) {
            return sendResolveExtensionMessage("setUserExtensionsDisabled", "success", { disable: disable })
                .then(success => {
                    if (success) {
                        apiObject.userExtensionsDisabled = disable;
                    }

                    return success;
                });
        },

        setVersionValidationDisabled: function (disable) {
            return sendResolveExtensionMessage("setVersionValidationDisabled", "success", { disable: disable })
                .then(success => {
                    if (success) {
                        apiObject.versionValidationEnabled = !disable;
                    }

                    return success;
                });
        },

        initialize: function () {
            if (SweetTooth.shellVersion !== '-1') {
                return Promise.resolve(apiObject);
            }

            var ready = new Promise(function (resolve, reject) {
                sendExtensionMessage("initialize", response => {
                    if (response?.success && response?.properties?.shellVersion) {
                        resolve(response.properties);
                    }
                    else {
                        var message = response && response.message ? GSC.getMessage(response.message) : GSC.getMessage('error_connector_response');
                        reject(message);
                    }
                });
            });

            ready.then(function (response) {
                apiObject.shellVersion = response.shellVersion;
                apiObject.versionValidationEnabled = response.versionValidationEnabled;
                apiObject.userExtensionsDisabled = response.userExtensionsDisabled;

                let REQUIRED_APIS = [
                    "notifications",
                    "v6"
                ];

                if (response.supports) {
                    for (let api of response.supports) {
                        let api_index;
                        if ((api_index = REQUIRED_APIS.indexOf(api)) != -1) {
                            REQUIRED_APIS.splice(api_index, 1);
                        }

                        if (api === 'v6') {
                            apiObject.apiVersion = 6;
                        }
                    }
                }

                if (REQUIRED_APIS.length > 0) {
                    require(['messages'], function (messages) {
                        messages.addWarning(GSC.getMessage('warning_apis_missing', REQUIRED_APIS.join(", ")));
                    });
                }
            }, function (message) {
                apiObject.apiVersion = null;

                require(['messages'], function (messages) {
                    messages.addError(message ? message : GSC.getMessage('no_host_connector'));
                })
            });

            return ready;
        }
    };

    window.addEventListener("message", function (event) {
        // We only accept messages from ourselves
        if (event.source !== window) {
            return;
        }

        if (event.data.type) {
            if (event.data.type == "gs-chrome") {
                if (event.data.request.signal == 'ExtensionStatusChanged' && apiObject.onchange) {
                    apiObject.onchange(
                        event.data.request.parameters[0],
                        event.data.request.parameters[1],
                        event.data.request.parameters[2]
                    );
                }
                else if (event.data.request.signal == 'org.gnome.Shell' && apiObject.onshellrestart) {
                    apiObject.onshellrestart();
                }
                else if (event.data.request.signal == 'ShellSettingsChanged' && apiObject.onShellSettingChanged) {
                    if (event.data.request.key === 'disable-user-extensions') {
                        apiObject.userExtensionsDisabled = event.data.request.value;
                    }
                    else if (event.data.request.key === 'disable-extension-version-validation') {
                        apiObject.versionValidationEnabled = !event.data.request.value;
                    }

                    apiObject.onShellSettingChanged(event.data.request.key, event.data.request.value);
                }
            }
        }
    }, false);

    function sendResolveExtensionMessage(method, resolveProperty, parameters) {
        return new Promise(function (resolve, reject) {
            sendExtensionMessage(method, function (response) {
                if (response && response.success) {
                    resolve(response[resolveProperty]);
                }
                else {
                    var message = response && response.message ? response.message : GSC.getMessage('error_connector_response');
                    reject(message);
                }
            },
                parameters
            );
        });
    }

    function sendExtensionMessage(method, callback, parameters) {
        var request = { execute: method };
        if (parameters) {
            request = Object.assign(parameters, request);
        }

        chrome.runtime.sendMessage(
            apiObject.getChromeExtensionId(),
            request,
            callback
        );
    }

    return apiObject;
}();
