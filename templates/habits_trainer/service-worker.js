self.addEventListener('notificationclick', function (e) {
    var notification = e.notification;
    //var primaryKey = notification.data.primaryKey;
    var action = e.action;

    var request = new Request(e.action);

    fetch(request).then(response => {
        if (!response.ok) {
            self.registration.showNotification("Fehler bei der Bearbeitung")
        }
    });

    //console.log(request.getAllResponseHeaders())


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
                requireInteraction: true,
                actions: JSON.parse(event.data.json().data.actions),
                //icon: icon,
                //tag: tag,
                //data: data,
                userVisibleOnly: true
            })
        ;
    } else {
        console.log('Push event but no data')
    }

    console.log('Notification received');
});