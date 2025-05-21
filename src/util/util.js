
export function getAttr(attr) {
    let s = window.location.search;
    let ok = false;
    let size = s.length;
    let l = 0;
    let str = '';
    for (let i = 0;i < size;i ++)
    {
        if (s[i] === '&') {
            if (!ok) {
                ok = true;
                str += s[i];
            }
        } else {
            ok = false;
            str += s[i];
        }
    }
    s = str;
    size = s.length;
    if (s[size - 1] === '&') size --;
    ok = false;
    str = '';
    for (let i = 0;i < size + 1;i ++)
    {
        if (s[i] === '?') continue;
        if (s[i] === '=' && !ok) {
            if (l !== 0) str += '":"';
            ok = true;
        } else if (s[i] === '&' || i === size) {
            if (l !== 0) {
                if (!ok) str += '":"';
                str += '","';
            }
            ok = false;
            l = 0;
        } else {
            if (l !== 0 || !ok) str += s[i];
            if (!ok) l ++;
        }
    }
    size = str.length;
    if (str[size - 1] === '"') str = str.substr(0,size - 3);
    let attrs = null;
    if (str !== '')
    {
        str = '{"' + str + '"}';
        attrs = JSON.parse(str);
    }
    if (attr != null) {
        if (attrs !== null) return unescape(attrs[attr]);
        return null;
    }
    return attrs;
}

function getResp(res,err) {
    const resp = res.response || res;
    if (resp.status !== 200 || resp.data.status !== 200) {
        err()
        return null;
    }
    return resp;
}

function isNumber(x,point,neg) {
    let str = String(x)
    let vis = false
    if (str.length === 0) return false;
    let visNeg = false;
    if (str[0] !== '-') visNeg = true

    for (let i in str) {
        if (str[i] >= '0' && str[i] <= '9') {
            continue;
        } else if (str[i] === '.') {
            if (!point || vis) return false;
            vis = true
        } else if (str[i] === '-') {
            if (!neg || visNeg) return false;
            visNeg = true
        } else return false;
    }
    return true;
}

function fullscreen() {
    if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen()
    } else {
        var element = document.getElementById('fullscreen-element');
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        } else if (element.webkitRequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen();
        } else {
            element.style.width = '100%';
            element.style.height = '100%';
            element.style.position = 'fixed';
            element.style.top = '0';
            element.style.left = '0';
        }
    }
}

export default {
    install(app) {
        app.config.globalProperties.getAttr = getAttr;
        app.config.globalProperties.getResp = getResp;
        app.config.globalProperties.isNumber = isNumber;
        app.config.globalProperties.fullscreen = fullscreen;
    }
}
