const TIMEAGO_UTIL = require("vue-timeago");

const DATE_OPTIONS = {
	year: 'numeric',
	month: 'short',
	day: 'numeric',
	hour: '2-digit',
	minute: '2-digit',
	hour12: true
};

const SHORT_DATE_OPTIONS = {
	year: 'numeric',
	month: 'short',
	day: 'numeric',
};

function getReadableDate(time) {
	return new Date(time).toLocaleDateString("en-US", DATE_OPTIONS)
}

function getShortReadableDate(time) {
	return new Date(time).toLocaleDateString("en-US", SHORT_DATE_OPTIONS)
}

function getTimeago(time, $timeago) {
	return TIMEAGO_UTIL.converter(new Date(time), $timeago.locale, { includeSeconds: true, addSuffix: true })
}

function formatIntoAbbreviatedString(ms) {
    let secs = parseInt(ms / 1000);
    if (secs === 0) {
        return "0s";
    }

    let remainder = parseInt(secs % 86400);
    let days = parseInt(secs / 86400);
    let hours = parseInt(remainder / 3600);
    let minutes = parseInt(remainder / 60 - hours * 60);
    let seconds = parseInt(remainder % 3600 - minutes * 60);

    let fDays;
    if (days > 0) {
        fDays = " " + days + "d";
    } else {
        fDays = "";
    }

    let fHours;
    if (hours > 0) {
        fHours = " " + hours + "h";
    } else {
        fHours = "";
    }

    let fMinutes;
    if (minutes > 0) {
        fMinutes = " " + minutes + "m";
    } else {
        fMinutes = "";
    }

    let fSeconds;
    if (seconds > 0) {
        fSeconds = " " + seconds + "s";
    } else {
        fSeconds = "";
    }

    return (fDays + fHours + fMinutes + fSeconds).trim()
}

export { getReadableDate, getShortReadableDate, getTimeago, formatIntoAbbreviatedString };
