const creditsUrl = "https://www.sadcaptcha.com/api/v1/license/credits?licenseKey="
const rotateUrl = "https://www.sadcaptcha.com/api/v1/rotate?licenseKey="
const puzzleUrl = "https://www.sadcaptcha.com/api/v1/puzzle?licenseKey="
const shapesUrl = "https://www.sadcaptcha.com/api/v1/shapes?licenseKey="
const iconUrl = "https://www.sadcaptcha.com/api/v1/icon?licenseKey="
const successXpath = "//*[contains(text(), 'Verification complete')]"
const apiHeaders = new Headers({ "Content-Type": "application/json" })
const CONTAINER: Element = document.documentElement || document.body

const Wrappers = {
	V1: ".captcha-disable-scroll",
	V2: ".captcha-verify-container"
}

const RotateV1 = {
	INNER: "[data-testid=whirl-inner-img]",
	OUTER: "[data-testid=whirl-outer-img]",
	SLIDE_BAR: ".captcha_verify_slide--slidebar",
	SLIDER_DRAG_BUTTON: ".secsdk-captcha-drag-icon",
	UNIQUE_IDENTIFIER: ".captcha-disable-scroll [data-testid=whirl-inner-img]"
}

const RotateV2 = {
	INNER: ".captcha-verify-container > div > div > div > img.cap-absolute",
	OUTER: ".captcha-verify-container > div > div > div > img:first-child",
	SLIDE_BAR: ".captcha-verify-container > div > div > div.cap-w-full > div.cap-rounded-full",
	SLIDER_DRAG_BUTTON: "div[draggable=true]:has(.secsdk-captcha-drag-icon)",
	UNIQUE_IDENTIFIER: ".captcha-verify-container > div > div > div > img.cap-absolute"
}

const PuzzleV1 = {
	PIECE: "img.captcha_verify_img_slide",
	PUZZLE: "#captcha-verify-image",
	SLIDER_DRAG_BUTTON: ".secsdk-captcha-drag-icon",
	UNIQUE_IDENTIFIER: ".captcha-disable-scroll img.captcha_verify_img_slide"
}

const PuzzleV2 = {
	PIECE: ".captcha-verify-container .cap-absolute img",
	PUZZLE: "#captcha-verify-image",
	SLIDER_DRAG_BUTTON: "div[draggable=true]:has(.secsdk-captcha-drag-icon)",
    PIECE_IMAGE_CONTAINER: ".captcha-verify-container div[draggable=true]:has(img[draggable=false])",
	UNIQUE_IDENTIFIER: ".captcha-verify-container #captcha-verify-image"
}

const ShapesV1 = {
	IMAGE: "#captcha-verify-image",
	SUBMIT_BUTTON: ".verify-captcha-submit-button" ,
	UNIQUE_IDENTIFIER: ".captcha-disable-scroll .verify-captcha-submit-button"
}

const ShapesV2 = {
	IMAGE: ".captcha-verify-container div.cap-relative img",
	SUBMIT_BUTTON: ".captcha-verify-container .cap-relative button.cap-w-full" ,
	UNIQUE_IDENTIFIER: ".captcha-verify-container .cap-relative button.cap-w-full" 
}

const IconV1 = {
	IMAGE: "#captcha-verify-image",
	SUBMIT_BUTTON: ".verify-captcha-submit-button" ,
	TEXT: ".captcha_verify_bar",
	UNIQUE_IDENTIFIER: ".captcha-disable-scroll .verify-captcha-submit-button"
}

const IconV2 = {
	IMAGE: ".captcha-verify-container div.cap-relative img",
	SUBMIT_BUTTON: ".captcha-verify-container .cap-relative button.cap-w-full" ,
	TEXT: ".captcha-verify-container > div > div > span"
}

type ShapesCaptchaResponse = {
	pointOneProportionX: number
	pointOneProportionY: number
	pointTwoProportionX: number
	pointTwoProportionY: number
}

type ProportionalPoint = {
	proportionX: number
	proportionY: number
}

