
export function formatDate(date, type) {
    const d = new Date(date);

    switch (type) {
        case 'time':{
            return String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0') + ':' + String(d.getSeconds()).padStart(2, '0') + '.' + String(d.getMilliseconds()).padStart(3, '0');
        }
        case 'date': {
            return String(d.getFullYear()) + '-' + String((d.getMonth() + 1)).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0')
        }
    }
}