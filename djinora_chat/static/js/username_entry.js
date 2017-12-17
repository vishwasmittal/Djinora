/**
 * Caching the references to the scene elements.
 */
var elements = {
    boxWrapper: document.getElementsByClassName("js-box-wrapper")[0],
    button: document.getElementsByClassName("js-button")[0],
    input: document.getElementsByClassName("js-input")[0],
    status: document.getElementsByClassName("js-response")[0],
    titleWrapper: document.getElementsByClassName("js-title-wrapper")[0]
};

/**
 * Flags.
 */
var animatingIconFlag = false;

/**
 * Global variables.
 */
var glob = {
    inputValue: "",
    name: getDefaultName(),
    status: getDefaultStatus(),
};

/**
 * global variable for socket
 */
var socket;

/**
 * Applies the passed style to the parent element.
 *
 * @param {Object} stylesObj
 */
Element.prototype.addStyle = function (stylesObj) {
    if (typeof stylesObj !== "object") return;

    for (var key in stylesObj) {
        this.style[key] = stylesObj[key];
    }
};

/**
 * Rotates the background boxes, transitions them to the new background,
 * and rotates them back.
 */
function animateIconBackground() {
    var animationValues = getAnimationValues(),
        easing = animationValues.easing,
        duration = animationValues.duration,
        delay = animationValues.delay,
        isDefaultName = glob.name === getDefaultName(),
        boxes,
        tempBoxWrapper;

    return new Promise(function (resolve, reject) {
        elements.boxWrapper.parentNode.addStyle({animationPlayState: "paused"});

        // Do the initial background rotation and set the transition.
        elements.boxWrapper.addStyle({
            transition: "transform " + duration + "ms " + easing,
            transform: "rotateZ(-180deg)"
        });

        // Create and insert a temporary background behind the original one,
        // so we can slide it into the view shortly.
        tempBoxWrapper = elements.boxWrapper.cloneNode(true);
        boxes = tempBoxWrapper.children;
        tempBoxWrapper.addStyle({transform: "rotateZ(-180deg) translateY(100%)"});

        for (var i = 0; i < boxes.length; i++) {
            // Leave the centre box alone!
            if (i === 4) continue;
            boxes[i].addStyle({
                backgroundColor: isDefaultName ? "" : getRandomHex(i)
            });
        }

        elements.boxWrapper.parentNode.insertBefore(
            tempBoxWrapper,
            elements.boxWrapper
        );

        // Wait until the initial rotation is done.
        setTimeout(function () {
            // Slide the original background out of the view, and the temporary one in.
            tempBoxWrapper.addStyle({transform: "rotateZ(-180deg)"});
            elements.boxWrapper.addStyle({
                transform: "rotateZ(-180deg) translateY(-100%)"
            });

            // Wait until the backgrounds are swapped.
            setTimeout(function () {
                // Remove the transform from the temporary background, make it the new original,
                // and remove the previous original.
                tempBoxWrapper.addStyle({transform: ""});
                elements.boxWrapper.remove();
                elements.boxWrapper = tempBoxWrapper;

                // Wait until the background is rotated back to its original position.
                setTimeout(function () {
                    elements.boxWrapper.parentNode.addStyle({animationPlayState: ""});
                    elements.boxWrapper.addStyle({transition: ""});
                    return resolve("");
                }, duration + delay);
            }, duration + delay);
        }, duration + delay);
    });
}

/**
 * Rotates the icon letter, transitions it to the new icon letter,
 * and rotates it back.
 *
 * @param {String} letter The letter to display.
 */