type IconCaptchaResponse = {
	proportionalPoints: Array<ProportionalPoint>
}

interface Request {
	apiKey: string
}

enum CaptchaType {
	PUZZLE_V1,
	ROTATE_V1,
	SHAPES_V1,
	ICON_V1,
	PUZZLE_V2,
	ROTATE_V2,
	SHAPES_V2,
	ICON_V2
}

function waitForAnyElementInList(selectors: Array<string>): Promise<Element> {
	return new Promise(resolve => {
		let selectorFound: string = null

		// Check if already present
		selectors.forEach(selector => {
			if (document.querySelector(selector)) {
				selectorFound = selector
				console.log("Selector found: " + selector)
				return resolve(document.querySelector(selectorFound))
			}
		})
		if (selectorFound !== null) {
			return resolve(document.querySelector(selectorFound))
		}

		// Then start waiting if not found immediately
		const observer: MutationObserver = new MutationObserver(mutations => {
			selectors.forEach(selector => {
				if (document.querySelector(selector)) {
					selectorFound = selector
					console.log("Selector found by mutation observer: " + selector)
					observer.disconnect()
					return
				}
			})
			if (selectorFound !== null) {
				console.log("returning selector from mutation observer: " + selectorFound)
				return resolve(document.querySelector(selectorFound))
			} else {
				console.log("unimportant mutation seen")
			}
		})

		observer.observe(CONTAINER, {
			childList: true,
			subtree: true
		})
	})
}

function waitForElement(selector: string): Promise<Element> {
	return new Promise(resolve => {
		if (document.querySelector(selector)) {
			console.log("Selector found: " + selector)
			return resolve(document.querySelector(selector)!)
		} else {
			const observer: MutationObserver = new MutationObserver(mutations => {
				if (document.querySelector(selector)) {
					observer.disconnect()
					console.log("Selector found by mutation observer: " + selector)
					return resolve(document.querySelector(selector)!)
				}
			})

			observer.observe(CONTAINER, {
				childList: true,
				subtree: true
			})
		}
	})
}

async function creditsApiCall(): Promise<number> {
	let resp = await fetch(creditsUrl + apiKey, {
		method: "GET",
		headers: apiHeaders,
	})
	let credits = (await resp.json()).credits
	console.log("api credits = " + credits)
	return credits
}

async function rotateApiCall(outerB64: string, innerB64: string): Promise<number> {
	let resp = await fetch(rotateUrl + apiKey, {
		method: "POST",
		headers: apiHeaders,
		body: JSON.stringify({
			outerImageB64: outerB64,
			innerImageB64: innerB64
		})
	})
	let angle = (await resp.json()).angle
	console.log("angle = " + angle)
	return angle
}

async function puzzleApiCall(puzzleB64: string, pieceB64: string): Promise<number> {
	let resp = await fetch(puzzleUrl + apiKey, {
		method: "POST",
		headers: apiHeaders,
		body: JSON.stringify({
			puzzleImageB64: puzzleB64,
			pieceImageB64: pieceB64
		})
	})
	let slideXProportion = (await resp.json()).slideXProportion
	console.log("slideXProportion = " + slideXProportion)
	return slideXProportion
}

async function shapesApiCall(imageB64: string): Promise<ShapesCaptchaResponse> {
	let resp = await fetch(shapesUrl + apiKey, {
		method: "POST",
		headers: apiHeaders,
		body: JSON.stringify({
			imageB64: imageB64
		})
	})
	let data = await resp.json()
	console.log("Shapes response data:")
	console.log(data)
	return {
		pointOneProportionX: data.pointOneProportionX,
		pointOneProportionY: data.pointOneProportionY,
		pointTwoProportionX: data.pointTwoProportionX,
		pointTwoProportionY: data.pointTwoProportionY
	}
}

async function iconApiCall(challenge: string, imageB64: string): Promise<IconCaptchaResponse> {
	let resp = await fetch(iconUrl + apiKey, {
		method: "POST",
		headers: apiHeaders,
		body: JSON.stringify({
			challenge: challenge,
			imageB64: imageB64
		})
	})
	let data = await resp.json()
	console.log("Icon response data:")
	console.log(data)
	return data
}

