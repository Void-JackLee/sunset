import axios from "axios";

export function postJSON(url,data) {
    return new Promise((resolve, reject) => {
        axios.post(url,data).then(res => {
            resolve(res.data)
        }).catch(err => {
            reject(getMsg(err))
        })
    })
}

export function postForm(url,datat) {
    return new Promise((resolve, reject) => {
        axios({
            method: 'POST',
            url: url,
            data: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            transformRequest: [data => {
                let formData = new FormData()
                for(let key in data){
                    formData.append(key, data[key])
                }
                return formData
            }],
        }).then(res => {
            resolve(res.data)
        }).catch(err => {
            reject(getMsg(err))
        })
    })
}

export function postString(url,data) {
    return new Promise((resolve, reject) => {
        axios({
            method: 'POST',
            url: url,
            data: data,
            headers: {
                'Content-Type': 'application/text; charset=utf-8'
            }
        }).then(res => {
            resolve(res.data)
        }).catch(err => {
            reject(getMsg(err))
        })
    })
}

export function postFile(url,data) {
    return new Promise((resolve, reject) => {
        axios({
            method: 'post',
            url: url,
            data: data,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(res => {
            resolve(res.data)
        }).catch(err => {
            reject(getMsg(err))
        })
    })
}

export function getJSON(url) {
    return new Promise((resolve,reject) => {
        axios.get(url).then(res => {
            resolve(res.data)
        }).catch(err => {
            reject(getMsg(err))
        })
    })
}

export function getMsg(err) {
    let status = -1;
    let msg = status + " - " + err.message;

    if (err.response) {
        if (err.response.status) {
            status = err.response.status;
            msg = status + " - Unknown Error!";
            if (err.response.statusText) {
                msg = status + " - " + err.response.statusText;
            }
            if (err.response.data) {
                if (err.response.data.status) {
                    status = err.response.data.status;
                    if (err.response.data.msg) {
                        msg = status + " - " + err.response.data.msg;
                    } else if (err.response.data.message) {
                        msg = status + " - " + err.response.data.message;
                    }
                }
            }
        }
    }
    return {
        status,
        msg
    };
}

export default {
    install(app) {
        app.config.globalProperties.postJSON = postJSON;
        app.config.globalProperties.postForm= postForm;
        app.config.globalProperties.postString = postString;
        app.config.globalProperties.getJSON = getJSON;
    }
}

