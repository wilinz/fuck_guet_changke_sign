# fuck_guet_changke_sign 桂电畅课系统签到url解析

源 js：
```js
 , fe = function(e) {
                    if (t.log("scanUrlAnalysis url:".concat(e)),
                    e.includes("/j?p=") && !e.startsWith("http") && (e = de() + e),
                    !e.startsWith("http"))
                        return e;
                    var n;
                    try {
                        n = new URL(e)
                    } catch (ae) {
                        return e
                    }
                    if ("/j" === n.pathname || "/scanner-jumper" === n.pathname) {
                        var o = new URLSearchParams(n.search)
                          , r = null;
                        try {
                            var a = o.get("_p");
                            a && (r = JSON.parse(a))
                        } catch (q) {}
                        return r || (r = (0,
                        G.V)(o.get("p") || "")),
                        r && Object.keys(r).length ? JSON.stringify(r) : e
                    }
                    return e
                }
```
```js
 var ta = String.fromCharCode(30)
          , ea = String.fromCharCode(31)
          , na = String.fromCharCode(26)
          , ra = String.fromCharCode(16)
          , ia = na + "1"
          , oa = na + "0"
          , aa = Object.fromEntries(["courseId", "activityId", "activityType", "data", "rollcallId", "groupSetId", "accessCode", "action", "enableGroupRollcall", "createUser", "joinCourse"].map((function(t, e) {
            return [t, e.toString(36)]
        }
        )))
          , ua = Object.fromEntries(["classroom-exam", "feedback", "vote"].map((function(t, e) {
            return [t, na + Number(e + 2).toString(36)]
        }
        )))
          , ca = Object.fromEntries(Object.entries(aa).map((function(t) {
            return [t[1], t[0]]
        }
        )))
          , sa = Object.fromEntries(Object.entries(ua).map((function(t) {
            return [t[1], t[0]]
        }
        )))
          , la = function(t) {
            var e = {};
            return t && "string" == typeof t ? (t.split("!").filter((function(t) {
                return !!t
            }
            )).forEach((function(t) {
                var n = t.split("~")
                  , r = n[0]
                  , i = n[1];
                r && void 0 !== i && (e[function(t) {
                    return ca[t] || t
                }(r)] = function(t) {
                    if (t.startsWith(na))
                        return t === ia || t !== oa && (sa[t] || t);
                    if (t.startsWith(ra)) {
                        var e = t.substring(1).split(".").map((function(t) {
                            return parseInt(t, 36)
                        }
                        ));
                        return e.length > 1 ? parseFloat(e[0] + "." + e[1]) : e[0]
                    }
                    return t.replaceAll(ea, "~").replaceAll(ta, "!")
                }(i))
            }
            )),
            e) : e
        }
    }
```

貌似这是整个请求体：
```js
if (t.rollcallId && e.latitude) {
                    var n = new u.YY(G());
                    n.setCourse(d["default"].state.course.currentCourse),
                    n.rollcallId = t.rollcallId,
                    n.location = {
                        lat: e.latitude,
                        lon: e.longitude
                    },
                    n.accuracy = e.accuracy,
                    n.altitude = e.altitude,
                    n.altitudeAccuracy = e.altitudeAccuracy,
                    n.heading = e.heading,
                    n.speed = e.speed,
                    n.actionType = t.actionType,
                    n.deviceId = t.deviceId,
                    n.studentStatus = t.studentStatus,
                    n.studentDistance = t.studentDistance,
                    s.cleanObjectNil(n),
                    z(n)
                }
```