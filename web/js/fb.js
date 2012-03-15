window.fbAsyncInit = function() {
	FB.init({
		appId      : '366467473377722',
		status     : true, 
		cookie     : true,
		xfbml      : true,
		oauth      : true,
	});					  

	function login(response, info){
		if (response.authResponse) {
			var accessToken      =   response.authResponse.accessToken;		
			userInfo.innerHTML   = /*'<img width=25 height=25 src="https://graph.facebook.com/' + info.id + '/picture"> ' +*/ info.name;					
			button.style.display     = 'none';
			loggedin.style.display   = 'block';
		}
	}

	function logout(response){
		userInfo.innerHTML  =  "";
		loggedin.style.display   = 'none';
		button.style.display     = 'block';
	}	
					
	function updateButton(response) {
		button       =   document.getElementById('fb-auth');
		userInfo     =   document.getElementById('user-info');
		loggedin     =   document.getElementById('loggedin');
		logoutlink   =   document.getElementById('logout');
		
		logoutlink.onclick = function() {
			FB.logout(function(response) {
				logout(response);
			});
		};
			
		button.onclick = function() {
			FB.login(function(response) {
				if (response.authResponse) {
					FB.api('/me', function(info) {
						login(response, info);
					});
				} else {
					//user cancelled login or did not grant authorization
				}
			}, {scope:'email,user_birthday,status_update,publish_stream,user_about_me'});
		}
		
		if (response.status === 'connected') {
			//user is already logged in and connected			
			if (response.authResponse) {
				FB.api('/me', function(info) {
					login(response, info);
				});
			}
		} else if (response.status === 'not_authorized') {
			// the user is logged in to Facebook, 
			// but has not authenticated your app
		} else {
			// the user isn't logged in to Facebook.
		}
	}

	//whenever the status changes
	FB.Event.subscribe('auth.statusChange', updateButton);
};
	
(function(d){
   var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
   js = d.createElement('script'); js.id = id; js.async = true;
   js.src = "//connect.facebook.net/en_US/all.js";
   d.getElementsByTagName('head')[0].appendChild(js);
 }(document));