function anySelectorInListPresent(selectors: Array<string>): boolean {
	for (const selector of selectors) {
		let ele = document.querySelector(selector)
		if (ele !== null) {
			return true
		}
	}
	return false
}

async function identifyCaptcha(): Promise<CaptchaType> {
	for (let i = 0; i < 30; i++) {
		if (anySelectorInListPresent([RotateV1.UNIQUE_IDENTIFIER])) {
			console.log("rotate v1 detected")
			return CaptchaType.ROTATE_V1
		} else if (anySelectorInListPresent([PuzzleV1.UNIQUE_IDENTIFIER])) {
			console.log("puzzle v1 detected")
			return CaptchaType.PUZZLE_V1
		} else if (anySelectorInListPresent([ShapesV1.UNIQUE_IDENTIFIER])) {
			let imgUrl: string = await getImageSource(ShapesV2.IMAGE)
			if (imgUrl.includes("/icon")) {
				console.log("icon v1 detected")
				return CaptchaType.ICON_V1
			} else {
				console.log("shapes v1 detected")
				return CaptchaType.SHAPES_V1
			}
		} else if (anySelectorInListPresent([RotateV2.UNIQUE_IDENTIFIER])) {
			console.log("rotate v2 detected")
			return CaptchaType.ROTATE_V2
		} else if (anySelectorInListPresent([PuzzleV2.UNIQUE_IDENTIFIER])) {
			console.log("puzzle v2 detected")
			return CaptchaType.PUZZLE_V2
		} else if (anySelectorInListPresent([ShapesV2.UNIQUE_IDENTIFIER])) {
			let imgUrl: string = await getImageSource(ShapesV2.IMAGE)
			if (imgUrl.includes("/icon")) {
				console.log("icon v1 detected")
				return CaptchaType.ICON_V2
			} else {
				console.log("shapes v2 detected")
				return CaptchaType.SHAPES_V2
			}
		} else {
			await new Promise(r => setTimeout(r, 1000));
		}
	}
	throw new Error("Could not identify CaptchaType")
}

async function getImageSource(selector: string): Promise<string> {
	let ele = await waitForElement(selector)
	let src = ele.getAttribute("src")
	console.log("src = " + selector)
	return src
}

function getBase64StringFromDataURL(dataUrl: string): string {
	return dataUrl.replace('data:', '').replace(/^.+,/, '')
}

async function fetchImageBase64(imageSource: string): Promise<string> {
	let res = await fetch(imageSource)
	let img = await res.blob()
	let reader = new FileReader()
	reader.readAsDataURL(img)
	return new Promise(resolve => {
		reader.onloadend = () => {
			resolve(getBase64StringFromDataURL(reader.result as string))
		}
	})
}

async function moveMouseTo(x: number, y: number): Promise<void> {
	CONTAINER.dispatchEvent(
		new MouseEvent("mousemove", {
			bubbles: true,
			view: window,
			clientX: x,
			clientY: y
		})
	)
	console.log("moved mouse to " + x + ", " + y)
}

async function solvePuzzleV2(): Promise<void> {
	for (let i = 0; i < 3; i++) {
		let puzzleSrc = await getImageSource(PuzzleV2.PUZZLE)
		let pieceSrc = await getImageSource(PuzzleV2.PIECE)
		let puzzleImg = await fetchImageBase64(puzzleSrc)
		let pieceImg = await fetchImageBase64(pieceSrc)
		let solution = await puzzleApiCall(puzzleImg, pieceImg)
		let puzzleImageEle = document.querySelector(PuzzleV2.PUZZLE)
		let distance = await computePuzzleSlideDistance(solution, puzzleImageEle) 

		let adjustment = 3
		distance = distance - adjustment

		function pieceHasReachedTargetLocation(): boolean {
			let piece = document.querySelector(PuzzleV2.PIECE_IMAGE_CONTAINER)
			let style = piece.getAttribute("style")
			console.log("piece style: " + style)
			let translateX = parseInt(style.match("(?<=translateX\\()[0-9]+").toString());
			console.debug("translateX: " + translateX)
			if (translateX >= distance) {
				console.debug("piece has reached target location")
				return true
			} else {
				console.debug("piece has not reached target location")
				return false
			}
		}

		await dragWithPreciseMonitoring(
			PuzzleV2.SLIDER_DRAG_BUTTON,
			distance,
			pieceHasReachedTargetLocation
		)
		if (await checkCaptchaSuccess())
			return;
	}
}

