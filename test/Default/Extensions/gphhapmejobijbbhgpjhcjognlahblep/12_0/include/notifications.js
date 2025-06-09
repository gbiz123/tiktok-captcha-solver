// SPDX-License-Identifer: GPL-3.0-or-later

import bus from './bus.js';
import { m } from './i18n.js';
import Integration from './integration.js';

const Notifications = (function () {
    var DEFAULT_NOTIFICATION_OPTIONS = {
        type: chrome.notifications.TemplateType.BASIC,
        iconUrl: 'icons/GnomeLogo-128.png',
        title: m('gs_chrome'),
        buttons: [
            { title: m('close') }
        ],
        priority: 2,
        isClickable: true,
        requireInteraction: true
    };

    function remove_notification() {
        Integration.onInitialize().then(response => {
            if (Integration.nativeNotificationsSupported(response)) {
                native.remove.apply(this, arguments);
            }
        });
    }

    function remove_list(options) {
        if (options.items) {
            var items = [];
            for (k in options.items) {
                if (options.items.hasOwnProperty(k)) {
                    items.push(options.items[k].title + ' ' + options.items[k].message);
                }
            }

            if (options.message && items) {
                options.message += "\n";
            }

            options.message += items.join("\n");

            options.type = chrome.notifications.TemplateType.BASIC;
            delete options.items;
        }

        return options;
    }

    var native = (function () {
        function create(name, options) {
            options = remove_list(options);

            bus.postMessage({
                execute: 'createNotification',
                name: name,
                options: { ...DEFAULT_NOTIFICATION_OPTIONS, ...options }
            });
        }

        function remove(notificationId) {
            chrome.runtime.sendMessage({
                execute: 'removeNotification',
                name: notificationId
            });
        }

        return {
            create: create,
            remove: remove
        };
    })();

    return {
        create: function () {
            Integration.onInitialize().then(response => {
                if (Integration.nativeNotificationsSupported(response)) {
                    native.create.apply(this, arguments);
                }
            });
        },
        remove: remove_notification,
    };
})();

export default Notifications;