function animateIconLetter(letter) {
    var animationValues = getAnimationValues(),
        easing = animationValues.easing,
        duration = animationValues.duration,
        delay = animationValues.delay,
        tempTitleWrapper;

    return new Promise(function (resolve, reject) {
        // Do the initial title rotation and set the transition.
        elements.titleWrapper.addStyle({
            transition: "transform " + duration + "ms " + easing,
            transform: "rotateZ(180deg)"
        });

        // Create and insert a temporary title behind the original one,
        // so we can slide it into the view shortly. It has the new letter.
        tempTitleWrapper = elements.titleWrapper.cloneNode(true);
        tempTitleWrapper.children[0].innerText = letter;
        tempTitleWrapper.addStyle({
            transform: "rotateZ(180deg) translateY(-100%)"
        });
        elements.titleWrapper.parentNode.insertBefore(
            tempTitleWrapper,
            elements.titleWrapper
        );

        // Wait until the initial rotation is done.
        setTimeout(function () {
            // Slide the original title out of the view, and the temporary one in.
            tempTitleWrapper.addStyle({transform: "rotateZ(180deg)"});
            elements.titleWrapper.addStyle({
                transform: "rotateZ(180deg) translateY(100%)"
            });

            // Wait until the titles are swapped.
            setTimeout(function () {
                // Remove the transform from the temporary style, make it the new original,
                // and remove the previous original.
                tempTitleWrapper.addStyle({transform: ""});
                elements.titleWrapper.remove();
                elements.titleWrapper = tempTitleWrapper;

                // Wait until the title is rotated back to its original position.
                setTimeout(function () {
                    elements.titleWrapper.addStyle({transition: ""});
                    return resolve("");
                }, duration + delay);
            }, duration + delay);
        }, duration + delay);
    });
}

/**
 * Displays the passed message.
 *
 * @param {String} string The message to display.
 */
function displayMessage(string) {
    var animationValues = getAnimationValues(),
        easing = animationValues.easing,
        duration = animationValues.duration,
        delay = animationValues.delay,
        status = glob.status;

    return new Promise(function (resolve, reject) {
        // Hide the status.
        elements.status.addStyle({
            opacity: 0,
            transition: "opacity " + duration + "ms " + easing
        });

        // Wait until the status is hidden.
        setTimeout(function () {
            // Display the new message.
            elements.status.innerHTML = string || status;

            // Wait a while.
            setTimeout(function () {
                // Reveal the status.
                elements.status.addStyle({opacity: 1});

                // Wait until the status is revealed.
                setTimeout(function () {
                    elements.status.addStyle({opacity: "", transition: ""});
                    return resolve("");
                }, duration + delay);
            }, duration + delay);
        }, duration + delay);
    });
}

/**
 * Returns an object holding all of the animation preferences.
 */
function getAnimationValues() {
    return {
        easing: "cubic-bezier(.42, .23, .77, .61)",
        duration: 350,
        delay: 50
    };
}

/**
 * Returns the default user name.
 */
function getDefaultName() {
    return "Slack";
}

/**
 * Return the default status message.
 */
function getDefaultStatus() {
    return "Experience what it's like to work for Slack.";
}

/**
 * Generates a random HEX colour.
 *
 * @param {Integer} index The iteration index.
 */
function getRandomHex(index) {
    var chars = "0123456789abcdef",
        colour = "#";

    for (var i = 0; i < 6; i++) {
        colour = colour + chars[Math.floor(Math.random() * (chars.length + 1))];
    }

    return colour;
}


/**
 * The main animation.
 */
function getUserInsideSlack(event) {
    var error, message;

    // Intercept the page refresh.
    event.preventDefault();

    // Launch the animation only if it is not running already.
    if (animatingIconFlag) return;

    // Raise the flag so the animation cannot be launched again.
    animatingIconFlag = true;

    // Store the input value.
    glob.inputValue = elements.input.value.trim();

    // Do not animate if the name value is equal to the default name.
    if (!error && glob.inputValue === getDefaultName()) {
        error =
            "<span>You are already inside of Slack, <b>" + getDefaultName() + "</b>!</span>";
    }

    // Do not animate if the name value is equal to the previous value, which was rejected by server
    if (!error && glob.inputValue === glob.name) {
        error =
            "<span>Entering same name again will do no good, <b>" + glob.name + "</b>! -_-</span>";
    }

    // Do not animate if the input is empty and we have already reset
    // the value to default. Otherwise, let us reset to default.
    if (!error && !glob.inputValue && glob.name === getDefaultName()) {
        error = "You shall not pass! Unless you tell us your name.";
    }

    // Do not animate if the name is too long.
    if (!error && glob.inputValue.length > 36) {
        error = "There is no way your name is that long!";
    }

    // Do not animate if the name contains disallowed characters.
    if (
        !error &&
        glob.inputValue &&
        glob.inputValue.match(/^[A-Za-z-. ]+$/) === null
    ) {
        error = "Who on Earth would have a name like that?";
    }

    // Display the feedback message.
    message = glob.inputValue
        ? "Requesting server to take you inside!"
        : getDefaultStatus();

    glob.status = error || message;

    displayMessage().then(function () {
        // Release the flag.
        animatingIconFlag = false;
    });

    // Update the name.
    glob.name = glob.inputValue || getDefaultName();

    if (error) {
        shakeInputAnimation();
    }
    else {
        socket = new WebSocket("ws://" + window.location.host + window.location.pathname + "?username=" + glob.name);
        socket.onmessage = handleServerMessage;
    }
}