async function dragWithPreciseMonitoring(
    selector: string, 
    targetDistance: number, 
    breakCondition: Function = null,
    retries: number = 3
): Promise<boolean> {
    let success = false;

    console.log(`Preparing to drag ${selector} with precise monitoring`);
	const adjustedTarget = targetDistance 

	try {
		const handle = await waitForElement(selector);
		const box = handle.getBoundingClientRect();
		const startX = box.x + (box.width / 2);
		const startY = box.y + (box.height / 2);
		const endX = startX + adjustedTarget;

		// Natural approach to the handle
		const approachStartX = startX - 80 - Math.random() * 40;
		const approachStartY = startY + 40 + Math.random() * 30;
		const approachPoints = generateNaturalApproach(
			{ x: approachStartX, y: approachStartY },
			{ x: startX, y: startY },
			8 + Math.floor(Math.random() * 4)
		);

		// Move cursor to approach the handle naturally
		for (const point of approachPoints) {
			moveMouseTo(point.x, point.y);
			await new Promise(r => setTimeout(r, 15 + Math.random() * 25));
		}

		// Hover on handle with slight jitter
		await new Promise(r => setTimeout(r, 200 + Math.random() * 150));
		moveMouseTo(
			startX + (Math.random() * 1.5 - 0.75),
			startY + (Math.random() * 1.5 - 0.75)
		);

		// Press down after a natural delay
		await new Promise(r => setTimeout(r, 350 + Math.random() * 200));
		
		// Mouse down and initial movement
		handle.dispatchEvent(
			new PointerEvent("mousedown", {
				pointerType: "mouse",
				width: 1,
				height: 1,
				cancelable: true,
				bubbles: true,
				view: window,
				clientX: startX,
				clientY: startY
			})
		);
		
		handle.dispatchEvent(
			new DragEvent("dragstart", {
				cancelable: true,
				bubbles: true,
				view: window,
				clientX: startX,
				clientY: startY
			})
		);

		await new Promise(r => setTimeout(r, 180 + Math.random() * 120));
		
		// Initial small movement
		const initialX = startX + 2 + (Math.random() * 1.5);
		const initialY = startY + (Math.random() * 1 - 0.5);
		
		moveMouseTo(initialX, initialY);
		handle.dispatchEvent(
			new DragEvent("drag", {
				cancelable: true,
				bubbles: true,
				view: window,
				clientX: initialX,
				clientY: initialY
			})
		);
		
		await new Promise(r => setTimeout(r, 120 + Math.random() * 80));
		
		// Create segmented movement with waypoints
		const numSegments = 3 + Math.floor(Math.random() * 3);
		let lastX = initialX;
		let lastY = initialY;
		
		const waypoints = [];
		for (let i = 1; i <= numSegments; i++) {
			const segmentTarget = startX + (adjustedTarget * (i/numSegments) * (0.85 + Math.random() * 0.3));
			const yVariation = Math.sin(i / numSegments * Math.PI) * (Math.random() * 4 - 2);
			
			waypoints.push({
				x: segmentTarget,
				y: startY + yVariation
			});
		}
		
		waypoints.push({
			x: endX,
			y: startY + (Math.random() * 1.2 - 0.6)
		});
		
		// Move through each waypoint with natural curves
		for (let i = 0; i < waypoints.length; i++) {
			if (breakCondition && breakCondition()) {
				console.log('Break condition satisfied, puzzle solved!');
				success = true;
				break;
			}

			const point = waypoints[i];
			
			const curvePoints = generateNaturalCurve(
				{ x: lastX, y: lastY },
				point,
				10 + Math.floor(Math.random() * 8)
			);
			
			for (const curvePoint of curvePoints) {
				if (breakCondition && breakCondition()) {
					console.log('Break condition satisfied, puzzle solved!');
					success = true;
					break;
				}

				// Add slight tremor to movement
				const tremorX = curvePoint.x + (Math.random() * 0.6 - 0.3);
				const tremorY = curvePoint.y + (Math.random() * 0.6 - 0.3);
				
				moveMouseTo(tremorX, tremorY);
				handle.dispatchEvent(
					new DragEvent("drag", {
						cancelable: true,
						bubbles: true,
						view: window,
						clientX: tremorX,
						clientY: tremorY
					})
				);
				
				const isSlowingDown = i >= waypoints.length - 2;
				const baseDelay = isSlowingDown ? 20 : 8;
				await new Promise(r => setTimeout(r, baseDelay + Math.random() * (isSlowingDown ? 15 : 8)));
			}
			
			// Random pauses during movement
			if (Math.random() < 0.3 && i < waypoints.length - 1) {
				await new Promise(r => setTimeout(r, 80 + Math.random() * 120));
			}
			
			lastX = point.x;
			lastY = point.y;
		}
		
		// Final micro-adjustments
		const finalAdjustments = 4 + Math.floor(Math.random() * 3);
		let finalX = lastX;
		let finalY = lastY;
		
		for (let i = 0; i < finalAdjustments; i++) {
			if (breakCondition && breakCondition()) {
				console.log('Break condition satisfied, puzzle solved!');
				success = true;
				break;
			}
			const precision = 1 - (i / finalAdjustments);
			
			const adjustX = (Math.random() * 1.0 - 0.5) * precision * (i === finalAdjustments - 1 ? 0.3 : 0.8);
			const adjustY = (Math.random() * 0.8 - 0.4) * precision * (i === finalAdjustments - 1 ? 0.3 : 0.8);
			
			finalX += adjustX;
			finalY += adjustY;
			
			moveMouseTo(finalX, finalY);
			handle.dispatchEvent(
				new DragEvent("drag", {
					cancelable: true,
					bubbles: true,
					view: window,
					clientX: finalX,
					clientY: finalY
				})
			);
			
			await new Promise(r => setTimeout(r, 120 + Math.random() * 180));
			
			// Last-second correction toward target
			if (i === finalAdjustments - 2) {
				const targetX = endX - finalX;
				if (Math.abs(targetX) > 0.5) {
					finalX += targetX * 0.8;
					moveMouseTo(finalX, finalY);
					handle.dispatchEvent(
						new DragEvent("drag", {
							cancelable: true,
							bubbles: true,
							view: window,
							clientX: finalX,
							clientY: finalY
						})
					);
					await new Promise(r => setTimeout(r, 200 + Math.random() * 100));
				}
			}
		}
		
		// Hold at final position
		const holdTime = 3000 + Math.random() * 3000;
		console.log(`Holding at final position for ${Math.round(holdTime)}ms`);
		await new Promise(r => setTimeout(r, holdTime));
		
		// Small final tremor
		const veryFinalX = finalX + (Math.random() * 0.3 - 0.15);
		const veryFinalY = finalY + (Math.random() * 0.3 - 0.15);
		moveMouseTo(veryFinalX, veryFinalY);
		
		await new Promise(r => setTimeout(r, 50 + Math.random() * 30));
		
		// Release mouse
		handle.dispatchEvent(
			new PointerEvent("mouseup", {
				pointerType: "mouse",
				width: 1,
				height: 1,
				cancelable: true,
				bubbles: true,
				view: window,
				clientX: veryFinalX,
				clientY: veryFinalY
			})
		);
		
		handle.dispatchEvent(
			new DragEvent("dragend", {
				cancelable: true,
				bubbles: true,
				view: window,
				clientX: veryFinalX,
				clientY: veryFinalY
			})
		);
		
		// Check if we're done
		await new Promise(r => setTimeout(r, 2500));
		
	} catch (err) {
		console.error(`Drag error: ${err.message}`);
	}

    return success;
}

