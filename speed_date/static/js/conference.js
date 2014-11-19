/**
 * Created by GoldenGate on 11/13/14.
 */
var room;

// when Bistri API client is ready, function
// "onBistriConferenceReady" is invoked
onBistriConferenceReady = function () {
    getUserLocation();
    // test if the browser is WebRTC compatible
    if ( !BistriConference.isCompatible() ) {
        // if the browser is not compatible, display an alert
        alert( "your browser is not WebRTC compatible !" );
        // then stop the script execution
        return;
    }

    // initialize API client with application keys
    // if you don't have your own, you can get them at:
    // https://api.developers.bistri.com/login
    BistriConference.init( {
        appId: "96ce4396",
        appKey: "a5408fe55d6a1f476d279c353f195562",
        userId: userId,
        userName: userName,
		debug: true
    } );

    /* Set events handler */

    // when local user is connected to the server
    BistriConference.signaling.addHandler( "onConnected", function () {
        // show pane with id "pane_1"
        showPanel( "pane_1" );
    } );

    // when an error occured on the server side
    BistriConference.signaling.addHandler( "onError", function ( error ) {
        // display an alert message
        alert( error.text + " (" + error.code + ")" );
    } );

    // when the user has joined a room
    BistriConference.signaling.addHandler( "onJoinedRoom", function ( data ) {
        // set the current room name
        room = data.room;
		// then, for every single members present in the room ...
		for ( var i=0, max=data.members.length; i<max; i++ ) {
			// ... request a call
			BistriConference.call( data.members[ i ].id, data.room );
		}
        });

    // when an error occurred while trying to join a room
    BistriConference.signaling.addHandler( "onJoinRoomError", function ( error ) {
        // display an alert message
       alert( error.text + " (" + error.code + ")" );
    } );

    // when the local user has quitted the room
    BistriConference.signaling.addHandler( "onQuittedRoom", function( room ) {
        // reset the current room name
		room = undefined;
        // show pane with id "pane_1"
        showPanel( "pane_1" );
        // stop the local stream
        BistriConference.stopStream( BistriConference.getLocalStreams()[ 0 ], function( stream ){
			// remove the local stream from the page
			BistriConference.detachStream( stream );
		} );
    } );

    // when a new remote stream is received
    BistriConference.streams.addHandler( "onStreamAdded", function ( remoteStream ) {
        // insert the new remote stream into div#video_container node
        BistriConference.attachStream( remoteStream, q( "#video_container" ) );
    } );

    // when a local or a remote stream has been stopped
    BistriConference.streams.addHandler( "onStreamClosed", function ( stream ) {
        // remove the remote stream from the page
        BistriConference.detachStream( stream );
		// if room has not been quitted yet
		if( room ){
			// quit room
			BistriConference.quitRoom( room );
		}
    } );

    // when a remote user presence status is received
    BistriConference.signaling.addHandler( "onPresence", function ( result ) {
        if( result.presence != "offline" ){
			// ask the user to access to his webcam
			BistriConference.startStream( "webcamSD", function( localStream ){
				// when webcam access has been granted
				// show pane with id "pane_2"
				showPanel( "pane_2" );
				// insert the local webcam stream into div#video_container node
				BistriConference.attachStream( localStream, q( "#video_container" ) );
				// invite user
				BistriConference.call( result.id, getRandomRoomName() );
			} );
        }
        else{
            alert( "The user you try to reach is currently offline" );
        }
    } );
    // when a call request is received from remote user
    BistriConference.signaling.addHandler( "onIncomingRequest", function ( request ) {
		// ask the user to accept or decline the invitation
//		if( confirm( request.name + " is inviting you to join his conference room. Click \"Ok\" to start the call." ) ){
			// invitation has been accepted
			// ask the user to access to his webcam
        console.log("connecting user local:");
        console.log(request.name);
        window.other_username = request.name;

			 BistriConference.startStream( "webcamSD", function( localStream ){
				// when webcam access has been granted
				// show pane with id "pane_2"
				showPanel( "pane_2" );
				// insert the local webcam stream into div#video_container node
				BistriConference.attachStream( localStream, q( "#video_container" ) );
			   // then join the room specified in the "request" object
				BistriConference.joinRoom( request.room );
			} );
//		}
	});
    // bind function "callUser" to button "Call XXX"
    q( "#call" ).addEventListener( "click", callUser );

    // bind function "stopCall" to button "Stop Call"
    q( "#quit" ).addEventListener( "click", stopCall );

    // open a new session on the server
    BistriConference.connect();
};

// when button "Call XXX" has been clicked
function callUser(){
	// check remote user presence
    BistriConference.getPresence( remoteUserId );
}

// when button "Stop Call" has been clicked
function stopCall(){
    // quit the current conference room
    BistriConference.quitRoom( room );
}