/**
 * Shakes the input to give a visual negative feedback to the user.
 */
function shakeInputAnimation() {
    var input = elements.input,
        offset = 8,
        duration = 80;

    // Shift the input to the left.
    input.addStyle({
        transform: "translateX(-" + offset + "px)",
        transition: "transform " + duration + "ms"
    });

    // Wait for the animation to finish.
    setTimeout(function () {
        // Shift the input to the right.
        input.addStyle({transform: "translateX(" + offset + "px)"});

        // Wait for the animation to finish.
        setTimeout(function () {
            // Shift the input to the default position.
            input.addStyle({transform: ""});

            // Wait for the animation to finish.
            setTimeout(function () {
                // Remove the transition.
                input.addStyle({transition: ""});
            }, duration);
        }, duration);
    }, duration);
}

elements.button.addEventListener("click", getUserInsideSlack);

function handleServerMessage(e) {
    // function will all the messages sent by server

    var payload = JSON.parse(e.data);
    var server_status = payload.status;
    var state = payload.state; // can have 2 values: connect, receive. Shows what state does the message represents.
    var message = payload.message;
    var is_bot = payload.bot;
    var username = payload.username;

    // if error received
    if ((state === 'c' || state === 'connect') && server_status >= 400) {
        // var error = payload.error;
        // deal with the error message
        animatingIconFlag = true;
        shakeInputAnimation();
        displayMessage(message).then(function () {
            // Release the flag
            animatingIconFlag = false;
        });
    }
    // server has accepted the user
    else if ((state === 'c' || state === 'connect') && server_status == 200) {
        // set the username in the chatting screen
        console.log(username);
        document.getElementById('username_text').value = username;

        // animate the background and display the welcome message
        // and fade out.
        animatingIconFlag = true;
        animateIconBackground();
        animateIconLetter(glob.name[0]);
        displayMessage(payload.message).then(function () {
            // Release the flag
            animatingIconFlag = false;
            document.getElementsByClassName("username_entry")[0].addStyle({
                display: "none",
                opacity: 0,
                transition: "opacity " + getAnimationValues().duration + "ms " + getAnimationValues().easing
            });
            fadeIn(document.getElementById("slack-container"));
        });
    }

    else if (state === 'r' || state === 'receive') {
        /** Sample html for chat message
         <li class="message">
         <div class="user-icon"><img
         src="http://socialmediaweek.org/wp-content/blogs.dir/1/files/slack-pattern-940x492.jpg">
         </div>
         <div class="body">
         <div class="username">navin</div>
         <div class="text">@kimberlygo: okay, i'll do it!</div>
         </div>
         </li>
         */
        var li = document.createElement('LI');
        li.className = 'message';
        var div_user_icon = document.createElement('DIV');
        div_user_icon.className = 'user-icon';
        var img = document.createElement('IMG');
        img.src = "http://socialmediaweek.org/wp-content/blogs.dir/1/files/slack-pattern-940x492.jpg";
        var div_body = document.createElement('DIV');
        div_body.className = 'body';
        var div_username = document.createElement('DIV');
        div_username.className = 'username';
        div_username.appendChild(document.createTextNode(username));
        var div_text = document.createElement('DIV');
        div_text.className = 'text';
        div_text.appendChild(document.createTextNode(message));
        div_user_icon.appendChild(img);
        div_body.appendChild(div_username);
        div_body.appendChild(div_text);
        li.appendChild(div_user_icon);
        li.appendChild(div_body);
        document.getElementsByClassName('messages')[0].appendChild(li);
    }
}

document.getElementById('send-message').onsubmit = function (event) {
    event.preventDefault();
    var message = document.getElementById('input-message').value;
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(message);
        document.getElementById('input-message').value = "";
    } else {
        console.error("Connection cannot be established")
    }
};

function fadeIn(el) {
    el.style.opacity = 0;
    el.style.display = "block";
    var tick = function () {
        el.style.opacity = +el.style.opacity + 0.01;
        if (+el.style.opacity < 1) {
            (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16)
        }
    };
    tick();
}
