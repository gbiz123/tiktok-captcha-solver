var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var creditsUrl = "https://www.sadcaptcha.com/api/v1/license/credits?licenseKey=";
var rotateUrl = "https://www.sadcaptcha.com/api/v1/rotate?licenseKey=";
var puzzleUrl = "https://www.sadcaptcha.com/api/v1/puzzle?licenseKey=";
var shapesUrl = "https://www.sadcaptcha.com/api/v1/shapes?licenseKey=";
var iconUrl = "https://www.sadcaptcha.com/api/v1/icon?licenseKey=";
var successXpath = "//*[contains(text(), 'Verification complete')]";
var apiHeaders = new Headers({ "Content-Type": "application/json" });
var CONTAINER = document.documentElement || document.body;
var Wrappers = {
    V1: ".captcha-disable-scroll",
    V2: ".captcha-verify-container"
};
var RotateV1 = {
    INNER: "[data-testid=whirl-inner-img]",
    OUTER: "[data-testid=whirl-outer-img]",
    SLIDE_BAR: ".captcha_verify_slide--slidebar",
    SLIDER_DRAG_BUTTON: ".secsdk-captcha-drag-icon",
    UNIQUE_IDENTIFIER: ".captcha-disable-scroll [data-testid=whirl-inner-img]"
};
var RotateV2 = {
    INNER: ".captcha-verify-container > div > div > div > img.cap-absolute",
    OUTER: ".captcha-verify-container > div > div > div > img:first-child",
    SLIDE_BAR: ".captcha-verify-container > div > div > div.cap-w-full > div.cap-rounded-full",
    SLIDER_DRAG_BUTTON: "div[draggable=true]:has(.secsdk-captcha-drag-icon)",
    UNIQUE_IDENTIFIER: ".captcha-verify-container > div > div > div > img.cap-absolute"
};
var PuzzleV1 = {
    PIECE: "img.captcha_verify_img_slide",
    PUZZLE: "#captcha-verify-image",
    SLIDER_DRAG_BUTTON: ".secsdk-captcha-drag-icon",
    UNIQUE_IDENTIFIER: ".captcha-disable-scroll img.captcha_verify_img_slide"
};
var PuzzleV2 = {
    PIECE: ".captcha-verify-container .cap-absolute img",
    PUZZLE: "#captcha-verify-image",
    SLIDER_DRAG_BUTTON: "div[draggable=true]:has(.secsdk-captcha-drag-icon)",
    PIECE_IMAGE_CONTAINER: ".captcha-verify-container div[draggable=true]:has(img[draggable=false])",
    UNIQUE_IDENTIFIER: ".captcha-verify-container #captcha-verify-image"
};
var ShapesV1 = {
    IMAGE: "#captcha-verify-image",
    SUBMIT_BUTTON: ".verify-captcha-submit-button",
    UNIQUE_IDENTIFIER: ".captcha-disable-scroll .verify-captcha-submit-button"
};
var ShapesV2 = {
    IMAGE: ".captcha-verify-container div.cap-relative img",
    SUBMIT_BUTTON: ".captcha-verify-container .cap-relative button.cap-w-full",
    UNIQUE_IDENTIFIER: ".captcha-verify-container .cap-relative button.cap-w-full"
};
var IconV1 = {
    IMAGE: "#captcha-verify-image",
    SUBMIT_BUTTON: ".verify-captcha-submit-button",
    TEXT: ".captcha_verify_bar",
    UNIQUE_IDENTIFIER: ".captcha-disable-scroll .verify-captcha-submit-button"
};
var IconV2 = {
    IMAGE: ".captcha-verify-container div.cap-relative img",
    SUBMIT_BUTTON: ".captcha-verify-container .cap-relative button.cap-w-full",
    TEXT: ".captcha-verify-container > div > div > span"
};
var CaptchaType;
(function (CaptchaType) {
    CaptchaType[CaptchaType["PUZZLE_V1"] = 0] = "PUZZLE_V1";
    CaptchaType[CaptchaType["ROTATE_V1"] = 1] = "ROTATE_V1";
    CaptchaType[CaptchaType["SHAPES_V1"] = 2] = "SHAPES_V1";
    CaptchaType[CaptchaType["ICON_V1"] = 3] = "ICON_V1";
    CaptchaType[CaptchaType["PUZZLE_V2"] = 4] = "PUZZLE_V2";
    CaptchaType[CaptchaType["ROTATE_V2"] = 5] = "ROTATE_V2";
    CaptchaType[CaptchaType["SHAPES_V2"] = 6] = "SHAPES_V2";
    CaptchaType[CaptchaType["ICON_V2"] = 7] = "ICON_V2";
})(CaptchaType || (CaptchaType = {}));
function waitForAnyElementInList(selectors) {
    return new Promise(function (resolve) {
        var selectorFound = null;
        // Check if already present
        selectors.forEach(function (selector) {
            if (document.querySelector(selector)) {
                selectorFound = selector;
                console.log("Selector found: " + selector);
                return resolve(document.querySelector(selectorFound));
            }
        });
        if (selectorFound !== null) {
            return resolve(document.querySelector(selectorFound));
        }
        // Then start waiting if not found immediately
        var observer = new MutationObserver(function (mutations) {
            selectors.forEach(function (selector) {
                if (document.querySelector(selector)) {
                    selectorFound = selector;
                    console.log("Selector found by mutation observer: " + selector);
                    observer.disconnect();
                    return;
                }
            });
            if (selectorFound !== null) {
                console.log("returning selector from mutation observer: " + selectorFound);
                return resolve(document.querySelector(selectorFound));
            }
            else {
                console.log("unimportant mutation seen");
            }
        });
        observer.observe(CONTAINER, {
            childList: true,
            subtree: true
        });
    });
}
function waitForElement(selector) {
    return new Promise(function (resolve) {
        if (document.querySelector(selector)) {
            console.log("Selector found: " + selector);
            return resolve(document.querySelector(selector));
        }
        else {
            var observer_1 = new MutationObserver(function (mutations) {
                if (document.querySelector(selector)) {
                    observer_1.disconnect();
                    console.log("Selector found by mutation observer: " + selector);
                    return resolve(document.querySelector(selector));
                }
            });
            observer_1.observe(CONTAINER, {
                childList: true,
                subtree: true
            });
        }
    });
}
function creditsApiCall() {
    return __awaiter(this, void 0, void 0, function () {
        var resp, credits;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(creditsUrl + apiKey, {
                        method: "GET",
                        headers: apiHeaders,
                    })];
                case 1:
                    resp = _a.sent();
                    return [4 /*yield*/, resp.json()];
                case 2:
                    credits = (_a.sent()).credits;
                    console.log("api credits = " + credits);
                    return [2 /*return*/, credits];
            }
        });
    });
}
function rotateApiCall(outerB64, innerB64) {
    return __awaiter(this, void 0, void 0, function () {
        var resp, angle;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(rotateUrl + apiKey, {
                        method: "POST",
                        headers: apiHeaders,
                        body: JSON.stringify({
                            outerImageB64: outerB64,
                            innerImageB64: innerB64
                        })
                    })];
                case 1:
                    resp = _a.sent();
                    return [4 /*yield*/, resp.json()];
                case 2:
                    angle = (_a.sent()).angle;
                    console.log("angle = " + angle);
                    return [2 /*return*/, angle];
            }
        });
    });
}
function puzzleApiCall(puzzleB64, pieceB64) {
    return __awaiter(this, void 0, void 0, function () {
        var resp, slideXProportion;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(puzzleUrl + apiKey, {
                        method: "POST",
                        headers: apiHeaders,
                        body: JSON.stringify({
                            puzzleImageB64: puzzleB64,
                            pieceImageB64: pieceB64
                        })
                    })];
                case 1:
                    resp = _a.sent();
                    return [4 /*yield*/, resp.json()];
                case 2:
                    slideXProportion = (_a.sent()).slideXProportion;
                    console.log("slideXProportion = " + slideXProportion);
                    return [2 /*return*/, slideXProportion];
            }
        });
    });
}
function shapesApiCall(imageB64) {
    return __awaiter(this, void 0, void 0, function () {
        var resp, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(shapesUrl + apiKey, {
                        method: "POST",
                        headers: apiHeaders,
                        body: JSON.stringify({
                            imageB64: imageB64
                        })
                    })];
                case 1:
                    resp = _a.sent();
                    return [4 /*yield*/, resp.json()];
                case 2:
                    data = _a.sent();
                    console.log("Shapes response data:");
                    console.log(data);
                    return [2 /*return*/, {
                            pointOneProportionX: data.pointOneProportionX,
                            pointOneProportionY: data.pointOneProportionY,
                            pointTwoProportionX: data.pointTwoProportionX,
                            pointTwoProportionY: data.pointTwoProportionY
                        }];
            }
        });
    });
}
function iconApiCall(challenge, imageB64) {
    return __awaiter(this, void 0, void 0, function () {
        var resp, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(iconUrl + apiKey, {
                        method: "POST",
                        headers: apiHeaders,
                        body: JSON.stringify({
                            challenge: challenge,
                            imageB64: imageB64
                        })
                    })];
                case 1:
                    resp = _a.sent();
                    return [4 /*yield*/, resp.json()];
                case 2:
                    data = _a.sent();
                    console.log("Icon response data:");
                    console.log(data);
                    return [2 /*return*/, data];
            }
        });
    });
}
function anySelectorInListPresent(selectors) {
    for (var _i = 0, selectors_1 = selectors; _i < selectors_1.length; _i++) {
        var selector = selectors_1[_i];
        var ele = document.querySelector(selector);
        if (ele !== null) {
            return true;
        }
    }
    return false;
}
function identifyCaptcha() {
    return __awaiter(this, void 0, void 0, function () {
        var i, imgUrl, imgUrl;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 30)) return [3 /*break*/, 12];
                    if (!anySelectorInListPresent([RotateV1.UNIQUE_IDENTIFIER])) return [3 /*break*/, 2];
                    console.log("rotate v1 detected");
                    return [2 /*return*/, CaptchaType.ROTATE_V1];
                case 2:
                    if (!anySelectorInListPresent([PuzzleV1.UNIQUE_IDENTIFIER])) return [3 /*break*/, 3];
                    console.log("puzzle v1 detected");
                    return [2 /*return*/, CaptchaType.PUZZLE_V1];
                case 3:
                    if (!anySelectorInListPresent([ShapesV1.UNIQUE_IDENTIFIER])) return [3 /*break*/, 5];
                    return [4 /*yield*/, getImageSource(ShapesV2.IMAGE)];
                case 4:
                    imgUrl = _a.sent();
                    if (imgUrl.includes("/icon")) {
                        console.log("icon v1 detected");
                        return [2 /*return*/, CaptchaType.ICON_V1];
                    }
                    else {
                        console.log("shapes v1 detected");
                        return [2 /*return*/, CaptchaType.SHAPES_V1];
                    }
                    return [3 /*break*/, 11];
                case 5:
                    if (!anySelectorInListPresent([RotateV2.UNIQUE_IDENTIFIER])) return [3 /*break*/, 6];
                    console.log("rotate v2 detected");
                    return [2 /*return*/, CaptchaType.ROTATE_V2];
                case 6:
                    if (!anySelectorInListPresent([PuzzleV2.UNIQUE_IDENTIFIER])) return [3 /*break*/, 7];
                    console.log("puzzle v2 detected");
                    return [2 /*return*/, CaptchaType.PUZZLE_V2];
                case 7:
                    if (!anySelectorInListPresent([ShapesV2.UNIQUE_IDENTIFIER])) return [3 /*break*/, 9];
                    return [4 /*yield*/, getImageSource(ShapesV2.IMAGE)];
                case 8:
                    imgUrl = _a.sent();
                    if (imgUrl.includes("/icon")) {
                        console.log("icon v1 detected");
                        return [2 /*return*/, CaptchaType.ICON_V2];
                    }
                    else {
                        console.log("shapes v2 detected");
                        return [2 /*return*/, CaptchaType.SHAPES_V2];
                    }
                    return [3 /*break*/, 11];
                case 9: return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1000); })];
                case 10:
                    _a.sent();
                    _a.label = 11;
                case 11:
                    i++;
                    return [3 /*break*/, 1];
                case 12: throw new Error("Could not identify CaptchaType");
            }
        });
    });
}
function getImageSource(selector) {
    return __awaiter(this, void 0, void 0, function () {
        var ele, src;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, waitForElement(selector)];
                case 1:
                    ele = _a.sent();
                    src = ele.getAttribute("src");
                    console.log("src = " + selector);
                    return [2 /*return*/, src];
            }
        });
    });
}
function getBase64StringFromDataURL(dataUrl) {
    return dataUrl.replace('data:', '').replace(/^.+,/, '');
}
function fetchImageBase64(imageSource) {
    return __awaiter(this, void 0, void 0, function () {
        var res, img, reader;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(imageSource)];
                case 1:
                    res = _a.sent();
                    return [4 /*yield*/, res.blob()];
                case 2:
                    img = _a.sent();
                    reader = new FileReader();
                    reader.readAsDataURL(img);
                    return [2 /*return*/, new Promise(function (resolve) {
                            reader.onloadend = function () {
                                resolve(getBase64StringFromDataURL(reader.result));
                            };
                        })];
            }
        });
    });
}
function moveMouseTo(x, y) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            CONTAINER.dispatchEvent(new MouseEvent("mousemove", {
                bubbles: true,
                view: window,
                clientX: x,
                clientY: y
            }));
            console.log("moved mouse to " + x + ", " + y);
            return [2 /*return*/];
        });
    });
}
function solvePuzzleV2() {
    return __awaiter(this, void 0, void 0, function () {
        var _loop_1, i, state_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _loop_1 = function (i) {
                        function pieceHasReachedTargetLocation() {
                            var piece = document.querySelector(PuzzleV2.PIECE_IMAGE_CONTAINER);
                            var style = piece.getAttribute("style");
                            console.log("piece style: " + style);
                            var translateX = parseInt(style.match("(?<=translateX\\()[0-9]+").toString());
                            console.debug("translateX: " + translateX);
                            if (translateX >= distance) {
                                console.debug("piece has reached target location");
                                return true;
                            }
                            else {
                                console.debug("piece has not reached target location");
                                return false;
                            }
                        }
                        var puzzleSrc, pieceSrc, puzzleImg, pieceImg, solution, puzzleImageEle, distance, adjustment;
                        return __generator(this, function (_b) {
                            switch (_b.label) {
                                case 0: return [4 /*yield*/, getImageSource(PuzzleV2.PUZZLE)];
                                case 1:
                                    puzzleSrc = _b.sent();
                                    return [4 /*yield*/, getImageSource(PuzzleV2.PIECE)];
                                case 2:
                                    pieceSrc = _b.sent();
                                    return [4 /*yield*/, fetchImageBase64(puzzleSrc)];
                                case 3:
                                    puzzleImg = _b.sent();
                                    return [4 /*yield*/, fetchImageBase64(pieceSrc)];
                                case 4:
                                    pieceImg = _b.sent();
                                    return [4 /*yield*/, puzzleApiCall(puzzleImg, pieceImg)];
                                case 5:
                                    solution = _b.sent();
                                    puzzleImageEle = document.querySelector(PuzzleV2.PUZZLE);
                                    return [4 /*yield*/, computePuzzleSlideDistance(solution, puzzleImageEle)];
                                case 6:
                                    distance = _b.sent();
                                    adjustment = 3;
                                    distance = distance - adjustment;
                                    return [4 /*yield*/, dragWithPreciseMonitoring(PuzzleV2.SLIDER_DRAG_BUTTON, distance, pieceHasReachedTargetLocation)];
                                case 7:
                                    _b.sent();
                                    return [4 /*yield*/, checkCaptchaSuccess()];
                                case 8:
                                    if (_b.sent())
                                        return [2 /*return*/, { value: void 0 }];
                                    return [2 /*return*/];
                            }
                        });
                    };
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 3)) return [3 /*break*/, 4];
                    return [5 /*yield**/, _loop_1(i)];
                case 2:
                    state_1 = _a.sent();
                    if (typeof state_1 === "object")
                        return [2 /*return*/, state_1.value];
                    _a.label = 3;
                case 3:
                    i++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    });
}
function dragWithPreciseMonitoring(selector_1, targetDistance_1) {
    return __awaiter(this, arguments, void 0, function (selector, targetDistance, breakCondition, retries) {
        var success, adjustedTarget, handle, box, startX, startY, endX, approachStartX, approachStartY, approachPoints, _i, approachPoints_1, point, initialX, initialY, numSegments, lastX, lastY, waypoints, i, segmentTarget, yVariation, i, point, curvePoints, _loop_2, _a, curvePoints_1, curvePoint, state_2, finalAdjustments, finalX, finalY, i, precision, adjustX, adjustY, targetX, holdTime_1, veryFinalX, veryFinalY, err_1;
        if (breakCondition === void 0) { breakCondition = null; }
        if (retries === void 0) { retries = 3; }
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    success = false;
                    console.log("Preparing to drag ".concat(selector, " with precise monitoring"));
                    adjustedTarget = targetDistance;
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 28, , 29]);
                    return [4 /*yield*/, waitForElement(selector)];
                case 2:
                    handle = _b.sent();
                    box = handle.getBoundingClientRect();
                    startX = box.x + (box.width / 2);
                    startY = box.y + (box.height / 2);
                    endX = startX + adjustedTarget;
                    approachStartX = startX - 80 - Math.random() * 40;
                    approachStartY = startY + 40 + Math.random() * 30;
                    approachPoints = generateNaturalApproach({ x: approachStartX, y: approachStartY }, { x: startX, y: startY }, 8 + Math.floor(Math.random() * 4));
                    _i = 0, approachPoints_1 = approachPoints;
                    _b.label = 3;
                case 3:
                    if (!(_i < approachPoints_1.length)) return [3 /*break*/, 6];
                    point = approachPoints_1[_i];
                    moveMouseTo(point.x, point.y);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 15 + Math.random() * 25); })];
                case 4:
                    _b.sent();
                    _b.label = 5;
                case 5:
                    _i++;
                    return [3 /*break*/, 3];
                case 6: 
                // Hover on handle with slight jitter
                return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 200 + Math.random() * 150); })];
                case 7:
                    // Hover on handle with slight jitter
                    _b.sent();
                    moveMouseTo(startX + (Math.random() * 1.5 - 0.75), startY + (Math.random() * 1.5 - 0.75));
                    // Press down after a natural delay
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 350 + Math.random() * 200); })];
                case 8:
                    // Press down after a natural delay
                    _b.sent();
                    // Mouse down and initial movement
                    handle.dispatchEvent(new PointerEvent("mousedown", {
                        pointerType: "mouse",
                        width: 1,
                        height: 1,
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: startX,
                        clientY: startY
                    }));
                    handle.dispatchEvent(new DragEvent("dragstart", {
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: startX,
                        clientY: startY
                    }));
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 180 + Math.random() * 120); })];
                case 9:
                    _b.sent();
                    initialX = startX + 2 + (Math.random() * 1.5);
                    initialY = startY + (Math.random() * 1 - 0.5);
                    moveMouseTo(initialX, initialY);
                    handle.dispatchEvent(new DragEvent("drag", {
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: initialX,
                        clientY: initialY
                    }));
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 120 + Math.random() * 80); })];
                case 10:
                    _b.sent();
                    numSegments = 3 + Math.floor(Math.random() * 3);
                    lastX = initialX;
                    lastY = initialY;
                    waypoints = [];
                    for (i = 1; i <= numSegments; i++) {
                        segmentTarget = startX + (adjustedTarget * (i / numSegments) * (0.85 + Math.random() * 0.3));
                        yVariation = Math.sin(i / numSegments * Math.PI) * (Math.random() * 4 - 2);
                        waypoints.push({
                            x: segmentTarget,
                            y: startY + yVariation
                        });
                    }
                    waypoints.push({
                        x: endX,
                        y: startY + (Math.random() * 1.2 - 0.6)
                    });
                    i = 0;
                    _b.label = 11;
                case 11:
                    if (!(i < waypoints.length)) return [3 /*break*/, 19];
                    if (breakCondition && breakCondition()) {
                        console.log('Break condition satisfied, puzzle solved!');
                        success = true;
                        return [3 /*break*/, 19];
                    }
                    point = waypoints[i];
                    curvePoints = generateNaturalCurve({ x: lastX, y: lastY }, point, 10 + Math.floor(Math.random() * 8));
                    _loop_2 = function (curvePoint) {
                        var tremorX, tremorY, isSlowingDown, baseDelay;
                        return __generator(this, function (_c) {
                            switch (_c.label) {
                                case 0:
                                    if (breakCondition && breakCondition()) {
                                        console.log('Break condition satisfied, puzzle solved!');
                                        success = true;
                                        return [2 /*return*/, "break"];
                                    }
                                    tremorX = curvePoint.x + (Math.random() * 0.6 - 0.3);
                                    tremorY = curvePoint.y + (Math.random() * 0.6 - 0.3);
                                    moveMouseTo(tremorX, tremorY);
                                    handle.dispatchEvent(new DragEvent("drag", {
                                        cancelable: true,
                                        bubbles: true,
                                        view: window,
                                        clientX: tremorX,
                                        clientY: tremorY
                                    }));
                                    isSlowingDown = i >= waypoints.length - 2;
                                    baseDelay = isSlowingDown ? 20 : 8;
                                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, baseDelay + Math.random() * (isSlowingDown ? 15 : 8)); })];
                                case 1:
                                    _c.sent();
                                    return [2 /*return*/];
                            }
                        });
                    };
                    _a = 0, curvePoints_1 = curvePoints;
                    _b.label = 12;
                case 12:
                    if (!(_a < curvePoints_1.length)) return [3 /*break*/, 15];
                    curvePoint = curvePoints_1[_a];
                    return [5 /*yield**/, _loop_2(curvePoint)];
                case 13:
                    state_2 = _b.sent();
                    if (state_2 === "break")
                        return [3 /*break*/, 15];
                    _b.label = 14;
                case 14:
                    _a++;
                    return [3 /*break*/, 12];
                case 15:
                    if (!(Math.random() < 0.3 && i < waypoints.length - 1)) return [3 /*break*/, 17];
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 80 + Math.random() * 120); })];
                case 16:
                    _b.sent();
                    _b.label = 17;
                case 17:
                    lastX = point.x;
                    lastY = point.y;
                    _b.label = 18;
                case 18:
                    i++;
                    return [3 /*break*/, 11];
                case 19:
                    finalAdjustments = 4 + Math.floor(Math.random() * 3);
                    finalX = lastX;
                    finalY = lastY;
                    i = 0;
                    _b.label = 20;
                case 20:
                    if (!(i < finalAdjustments)) return [3 /*break*/, 24];
                    if (breakCondition && breakCondition()) {
                        console.log('Break condition satisfied, puzzle solved!');
                        success = true;
                        return [3 /*break*/, 24];
                    }
                    precision = 1 - (i / finalAdjustments);
                    adjustX = (Math.random() * 1.0 - 0.5) * precision * (i === finalAdjustments - 1 ? 0.3 : 0.8);
                    adjustY = (Math.random() * 0.8 - 0.4) * precision * (i === finalAdjustments - 1 ? 0.3 : 0.8);
                    finalX += adjustX;
                    finalY += adjustY;
                    moveMouseTo(finalX, finalY);
                    handle.dispatchEvent(new DragEvent("drag", {
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: finalX,
                        clientY: finalY
                    }));
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 120 + Math.random() * 180); })];
                case 21:
                    _b.sent();
                    if (!(i === finalAdjustments - 2)) return [3 /*break*/, 23];
                    targetX = endX - finalX;
                    if (!(Math.abs(targetX) > 0.5)) return [3 /*break*/, 23];
                    finalX += targetX * 0.8;
                    moveMouseTo(finalX, finalY);
                    handle.dispatchEvent(new DragEvent("drag", {
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: finalX,
                        clientY: finalY
                    }));
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 200 + Math.random() * 100); })];
                case 22:
                    _b.sent();
                    _b.label = 23;
                case 23:
                    i++;
                    return [3 /*break*/, 20];
                case 24:
                    holdTime_1 = 3000 + Math.random() * 3000;
                    console.log("Holding at final position for ".concat(Math.round(holdTime_1), "ms"));
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, holdTime_1); })];
                case 25:
                    _b.sent();
                    veryFinalX = finalX + (Math.random() * 0.3 - 0.15);
                    veryFinalY = finalY + (Math.random() * 0.3 - 0.15);
                    moveMouseTo(veryFinalX, veryFinalY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 50 + Math.random() * 30); })];
                case 26:
                    _b.sent();
                    // Release mouse
                    handle.dispatchEvent(new PointerEvent("mouseup", {
                        pointerType: "mouse",
                        width: 1,
                        height: 1,
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: veryFinalX,
                        clientY: veryFinalY
                    }));
                    handle.dispatchEvent(new DragEvent("dragend", {
                        cancelable: true,
                        bubbles: true,
                        view: window,
                        clientX: veryFinalX,
                        clientY: veryFinalY
                    }));
                    // Check if we're done
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 2500); })];
                case 27:
                    // Check if we're done
                    _b.sent();
                    return [3 /*break*/, 29];
                case 28:
                    err_1 = _b.sent();
                    console.error("Drag error: ".concat(err_1.message));
                    return [3 /*break*/, 29];
                case 29: return [2 /*return*/, success];
            }
        });
    });
}
function clickMouse(element, x, y) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            element.dispatchEvent(new MouseEvent("click", {
                bubbles: true,
                clientX: x,
                clientY: y
            }));
            return [2 /*return*/];
        });
    });
}
function clickCenterOfElement(element) {
    return __awaiter(this, void 0, void 0, function () {
        var rect, x, y;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    rect = element.getBoundingClientRect();
                    x = rect.x + (rect.width / 2);
                    y = rect.y + (rect.height / 2);
                    return [4 /*yield*/, clickMouse(element, x, y)];
                case 1:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
function clickProportional(element, proportionX, proportionY) {
    return __awaiter(this, void 0, void 0, function () {
        var boundingBox, xOrigin, yOrigin, xOffset, yOffset, x, y;
        return __generator(this, function (_a) {
            boundingBox = element.getBoundingClientRect();
            xOrigin = boundingBox.x;
            yOrigin = boundingBox.y;
            xOffset = (proportionX * boundingBox.width);
            yOffset = (proportionY * boundingBox.height);
            x = xOrigin + xOffset;
            y = yOrigin + yOffset;
            clickMouse(element, x, y);
            return [2 /*return*/];
        });
    });
}
function computeRotateSlideDistance(angle, slideBarEle, slideIconEle) {
    return __awaiter(this, void 0, void 0, function () {
        var slideLength, iconLength;
        return __generator(this, function (_a) {
            slideLength = slideBarEle.getBoundingClientRect().width;
            iconLength = slideIconEle.getBoundingClientRect().width;
            return [2 /*return*/, ((slideLength - iconLength) * angle) / 360];
        });
    });
}
function computePuzzleSlideDistance(proportionX, puzzleImageEle) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, puzzleImageEle.getBoundingClientRect().width * proportionX];
        });
    });
}
function checkCaptchaSuccess() {
    return __awaiter(this, void 0, void 0, function () {
        var i;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 20)) return [3 /*break*/, 5];
                    if (!(document.evaluate(successXpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue !== null)) return [3 /*break*/, 2];
                    return [2 /*return*/, true];
                case 2: return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1000); })];
                case 3:
                    _a.sent();
                    _a.label = 4;
                case 4:
                    i++;
                    return [3 /*break*/, 1];
                case 5: return [2 /*return*/, false];
            }
        });
    });
}
function solveShapesV1() {
    return __awaiter(this, void 0, void 0, function () {
        var i, src, img, res, ele, submitButton;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 3)) return [3 /*break*/, 10];
                    return [4 /*yield*/, getImageSource(ShapesV1.IMAGE)];
                case 2:
                    src = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(src)];
                case 3:
                    img = _a.sent();
                    return [4 /*yield*/, shapesApiCall(img)];
                case 4:
                    res = _a.sent();
                    ele = document.querySelector(ShapesV1.IMAGE);
                    clickProportional(ele, res.pointOneProportionX, res.pointOneProportionY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 5:
                    _a.sent();
                    clickProportional(ele, res.pointTwoProportionX, res.pointTwoProportionY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 2337); })];
                case 6:
                    _a.sent();
                    submitButton = document.querySelector(ShapesV1.SUBMIT_BUTTON);
                    clickCenterOfElement(submitButton);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 7:
                    _a.sent();
                    return [4 /*yield*/, checkCaptchaSuccess()];
                case 8:
                    if (_a.sent())
                        return [2 /*return*/];
                    _a.label = 9;
                case 9:
                    i++;
                    return [3 /*break*/, 1];
                case 10: return [2 /*return*/];
            }
        });
    });
}
function solveShapesV2() {
    return __awaiter(this, void 0, void 0, function () {
        var src, img, res, ele, submitButton;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, getImageSource(ShapesV2.IMAGE)];
                case 1:
                    src = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(src)];
                case 2:
                    img = _a.sent();
                    return [4 /*yield*/, shapesApiCall(img)];
                case 3:
                    res = _a.sent();
                    ele = document.querySelector(ShapesV2.IMAGE);
                    clickProportional(ele, res.pointOneProportionX, res.pointOneProportionY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 4:
                    _a.sent();
                    clickProportional(ele, res.pointTwoProportionX, res.pointTwoProportionY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 2337); })];
                case 5:
                    _a.sent();
                    submitButton = document.querySelector(ShapesV2.SUBMIT_BUTTON);
                    clickCenterOfElement(submitButton);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 6:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