async function clickMouse(element: Element, x: number, y: number): Promise<void> {
	element.dispatchEvent(
		new MouseEvent("click", {
			bubbles: true,
			clientX: x,
			clientY: y
		})
	)
}

async function clickCenterOfElement(element: Element): Promise<void> {
	let rect = element.getBoundingClientRect()
	let x = rect.x + (rect.width / 2)
	let y = rect.y + (rect.height / 2)
	await clickMouse(element, x, y)
}

async function clickProportional(element: Element, proportionX: number, proportionY: number): Promise<void> {
	let boundingBox = element.getBoundingClientRect()
	let xOrigin = boundingBox.x
	let yOrigin = boundingBox.y
	let xOffset = (proportionX * boundingBox.width)
	let yOffset = (proportionY * boundingBox.height)
	let x = xOrigin + xOffset
	let y = yOrigin + yOffset
	clickMouse(element, x, y)
}

async function computeRotateSlideDistance(angle: number, slideBarEle: Element, slideIconEle: Element): Promise<number> {
	let slideLength = slideBarEle.getBoundingClientRect().width
	let iconLength = slideIconEle.getBoundingClientRect().width
	return ((slideLength - iconLength) * angle) / 360
}

async function computePuzzleSlideDistance(proportionX: number, puzzleImageEle: Element): Promise<number> {
	return puzzleImageEle.getBoundingClientRect().width * proportionX
}

