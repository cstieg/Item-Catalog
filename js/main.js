
/*Resize pictures to be square*/
$(window).resize(function() {
  $('.catalog-picture').height($('.catalog-picture').width());
  $('.item-picture').height($('.item-picture').width());
});
$(window).resize();

/*Set callback function for <accept> button in confirm delete dialogs. Called when
opening Bootstrap dialog window.
Parameter:
- callbackText: A string containing the function call to be called when the button
is clicked.
*/
function setDialogCallback(callbackText) {
  $('#delete-dialog button[name=delete]').attr('onclick', callbackText);
}

/*Makes POST request to delete catalog*/
function deleteCatalog(catalogID) {
  $.ajax({
    type: 'POST',
    url: '/deletecatalog/' + catalogID,
    success: closeDeleteDialog,
    error: deleteFailure
  });
}

/*Makes POST request to delete category*/
function deleteCategory(catalogID, categoryID) {
  $.ajax({
    type: 'POST',
    url: '/catalog/' + catalogID + "/deletecategory/" + categoryID,
    success: closeDeleteDialog,
    error: deleteFailure
  });
}

/*Makes POST request to delete item*/
function deleteItem(catalogID, itemID) {
  $.ajax({
    type: 'POST',
    url: '/catalog/' + catalogID + "/deleteitem/" + itemID,
    success: closeDeleteDialog,
    error: deleteFailure
  });
}

/*Closes the delete confirmation dialog box when delete POST request returns successfully*/
function closeDeleteDialog() {
  $('#delete-dialog').modal('hide');
}

/*Alerts user to unsuccessful delete POST request*/
function deleteFailure() {
  alert('You are not the owner of this item and do not have authorization to delete!');
}


/*******************************GOOGLE OAUTH2**********************************/
/*Code provided by Google*/

/*Initializes the Google Oauth2 API*/
gapi.load('auth2', function() {
  auth2 = gapi.auth2.init({
    client_id: '1050453128023-lpuo4af45992ivtcf80jqq4gpghka0l0.apps.googleusercontent.com',
    // Scopes to request in addition to 'profile' and 'email'
    //scope: 'additional_scope'
  });
});

/*Sets the callback function to be called when clicking the Google signin button*/
$('#gsignin').click(function() {
  // signInCallback defined in step 6.
  auth2.grantOfflineAccess().then(signInCallback);
});

/*After receiving an authorization code from Google requested by user, send it
  to server in order to exchange code for full credentials from Google*/
function signInCallback(authResult) {
  if (authResult['code']) {
    // Hide the sign-in button now that the user is authorized
    $('#gsignin').attr('style', 'display: none');
    $.ajax({
      type: 'POST',
      url: '/gconnect',
      // Always include an `X-Requested-With` header in every AJAX request,
      // to protect against CSRF attacks.
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // redirect to main page
        window.location.href = '/';
      },
      error: function(result) {
        alert('Failed to make a server-side call. Check your configuration and console.');
      }
    });
  }
}

/*Sends a logout call to server and disconnects from Google OAuth2 clientside*/
function googleLogout() {
  $.ajax({
    type: 'POST',
    url: '/logout',
    // Always include an `X-Requested-With` header in every AJAX request,
    // to protect against CSRF attacks.
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    },
    processData: false,
    contentType: 'application/octet-stream; charset=utf-8',
    success: function(result) {
      // disconnect from Google OAuth2 API
      auth2.disconnect();
      alert('Succesfully logged out!');
    },
    error: function(result) {
      alert('Failed to make a server-side call. Check your configuration and console.');
    }
  });
}