function getRandomRoomName(){
    var chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
    var randomId = "";
    for( var i=0; i<20; i++ ){
        randomId += chars.charAt( Math.random() * 63 );
    }
	// return a random room name
    return randomId;
}

function showPanel( id ){
    var panes = document.querySelectorAll( ".pane" );
    // for all nodes matching the query ".pane"
    for( var i=0, max=panes.length; i<max; i++ ){
        // hide all nodes except the one to show
        panes[ i ].style.display = panes[ i ].id == id ? "block" : "none";
    };
}

function q( query ){
    // return the DOM node matching the query
    return document.querySelector( query );
}


// User Location

var getUserLocation = function () {
    console.log("getting location");
    //check if the geolocation object is supported, if so get position
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(displayLocation, displayError);
    }
};


var displayLocation = function (position) {

    //build text string including co-ordinate data passed in parameter
    var displayText = "User latitude is " + position.coords.latitude + " and longitude is " + position.coords.longitude;

    //display the string for demonstration
    document.getElementById("locationData").innerHTML = displayText;
};

var displayError = function (error) {

    //get a reference to the HTML element for writing result
    var locationElement = document.getElementById("locationData");

    //find out which error we have, output message accordingly
    switch (error.code) {
        case error.PERMISSION_DENIED:
            locationElement.innerHTML = "Permission was denied";
            break;
        case error.POSITION_UNAVAILABLE:
            locationElement.innerHTML = "Location data not available";
            break;
        case error.TIMEOUT:
            locationElement.innerHTML = "Location request timeout";
            break;
        case error.UNKNOWN_ERROR:
            locationElement.innerHTML = "An unspecified error occurred";
            break;
        default:
            locationElement.innerHTML = "Who knows what happened...";
            break;
    }
};

// CHAT
$(document).ready(function() {
//$('#video_container').children().eq(1).css("opacity", .1);
    var clear = false;
    user_id = $('.chat_area').attr('id');
    dater_id = $('.user').attr('id');
    function loadMessages_fade_video_and_check_online() {
        if ($('#video_container').children().eq(1).length != 0 && clear == false) {
            clear = true;
            $('#video_container').children().eq(1).fadeIn(100000);
            console.log("fading")
        }
        if (typeof window.other_username === 'undefined') {
            other_user = dater_id;
        }
        else {
            other_user = window.other_username;

        }
        if ($('#video_container').children().eq(1).length == 0) {
            clear = false
        }
        $.ajax({
            url: '../../chat_messages/' + other_user,
            type: 'GET',
            success: function (data) {
                $('.message_area').html(data)
                $(".message_area").scrollTop($(".message_area")[0].scrollHeight);
            }
        });
        $.ajax({
            url: '../../chat_with/' + other_user,
            type: 'GET',
            success: function (data) {
                $('#chat_with').html(data)
            }
        });
        $.ajax({
            url: '../../online/',
            type: 'GET',
            success: function (data) {
            }
        });
    }

    loadMessages_fade_video_and_check_online();
    $(".message_area").scrollTop($(".message_area")[0].scrollHeight);
    setInterval(loadMessages_fade_video_and_check_online, 500);

    $(".add_message").on("click", function () {
        add_message()
    });
    $('#message_id').keypress(function (e) {
        if (e.which == 13) {
            add_message(function () {
            })

        }
    });
    var add_message = function () {
        content = $('#message_id').val();
        if (typeof window.other_username === 'undefined') {
            other_user = dater_id;
        }
        else {
            other_user = window.other_username;
        }
        var new_message = {
            message: content,
            sender: user_id,
            recipient: other_user
        };
        new_message = JSON.stringify(new_message);
        $.ajax({
            url: '../../new_message/',
            type: 'POST',
            dataType: 'json',
            data: new_message,
            success: function (response) {
                $('#message_id').val("");
            }
        });
    };
    $("#liked").on("click", function () {
        if (typeof window.other_username === 'undefined') {
            other_user = dater_id;
        }
        else {
            other_user = window.other_username;
        }
        $.ajax({
            url: '../../liked/' + other_user,
            type: 'GET',
            success: function (data) {
                $("#liked").html("Liked!")
            }
        });
    });
    $("#flag").on("click", function () {
        if (typeof window.other_username === 'undefined') {
            other_user = dater_id;
        }
        else {
            other_user = window.other_username;
        }
        var response = confirm("Are you sure you want to flag this user? Please flag only for explicit content");
        if (response == true){
            $.ajax({
                url: '../../flag/' + other_user,
                type: 'GET',
                success: function (data) {
                    $("#flag").html("Flagged")
                }
            });
        }
    });
    $("#newPerson").on("click", function () {
        location.reload()
    });
});