async function checkCaptchaSuccess(): Promise<boolean> {
	for (let i = 0; i < 20; i++) {
		if (document.evaluate(
			successXpath,
			document,
			null,
			XPathResult.FIRST_ORDERED_NODE_TYPE,
			null
		).singleNodeValue !== null)
			return true
		else
			await new Promise(r => setTimeout(r, 1000));
	}
	return false
}

async function solveShapesV1(): Promise<void> {
	for (let i = 0; i < 3; i++) {
		let src = await getImageSource(ShapesV1.IMAGE)
		let img = await fetchImageBase64(src)
		let res = await shapesApiCall(img)
		let ele = document.querySelector(ShapesV1.IMAGE)
		clickProportional(ele, res.pointOneProportionX, res.pointOneProportionY)
		await new Promise(r => setTimeout(r, 1337));
		clickProportional(ele, res.pointTwoProportionX, res.pointTwoProportionY)
		await new Promise(r => setTimeout(r, 2337));
		let submitButton = document.querySelector(ShapesV1.SUBMIT_BUTTON)
		clickCenterOfElement(submitButton)
		await new Promise(r => setTimeout(r, 1337));
		if (await checkCaptchaSuccess())
			return;
	}
}

async function solveShapesV2(): Promise<void> {
	let src = await getImageSource(ShapesV2.IMAGE)
	let img = await fetchImageBase64(src)
	let res = await shapesApiCall(img)
	let ele = document.querySelector(ShapesV2.IMAGE)
	clickProportional(ele, res.pointOneProportionX, res.pointOneProportionY)
	await new Promise(r => setTimeout(r, 1337));
	clickProportional(ele, res.pointTwoProportionX, res.pointTwoProportionY)
	await new Promise(r => setTimeout(r, 2337));
	let submitButton = document.querySelector(ShapesV2.SUBMIT_BUTTON)
	clickCenterOfElement(submitButton)
	await new Promise(r => setTimeout(r, 1337));
}