function solveRotateV1() {
    return __awaiter(this, void 0, void 0, function () {
        var i, outerSrc, innerSrc, outerImg, innerImg, solution, slideBar, slideButton, distance;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 3)) return [3 /*break*/, 11];
                    return [4 /*yield*/, getImageSource(RotateV1.OUTER)];
                case 2:
                    outerSrc = _a.sent();
                    return [4 /*yield*/, getImageSource(RotateV1.INNER)];
                case 3:
                    innerSrc = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(outerSrc)];
                case 4:
                    outerImg = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(innerSrc)];
                case 5:
                    innerImg = _a.sent();
                    return [4 /*yield*/, rotateApiCall(outerImg, innerImg)];
                case 6:
                    solution = _a.sent();
                    slideBar = document.querySelector(RotateV1.SLIDE_BAR);
                    slideButton = document.querySelector(RotateV1.SLIDER_DRAG_BUTTON);
                    return [4 /*yield*/, computeRotateSlideDistance(solution, slideBar, slideButton)];
                case 7:
                    distance = _a.sent();
                    return [4 /*yield*/, dragWithPreciseMonitoring(RotateV1.SLIDER_DRAG_BUTTON, distance)];
                case 8:
                    _a.sent();
                    return [4 /*yield*/, checkCaptchaSuccess()];
                case 9:
                    if (_a.sent())
                        return [2 /*return*/];
                    _a.label = 10;
                case 10:
                    i++;
                    return [3 /*break*/, 1];
                case 11: return [2 /*return*/];
            }
        });
    });
}
function solveRotateV2() {
    return __awaiter(this, void 0, void 0, function () {
        var i, outerSrc, innerSrc, outerImg, innerImg, solution, slideBar, slideButton, distance;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 3)) return [3 /*break*/, 11];
                    return [4 /*yield*/, getImageSource(RotateV2.OUTER)];
                case 2:
                    outerSrc = _a.sent();
                    return [4 /*yield*/, getImageSource(RotateV2.INNER)];
                case 3:
                    innerSrc = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(outerSrc)];
                case 4:
                    outerImg = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(innerSrc)];
                case 5:
                    innerImg = _a.sent();
                    return [4 /*yield*/, rotateApiCall(outerImg, innerImg)];
                case 6:
                    solution = _a.sent();
                    slideBar = document.querySelector(RotateV2.SLIDE_BAR);
                    slideButton = document.querySelector(RotateV2.SLIDER_DRAG_BUTTON);
                    return [4 /*yield*/, computeRotateSlideDistance(solution, slideBar, slideButton)];
                case 7:
                    distance = _a.sent();
                    return [4 /*yield*/, dragWithPreciseMonitoring(RotateV2.SLIDER_DRAG_BUTTON, distance)];
                case 8:
                    _a.sent();
                    return [4 /*yield*/, checkCaptchaSuccess()];
                case 9:
                    if (_a.sent())
                        return [2 /*return*/];
                    _a.label = 10;
                case 10:
                    i++;
                    return [3 /*break*/, 1];
                case 11: return [2 /*return*/];
            }
        });
    });
}
function solvePuzzleV1() {
    return __awaiter(this, void 0, void 0, function () {
        var i, puzzleSrc, pieceSrc, puzzleImg, pieceImg, solution, puzzleImageEle, distance;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 3)) return [3 /*break*/, 11];
                    return [4 /*yield*/, getImageSource(PuzzleV1.PUZZLE)];
                case 2:
                    puzzleSrc = _a.sent();
                    return [4 /*yield*/, getImageSource(PuzzleV1.PIECE)];
                case 3:
                    pieceSrc = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(puzzleSrc)];
                case 4:
                    puzzleImg = _a.sent();
                    return [4 /*yield*/, fetchImageBase64(pieceSrc)];
                case 5:
                    pieceImg = _a.sent();
                    return [4 /*yield*/, puzzleApiCall(puzzleImg, pieceImg)];
                case 6:
                    solution = _a.sent();
                    puzzleImageEle = document.querySelector(PuzzleV1.PUZZLE);
                    return [4 /*yield*/, computePuzzleSlideDistance(solution, puzzleImageEle)];
                case 7:
                    distance = _a.sent();
                    return [4 /*yield*/, dragWithPreciseMonitoring(PuzzleV1.SLIDER_DRAG_BUTTON, distance)];
                case 8:
                    _a.sent();
                    return [4 /*yield*/, checkCaptchaSuccess()];
                case 9:
                    if (_a.sent())
                        return [2 /*return*/];
                    _a.label = 10;
                case 10:
                    i++;
                    return [3 /*break*/, 1];
                case 11: return [2 /*return*/];
            }
        });
    });
}
function solveIconV1() {
    return __awaiter(this, void 0, void 0, function () {
        var i, src, img, challenge, res, ele, _i, _a, point, submitButton;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    i = 0;
                    _b.label = 1;
                case 1:
                    if (!(i < 3)) return [3 /*break*/, 12];
                    return [4 /*yield*/, getImageSource(IconV1.IMAGE)];
                case 2:
                    src = _b.sent();
                    return [4 /*yield*/, fetchImageBase64(src)];
                case 3:
                    img = _b.sent();
                    challenge = document.querySelector(IconV1.TEXT).textContent;
                    return [4 /*yield*/, iconApiCall(challenge, img)];
                case 4:
                    res = _b.sent();
                    ele = document.querySelector(IconV1.IMAGE);
                    _i = 0, _a = res.proportionalPoints;
                    _b.label = 5;
                case 5:
                    if (!(_i < _a.length)) return [3 /*break*/, 8];
                    point = _a[_i];
                    clickProportional(ele, point.proportionX, point.proportionY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 6:
                    _b.sent();
                    _b.label = 7;
                case 7:
                    _i++;
                    return [3 /*break*/, 5];
                case 8:
                    submitButton = document.querySelector(IconV1.SUBMIT_BUTTON);
                    clickCenterOfElement(submitButton);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 9:
                    _b.sent();
                    return [4 /*yield*/, checkCaptchaSuccess()];
                case 10:
                    if (_b.sent())
                        return [2 /*return*/];
                    _b.label = 11;
                case 11:
                    i++;
                    return [3 /*break*/, 1];
                case 12: return [2 /*return*/];
            }
        });
    });
}
function solveIconV2() {
    return __awaiter(this, void 0, void 0, function () {
        var src, img, challenge, res, ele, _i, _a, point, submitButton;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, getImageSource(IconV2.IMAGE)];
                case 1:
                    src = _b.sent();
                    return [4 /*yield*/, fetchImageBase64(src)];
                case 2:
                    img = _b.sent();
                    challenge = document.querySelector(IconV2.TEXT).textContent;
                    return [4 /*yield*/, iconApiCall(challenge, img)];
                case 3:
                    res = _b.sent();
                    ele = document.querySelector(IconV2.IMAGE);
                    _i = 0, _a = res.proportionalPoints;
                    _b.label = 4;
                case 4:
                    if (!(_i < _a.length)) return [3 /*break*/, 7];
                    point = _a[_i];
                    clickProportional(ele, point.proportionX, point.proportionY);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 5:
                    _b.sent();
                    _b.label = 6;
                case 6:
                    _i++;
                    return [3 /*break*/, 4];
                case 7:
                    submitButton = document.querySelector(IconV2.SUBMIT_BUTTON);
                    clickCenterOfElement(submitButton);
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 1337); })];
                case 8:
                    _b.sent();
                    return [4 /*yield*/, checkCaptchaSuccess()];
                case 9:
                    if (_b.sent())
                        return [2 /*return*/];
                    return [2 /*return*/];
            }
        });
    });
}
function generateNaturalCurve(start, end, steps) {
    var points = [];
    var controlPoint = {
        x: start.x + (end.x - start.x) * (0.3 + Math.random() * 0.4),
        y: start.y + (Math.random() * 12 - 6)
    };
    for (var i = 0; i <= steps; i++) {
        var t = i / steps;
        var x = Math.pow(1 - t, 2) * start.x + 2 * (1 - t) * t * controlPoint.x + Math.pow(t, 2) * end.x;
        var y = Math.pow(1 - t, 2) * start.y + 2 * (1 - t) * t * controlPoint.y + Math.pow(t, 2) * end.y;
        points.push({ x: x, y: y });
    }
    return points;
}
function generateNaturalApproach(start, end, steps) {
    var control1 = {
        x: start.x + (end.x - start.x) * (0.2 + Math.random() * 0.2),
        y: start.y + (Math.random() * 15 - 5)
    };
    var control2 = {
        x: start.x + (end.x - start.x) * (0.6 + Math.random() * 0.2),
        y: end.y + (Math.random() * 10 - 5)
    };
    var points = [];
    for (var i = 0; i <= steps; i++) {
        var t = i / steps;
        var x = Math.pow(1 - t, 3) * start.x +
            3 * Math.pow(1 - t, 2) * t * control1.x +
            3 * (1 - t) * Math.pow(t, 2) * control2.x +
            Math.pow(t, 3) * end.x;
        var y = Math.pow(1 - t, 3) * start.y +
            3 * Math.pow(1 - t, 2) * t * control1.y +
            3 * (1 - t) * Math.pow(t, 2) * control2.y +
            Math.pow(t, 3) * end.y;
        points.push({ x: x, y: y });
    }
    return points;
}
var isCurrentSolve = false;
function solveCaptchaLoop() {
    return __awaiter(this, void 0, void 0, function () {
        var _, captchaType, e_1, _a, err_2;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    if (!!isCurrentSolve) return [3 /*break*/, 29];
                    return [4 /*yield*/, waitForAnyElementInList([Wrappers.V1, Wrappers.V2])];
                case 1:
                    _ = _b.sent();
                    return [4 /*yield*/, identifyCaptcha()];
                case 2:
                    captchaType = _b.sent();
                    _b.label = 3;
                case 3:
                    _b.trys.push([3, 5, , 6]);
                    return [4 /*yield*/, creditsApiCall()];
                case 4:
                    if ((_b.sent()) <= 0) {
                        console.log("out of credits");
                        alert("Out of SadCaptcha credits. Please boost your balance on sadcaptcha.com/dashboard.");
                        return [2 /*return*/];
                    }
                    return [3 /*break*/, 6];
                case 5:
                    e_1 = _b.sent();
                    // Catch the error because we dont want to break the solver just because we failed to fetch the credits API
                    console.log("error making check credits api call: " + e_1);
                    return [3 /*break*/, 6];
                case 6:
                    isCurrentSolve = true;
                    _b.label = 7;
                case 7:
                    _b.trys.push([7, 25, 26, 29]);
                    _a = captchaType;
                    switch (_a) {
                        case CaptchaType.PUZZLE_V1: return [3 /*break*/, 8];
                        case CaptchaType.ROTATE_V1: return [3 /*break*/, 10];
                        case CaptchaType.SHAPES_V1: return [3 /*break*/, 12];
                        case CaptchaType.ICON_V1: return [3 /*break*/, 14];
                        case CaptchaType.PUZZLE_V2: return [3 /*break*/, 16];
                        case CaptchaType.ROTATE_V2: return [3 /*break*/, 18];
                        case CaptchaType.SHAPES_V2: return [3 /*break*/, 20];
                        case CaptchaType.ICON_V2: return [3 /*break*/, 22];
                    }
                    return [3 /*break*/, 24];
                case 8: return [4 /*yield*/, solvePuzzleV1()];
                case 9:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 10: return [4 /*yield*/, solveRotateV1()];
                case 11:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 12: return [4 /*yield*/, solveShapesV1()];
                case 13:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 14: return [4 /*yield*/, solveIconV1()];
                case 15:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 16: return [4 /*yield*/, solvePuzzleV2()];
                case 17:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 18: return [4 /*yield*/, solveRotateV2()];
                case 19:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 20: return [4 /*yield*/, solveShapesV2()];
                case 21:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 22: return [4 /*yield*/, solveIconV2()];
                case 23:
                    _b.sent();
                    return [3 /*break*/, 24];
                case 24: return [3 /*break*/, 29];
                case 25:
                    err_2 = _b.sent();
                    console.log("error solving captcha");
                    console.error(err_2);
                    console.log("restarting captcha loop");
                    return [3 /*break*/, 29];
                case 26:
                    isCurrentSolve = false;
                    return [4 /*yield*/, new Promise(function (r) { return setTimeout(r, 5000); })];
                case 27:
                    _b.sent();
                    return [4 /*yield*/, solveCaptchaLoop()];
                case 28:
                    _b.sent();
                    return [7 /*endfinally*/];
                case 29: return [2 /*return*/];
            }
        });
    });
}
// Api key is passed from extension via message
var apiKey = "925d4ebe0258d96923994633efe2361f";;
try {
    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        if (request.apiKey !== null) {
            console.log("Api key: " + request.apiKey);
            apiKey = request.apiKey;
            localStorage.setItem("sadCaptchaKey", apiKey);
            sendResponse({ message: "API key set.", success: 1 });
        }
        else {
            sendResponse({ message: "API key cannot be empty.", success: 0 });
        }
    });
}
catch (err) {
    console.warn("Chrome runtime is not available");
}
solveCaptchaLoop();
