self.addEventListener('notificationclick', function (e) {
    var notification = e.notification;
    var primaryKey = notification.data.primaryKey;
    var action = e.action;

    if (action === 'close') {
        notification.close();
    } else {
        clients.openWindow('http://www.example.com');
        notification.close();
    }
});

self.addEventListener('notificationclose', function (event) {
    var notification = event.notification;
    var primaryKey = notification.data.primaryKey;

    console.log('Closed notification');
});

self.addEventListener('install', function (event) {
    // Perform install steps
    console.log('Service Worker install');
});

self.addEventListener('push', function (event) {
    // Perform install steps

    if (event.data) {

        let notification = event.data.json().notification

        self.registration.showNotification(notification.title,
            {
                body: notification.body,
                //icon: icon,
                //tag: tag,
                //data: data,
                userVisibleOnly: true
            });
    } else {
        console.log('Push event but no data')
    }

    console.log('Notification received');
});