async function solveRotateV1(): Promise<void> {
	for (let i = 0; i < 3; i++) {
		let outerSrc = await getImageSource(RotateV1.OUTER)
		let innerSrc = await getImageSource(RotateV1.INNER)
		let outerImg = await fetchImageBase64(outerSrc)
		let innerImg = await fetchImageBase64(innerSrc)
		let solution = await rotateApiCall(outerImg, innerImg)
		let slideBar = document.querySelector(RotateV1.SLIDE_BAR)
		let slideButton = document.querySelector(RotateV1.SLIDER_DRAG_BUTTON)
		let distance = await computeRotateSlideDistance(solution, slideBar, slideButton)
		await dragWithPreciseMonitoring(RotateV1.SLIDER_DRAG_BUTTON, distance)
		if (await checkCaptchaSuccess())
			return;
	}
}

async function solveRotateV2(): Promise<void> {
	for (let i = 0; i < 3; i++) {
		let outerSrc = await getImageSource(RotateV2.OUTER)
		let innerSrc = await getImageSource(RotateV2.INNER)
		let outerImg = await fetchImageBase64(outerSrc)
		let innerImg = await fetchImageBase64(innerSrc)
		let solution = await rotateApiCall(outerImg, innerImg)
		let slideBar = document.querySelector(RotateV2.SLIDE_BAR)
		let slideButton = document.querySelector(RotateV2.SLIDER_DRAG_BUTTON)
		let distance = await computeRotateSlideDistance(solution, slideBar, slideButton)
		await dragWithPreciseMonitoring(RotateV2.SLIDER_DRAG_BUTTON, distance)
		if (await checkCaptchaSuccess())
			return;
	}
}

async function solvePuzzleV1(): Promise<void> {
	for (let i = 0; i < 3; i++) {
		let puzzleSrc = await getImageSource(PuzzleV1.PUZZLE)
		let pieceSrc = await getImageSource(PuzzleV1.PIECE)
		let puzzleImg = await fetchImageBase64(puzzleSrc)
		let pieceImg = await fetchImageBase64(pieceSrc)
		let solution = await puzzleApiCall(puzzleImg, pieceImg)
		let puzzleImageEle = document.querySelector(PuzzleV1.PUZZLE)
		let distance = await computePuzzleSlideDistance(solution, puzzleImageEle)
		await dragWithPreciseMonitoring(PuzzleV1.SLIDER_DRAG_BUTTON, distance)
		if (await checkCaptchaSuccess())
			return;
	}
}

async function solveIconV1(): Promise<void> {
	for (let i = 0; i < 3; i++) {
		let src = await getImageSource(IconV1.IMAGE)
		let img = await fetchImageBase64(src)
		let challenge: string = document.querySelector(IconV1.TEXT).textContent
		let res = await iconApiCall(challenge, img)
		let ele = document.querySelector(IconV1.IMAGE)
		for (const point of res.proportionalPoints) {
			clickProportional(ele, point.proportionX, point.proportionY)
			await new Promise(r => setTimeout(r, 1337));
		}
		let submitButton = document.querySelector(IconV1.SUBMIT_BUTTON)
		clickCenterOfElement(submitButton)
		await new Promise(r => setTimeout(r, 1337));
		if (await checkCaptchaSuccess())
			return;
	}
}

async function solveIconV2(): Promise<void> {
	let src = await getImageSource(IconV2.IMAGE)
	let img = await fetchImageBase64(src)
	let challenge: string = document.querySelector(IconV2.TEXT).textContent
	let res = await iconApiCall(challenge, img)
	let ele = document.querySelector(IconV2.IMAGE)
	for (const point of res.proportionalPoints) {
		clickProportional(ele, point.proportionX, point.proportionY)
		await new Promise(r => setTimeout(r, 1337));
	}
	let submitButton = document.querySelector(IconV2.SUBMIT_BUTTON)
	clickCenterOfElement(submitButton)
	await new Promise(r => setTimeout(r, 1337));
	if (await checkCaptchaSuccess())
		return;
}

function generateNaturalCurve(start: {x: number, y: number}, end: {x: number, y: number}, steps: number): Array<{x: number, y: number}> {
    const points = [];
    const controlPoint = {
        x: start.x + (end.x - start.x) * (0.3 + Math.random() * 0.4),
        y: start.y + (Math.random() * 12 - 6)
    };
    
    for (let i = 0; i <= steps; i++) {
        const t = i / steps;
        const x = Math.pow(1 - t, 2) * start.x + 2 * (1 - t) * t * controlPoint.x + Math.pow(t, 2) * end.x;
        const y = Math.pow(1 - t, 2) * start.y + 2 * (1 - t) * t * controlPoint.y + Math.pow(t, 2) * end.y;
        points.push({ x, y });
    }
    return points;
}

function generateNaturalApproach(start: {x: number, y: number}, end: {x: number, y: number}, steps: number): Array<{x: number, y: number}> {
    const control1 = {
        x: start.x + (end.x - start.x) * (0.2 + Math.random() * 0.2),
        y: start.y + (Math.random() * 15 - 5)
    };
    
    const control2 = {
        x: start.x + (end.x - start.x) * (0.6 + Math.random() * 0.2),
        y: end.y + (Math.random() * 10 - 5)
    };
    
    const points = [];
    for (let i = 0; i <= steps; i++) {
        const t = i / steps;
        const x = Math.pow(1 - t, 3) * start.x +
                  3 * Math.pow(1 - t, 2) * t * control1.x +
                  3 * (1 - t) * Math.pow(t, 2) * control2.x +
                  Math.pow(t, 3) * end.x;
                  
        const y = Math.pow(1 - t, 3) * start.y +
                  3 * Math.pow(1 - t, 2) * t * control1.y +
                  3 * (1 - t) * Math.pow(t, 2) * control2.y +
                  Math.pow(t, 3) * end.y;
        
        points.push({ x, y });
    }
    return points;
}

let isCurrentSolve: boolean = false
async function solveCaptchaLoop() {
	if (!isCurrentSolve) {
		const _: Element = await waitForAnyElementInList([Wrappers.V1, Wrappers.V2])
		const captchaType: CaptchaType = await identifyCaptcha()

		try {
			if (await creditsApiCall() <= 0) {
				console.log("out of credits")
				alert("Out of SadCaptcha credits. Please boost your balance on sadcaptcha.com/dashboard.")
				return
			}
		} catch (e) {
			// Catch the error because we dont want to break the solver just because we failed to fetch the credits API
			console.log("error making check credits api call: " + e)
		}
		
		isCurrentSolve = true
		try {
			switch (captchaType) {
				case CaptchaType.PUZZLE_V1:
					await solvePuzzleV1()
					break
				case CaptchaType.ROTATE_V1:
					await solveRotateV1()
					break
				case CaptchaType.SHAPES_V1:
					await solveShapesV1()
					break
				case CaptchaType.ICON_V1:
					await solveIconV1()
					break
				case CaptchaType.PUZZLE_V2:
					await solvePuzzleV2()
					break
				case CaptchaType.ROTATE_V2:
					await solveRotateV2()
					break
				case CaptchaType.SHAPES_V2:
					await solveShapesV2()
					break
				case CaptchaType.ICON_V2:
					await solveIconV2()
					break
				} 
			} catch (err) {
					console.log("error solving captcha")
					console.error(err)
					console.log("restarting captcha loop")
			} finally {
				isCurrentSolve = false
				await new Promise(r => setTimeout(r, 5000));
				await solveCaptchaLoop()
			}
		}
	}


// Api key is passed from extension via message
let apiKey: string = localStorage.getItem("sadCaptchaKey");
try {
	chrome.runtime.onMessage.addListener(
		function(request: Request, sender, sendResponse) {
			if (request.apiKey !== null) {
				console.log("Api key: " + request.apiKey)
				apiKey = request.apiKey
				localStorage.setItem("sadCaptchaKey", apiKey)
				sendResponse({ message: "API key set.", success: 1 })
			} else {
				sendResponse({ message: "API key cannot be empty.", success: 0 })
			} 
		}
	)
} catch (err) {
	console.warn("Chrome runtime is not available")
}
solveCaptchaLoop()

